from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import TikTokPost, Comment
from configuration import client
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TikTok Data API",
    description="API for accessing TikTok scraped data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
try:
    db = client['tiktok_scraper']
    collection = db['new_posts_comment']
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

@app.get("/")
async def root():
    return {"message": "Welcome to TikTok Data API"}

@app.get("/posts", response_model=List[TikTokPost])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    username: Optional[str] = None,
    hashtag: Optional[str] = None
):
    try:
        query = {}
        if username:
            query["username"] = username
        if hashtag:
            query["hashtags"] = hashtag

        logger.info(f"Executing query: {query}")
        posts = list(collection.find(query).skip(skip).limit(limit))
        logger.info(f"Found {len(posts)} posts")
        
        # Convert ObjectId to string for each post
        for post in posts:
            post['_id'] = str(post['_id'])
        
        return posts
    except Exception as e:
        logger.error(f"Error in get_posts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts/{post_id}", response_model=TikTokPost)
async def get_post(post_id: str):
    try:
        post = collection.find_one({"_id": ObjectId(post_id)})
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        post['_id'] = str(post['_id'])
        return post
    except Exception as e:
        logger.error(f"Error in get_post: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/posts/search/{keyword}", response_model=List[TikTokPost])
async def search_posts(keyword: str):
    try:
        query = {
            "$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"username": {"$regex": keyword, "$options": "i"}},
                {"hashtags": {"$regex": keyword, "$options": "i"}}
            ]
        }
        posts = list(collection.find(query))
        # Convert ObjectId to string for each post
        for post in posts:
            post['_id'] = str(post['_id'])
        return posts
    except Exception as e:
        logger.error(f"Error in search_posts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        total_posts = collection.count_documents({})
        total_comments = collection.aggregate([
            {"$project": {"comment_count": {"$size": "$comments"}}},
            {"$group": {"_id": None, "total": {"$sum": "$comment_count"}}}
        ])
        total_comments = list(total_comments)[0]["total"] if total_comments else 0
        
        return {
            "total_posts": total_posts,
            "total_comments": total_comments
        }
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)