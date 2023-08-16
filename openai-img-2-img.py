import requests
import json
import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")
openai_api_base = "https://api.openai.com/v1"
openai_api_image_generation = "https://api.openai.com/v1/images/variations"

azure_openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
use_azure = False

def image_to_image(api_key: str, api_url: str, imagefile: str, imagesize: str ="256x256", num_images: int = 1):
   authorization = f"Bearer {api_key}"
   headers = {'Content-type': 'application/json', 'Authorization': authorization}
   data = {'image': f"@{imagefile}", 'n':num_images, 'size': imagesize, 'response_format': 'url'}
   response = requests.post(api_url, data=json.dumps(data), headers=headers)
   return response.json()['data'][0]['url']

def create_image_variation(imagefile: str, imagesize: str ="256x256", num_images: int = 1):
   if use_azure:
      openai.api_type = "azure"
      openai.api_version = "2023-05-15"
      openai.api_key = azure_openai_api_key
      openai.api_base = azure_openai_api_base
   else:
      openai.api_type = "openai"
      openai.api_version = '2020-11-07'
      openai.api_key = openai_api_key
      openai.api_base = openai_api_base
      if openai_org_id:
         openai.organization = openai_org_id

   response = openai.Image.create_variation(
                    image=open(imagefile, "rb"),
                    n=num_images,
                    size=imagesize)
   image_urls = [data['url'] for data in response['data']]
   return image_urls

def main():
   imagefile="avatar.png"
   output = image_to_image(openai_api_key,openai_api_image_generation, imagefile)
   print(output)
   image_urls = create_image_variation(imagefile)
   for image_url in image_urls:
      print(image_url)

if __name__ == '__main__':
    main()
