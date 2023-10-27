import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

#this module is not used in the api but it's useful when we deal with image manipulation.

cloudinary.config(
    cloud_name="cloudinary cloud name here",
    api_key="cloudinary api key here",
    api_secret="cloudinary api secret here",
    secure=True,
)

class ImageManager:

    cloudinary_pub_id = ''
    cloudinary_sec_url = ''
    cloudinary_converted_url = ''
    cloudinary_resized_url = ''
    
    def convert(self,cx,cy,csize):
        converted_image_url = cloudinary.utils.cloudinary_url(
            self.cloudinary_pub_id,
            format="png",
            fetch_format="png",
            flags="preserve_transparency",
            crop="crop",
            x=cx,
            y=cy,
            width=csize,
            height=csize
        )[0]
        self.cloudinary_converted_url = converted_image_url
        return {'success': True}

    def resize(self, new_width, new_height):
        resized_image_url = cloudinary.utils.cloudinary_url(
            self.cloudinary_pub_id,
            format="png",
            fetch_format="png",
            width=new_width,
            height=new_height
        )[0]
        self.cloudinary_resized_url = resized_image_url
        return {'success': True}

    def upload(self,imagefile):

        upload_result = cloudinary.uploader.upload(imagefile)
        self.cloudinary_pub_id = upload_result['public_id']
        self.cloudinary_sec_url = upload_result['url']
        return {'success': True}

  
   
    

