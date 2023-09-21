import requests
import PIL
from io import BytesIO
import os
from pathvalidate import sanitize_filename
import res.tarkovItem as tarkovItem
import json
import collections

def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def get_all_barter_items():
    items = []
    query = """
    {
    items(categoryNames:BarterItem) {
        name
        gridImageLink
    		craftsFor{
        	station{
          	  name
            
        	}
        	level
        }
    }
}
    """
    result = run_query(query)
    items = result["data"]["items"]
    return items
    
def get_all_craftable_barter_items():
    craftable = []
    items = get_all_barter_items()
    for item in items:
        if item["craftsFor"] != []:
            craftable.append(item)
    return craftable
    
    
def ask_for_item(itemname: str):
    new_query = '''
    {{
    items(name:"{itemname}") {{
        name
        gridImageLink
        craftsFor{{
        station{{
            name
            
        }}
        level
        }}
        }}
    }}
    '''.format(itemname = itemname.strip("\n"))
    result = run_query(new_query)
    if result["data"]["items"][0]["craftsFor"] != None:
        return result["data"]["items"][0]["name"], result["data"]["items"][0]["gridImageLink"]
    else:
        return None, None

def get_image_from_url(name, imageurl, basepath):
    if name == None:
        return
    if(os.path.isfile(f"{basepath}/{sanitize_filename(name)}.png")):
        return
    r = requests.get(imageurl)
    image = PIL.Image.open(BytesIO(r.content))
    image = image.convert("RGB")
    image.save(f"{basepath}/{sanitize_filename(name)}.png", "png")

def save_items_to_json(items, filepath):
    with open(filepath, "w") as f:
        json.dump(items, f)
        
        
        
