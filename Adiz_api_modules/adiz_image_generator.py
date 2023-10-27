import openai
import urllib.request


class ImageGenerator:
    generated_image = ''
    def __init__(self,apikey='openai api key here'):
        openai.api_key = apikey 
        
    def generate(self,description,img_size,n_of_images=1):
        if not self.__mod_prompt(prompt):
            response = openai.Image.create(
               prompt=description,
               n=n_of_mages,
               size = img_size
            )
            return response
        else:
            return {"error": "Don't talk dirt!"}
        


    def edit(self, description, image_url, mask_url,img_size,n_of_images=1):
        with urllib.request.urlopen(image_url) as url:
            # Read image data using a buffered reader
            image_file = url.read()
        with urllib.request.urlopen(mask_url) as url:
            # Read image data using a buffered reader
            mask_image = url.read()
        response = openai.Image.create_edit(
        image=image_file,
        mask=mask_image,
        prompt=description,
        n=n_of_images,      
        size=img_size
        )
        print (response)
        image_url = response['data'][0]['url']
        self.generated_image = image_url
        print (response)
        return
    
    def __mod_prompt(self, prompt):
        response = openai.Moderation.create(
            input=prompt
            )
        return response['results'][0]['flagged']






