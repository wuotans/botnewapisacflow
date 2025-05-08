import os
import uuid
from openai import OpenAI
import base64
import requests
import logging

class Vision:

    def __init__(self,model:str="gpt-4o"):
        self.client = OpenAI()
        self.model = model


    # Function to encode the image
    def encode_image(self,image_path):
        with open(image_path, "rb") as image_file:
            base64_content = base64.b64encode(image_file.read()).decode('utf-8')
        os.remove(image_path)
        return base64_content

    def get_image(self,path_image):
        resp = requests.get(path_image)
        os.makedirs('files', exist_ok=True)
        name_file = 'img_' + str(uuid.uuid4()) + '.jpeg'
        path_file = os.path.join('files', name_file)
        with open(path_file,'wb') as f:
            f.write(resp.content)
        return path_file


    def identify_type_image(self,path_image):
        base64_url = f"data:image/jpeg;base64,{self.encode_image(self.get_image(path_image))}" \
            if 'https://' in path_image else f"data:image/jpeg;base64,{self.encode_image(path_image)}"
        return base64_url


    def submit_image(self,path_image,prompt="Whats in this image?",max_tokens=300,**kwargs):

        list_objects = []
        if isinstance(path_image,list):
            for path_ in path_image:
                list_objects.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": self.identify_type_image(path_),
                        }
                    }
                )
        else:
            list_objects = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": self.identify_type_image(path_image),
                    }
                }
            ]
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *list_objects
                    ],
                }
            ],
            max_tokens=max_tokens,
            **kwargs
        )
        message = self.response.choices[0].message.content
        logging.info(message)
        return message