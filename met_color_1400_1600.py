import requests
from PIL import Image
import colorgram
import csv

endpoint_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
parameters = {"q": "modern art", "dateBegin": "1400", "dateEnd": "1600"}

response = requests.get(endpoint_url, params=parameters)

object_ids = response.json()["objectIDs"]

dominant_colors_list = []
artwork_info_list = []


for object_id in object_ids:
    object_response = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}")
    object_data = object_response.json()

    medium = object_data["medium"]
    title = object_data["title"]
    
   
    if ',' in medium:
        mediums = medium.split(', ')
        for medium in mediums:
            artwork_info_list.append((object_id, medium, title))
    else:
        artwork_info_list.append((object_id, medium, title))
  
    image_url = object_data["primaryImageSmall"]
    

    image = Image.open(requests.get(image_url, stream=True).raw)
    
  
    colors = colorgram.extract(image, 10)
 
    dominant_colors = [color.rgb for color in colors]
    dominant_colors_list.append(dominant_colors)

##################################################
with open("dominant_colors.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Artwork ID"] + [f"Color {i+1}" for i in range(10)])
    for i, colors in enumerate(dominant_colors_list):
        writer.writerow([object_ids[i]] + [f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}" for color in colors[:10]])

with open("artwork_info_renaissance_refined.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Artwork ID", "Medium", "Title"])
    for artwork_info in artwork_info_list:
        writer.writerow(artwork_info)