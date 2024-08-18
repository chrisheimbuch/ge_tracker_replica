#Imports
from flask import Flask
from markupsafe import escape
from dotenv import load_dotenv
import requests
import os

#Initiate the flask call
app = Flask(__name__)
load_dotenv()
user_agent= os.getenv("USER_AGENT")

#Home page of website denoted by "/". The function returns the text of whatever you want to say.
@app.route("/")
def home_interface():
    return "<p>Welcome to home screen. Enter an item ID to get information.</p>"

#User inputs an item ID, and returns on a new webpage based off the ID, the high price, low price, high alch value, examine details, and image of item. 
@app.route("/<item_id>")
def item_id(item_id):
    url = f'https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}'
    headers = {'user-agent': user_agent}
    r = requests.get(url, headers=headers)
    price = r.json()['data'][item_id]
    high = price['high']
    low = price['low']
    mapping_response = get_mapping(item_id)
    high_alch = mapping_response['highalch']
    examine = mapping_response['examine']
    image_png = mapping_response["icon"].replace(" ", "_")
    image_url = f"https://oldschool.runescape.wiki/images/{image_png}"

    return f'''
        Here is the high price and low price of the {mapping_response["name"]}: 
        <p>High price: {escape("{:,}".format(high))}</p>
        <p>Low price: {escape("{:,}".format(low))}</p>
        <p>High Alch Value: {escape("{:,}".format(high_alch))}</p>
        <p>Examine Details: {escape((examine))}</p>
        <img src={image_url} alt={image_png}/>

    '''

#Getting mapping of all items from the OSRS wiki, which is a JSON format, which includes the examine text, item id number, if it's a members item or not,
#low alch amount, GE buy limit, Current GE value price, high alch value, the item name, and item icon in a PNG format.
def get_mapping(item_id):
    url = f'https://prices.runescape.wiki/api/v1/osrs/mapping'
    headers = {'user-agent': user_agent}
    r = requests.get(url, headers=headers)

    for item in r.json():
        if int(item_id) == int(item["id"]):
            return item


#Reference to see what would be returned from r.json.
# {
#     "examine": "Fabulously ancient mage protection enchanted in the 3rd Age.",
#     "id": 10344,
#     "members": true,
#     "lowalch": 20200,
#     "limit": 8,
#     "value": 50500,
#     "highalch": 30300,
#     "icon": "3rd age amulet.png",
#     "name": "3rd age amulet"
#   },