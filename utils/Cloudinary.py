import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

cloudinary.config(
          cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
          api_key=os.getenv("CLOUDINARY_KEY"),
          api_secret=os.getenv("CLOUDINARY_SECRET")
        )

class Cloudinary:

    @staticmethod
    def upload_image(file_path: str):
        return cloudinary.uploader.upload(file_path)
