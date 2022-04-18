from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()
posts = [{
  "title": "Post 1",
  "content": "Content 1",
  "published": True,
  "id": randrange(0, 2500000)
}, {
  "title": "Post 2",
  "content": "Content 2",
  "published": False,
  "id": randrange(0, 2500000)
}]

class CreatePost(BaseModel):
  title: str
  content: str
  published: bool = True

def find_post_by_id(id: int):
  for index, post in enumerate(posts):
    if post["id"] == id:
      return (index, post)
  return (-1, None)

@app.get("/")
async def root():
  return {
    "message": "Welcome to my api"
  }

@app.get("/posts")
async def get_posts():
  return posts

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
  post = None
  for _post in posts:
    if _post["id"] == int(id):
      post = _post
      break

  if not post:
    response.status_code = status.HTTP_404_NOT_FOUND
  return {
    "data": post
  }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(create_post: CreatePost):
  create_post_payload = create_post.dict()
  create_post_payload["id"] = randrange(1, 2500000)
  posts.append(create_post_payload)
  return create_post_payload

@app.delete("/posts/{id}")
async def delete_post(id: int, response: Response):
  (id_index, deleted_post) = find_post_by_id(id)
  if id_index == -1:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {
      "data": None
    }
  
  posts.pop(id_index)
  return {
    "data": deleted_post
  }

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
async def update_post(id: int, update_post: CreatePost, response: Response):
  updated_post_payload = update_post.dict()
  (id_index, _) = find_post_by_id(id)
  if id_index == -1:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {
      "data": None
    }
  updated_post_payload["id"] = id
  posts[id_index] = updated_post_payload
  return {
    "data": updated_post_payload
  }

