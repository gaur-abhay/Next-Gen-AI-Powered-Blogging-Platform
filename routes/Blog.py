import json

from fastapi import APIRouter, Depends, UploadFile, File, Form, Body
from routes import oauth2_scheme, supabase_manager
from typing import Optional
import uuid
from datetime import datetime
from schemas.BlogSchema import CreateBlogSchema, GenerateBlogSchema
from utils.Cloudinary import Cloudinary
from utils.NoSqlHandler import NoSqlHandler
from utils.Gemini import GeminiUtils

api_router = APIRouter()


@api_router.post("/create-blog")
async def translate_user_message(
        blog_data: str = Body(...),
        image_file: Optional[UploadFile] = Form(None),
        token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)
    blog_data = json.loads(blog_data)

    image_url = None
    if image_file:
        cloudinary_response = Cloudinary.upload_image(image_file.file)
        image_url = cloudinary_response.url

    document = {
        "id": str(uuid.uuid4()),
        "userid:": auth_user.user.id,
        "title": blog_data["title"],
        "description": blog_data["description"],
        "image_url": image_url,
        "created_on": datetime.utcnow().isoformat(),
        "tag": blog_data["tag"],
        "likes": 0,
        "views": 0,
        "comments": [],
    }
    NoSqlHandler.create_document(document, "Blogs")

    return {"message": "Blog Created Successfully"}


@api_router.post("/generate_blog")
async def generate_blog_for_user(
        request_data: GenerateBlogSchema,
        token: str = Depends(oauth2_scheme),
        gemini_utils: GeminiUtils = Depends(GeminiUtils)
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    response = gemini_utils.generate_blog_post(request_data.title, request_data.topic, request_data.tone)

    return {"title": response["title"], "body": response["body"]}


@api_router.get("/delete_blog/{blog_guid}")
async def get_all_blogs(
    blog_guid: str,
    token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    NoSqlHandler.delete_document(blog_guid, "Blogs")

    return {"message": "Blog Deleted Successfully"}


@api_router.get("/blog/{blog_guid}")
async def get_blog(
    blog_guid: str,
    token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    document = NoSqlHandler.read_document(blog_guid, "Blogs")

    if document["userid"] == auth_user.user.id:
        return {"blog": document, "write_access": True}

    return {"blog": document, "write_access": False}


@api_router.get("/all_blogs")
async def get_all_blogs(
    token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    documents = NoSqlHandler.read_all("Blogs")

    all_blogs = [doc for doc_id, doc in documents.items()]

    return {"all_blogs": all_blogs}


@api_router.get("/all_user_blogs")
async def get_all_user_blogs(
    token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)
    user_id = auth_user.user.id

    documents = NoSqlHandler.read_all("Blogs")

    user_blogs = [doc for doc_id, doc in documents.items() if doc["userid"] == user_id]

    return {"user_blogs": user_blogs}


@api_router.post("/like/{blog_guid}")
async def comment_on_blog(
        blog_guid: str,
        token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    document = NoSqlHandler.read_document(blog_guid, "Blogs")

    document["likes"] += 1
    NoSqlHandler.update_document(document, "Blogs")

    return {"message": "Blog Liked Successfully"}


@api_router.post("/comment/{blog_guid}")
async def comment_on_blog(
        blog_guid: str,
        comment: str = Body(...),
        token: str = Depends(oauth2_scheme),
):
    supabase = supabase_manager.get_supabase_db()
    auth_user = supabase.auth.get_user(token)

    document = NoSqlHandler.read_document(blog_guid, "Blogs")

    document["comments"].append({
        {
            "userid": auth_user.user.id,
            "comment": comment,
            "date": datetime.utcnow().isoformat(),
        }
    })
    NoSqlHandler.update_document(document, "Blogs")

    return {"message": "Blog Commented Successfully"}
