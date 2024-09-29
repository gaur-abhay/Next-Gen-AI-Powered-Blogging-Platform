from pydantic import BaseModel

class CreateBlogSchema(BaseModel):
    title: str
    description: str


class GenerateBlogSchema(BaseModel):
    title: str
    topic: str
    tone: str
