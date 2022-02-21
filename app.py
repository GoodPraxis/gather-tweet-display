import functools
import http.server
import os
import requests
import socketserver
import textwrap
import threading
from PIL import Image, ImageDraw
from config import twitter_token, twitter_userid, gather_api_key, gather_space_id, gather_object_name, domain, gather_map_id
from time import sleep

BACKGROUND_COLOR = (16, 16, 16)
TEXT_COLOR = (251, 224, 114)
STATIC_FOLDER = 'static'

PORT = 8000

def make_payload(map_id=None, map_content=None):
  return {
    "apiKey": gather_api_key,
    "spaceId": gather_space_id,
    "mapId": map_id,
    "mapContent": map_content,
  }

def update_object_image(map_id, name, img):
  headers = {"Content-type": "application/json", "Accept": "text/plain"}
  new_payload = make_payload(map_id=map_id)
  data = requests.get("https://gather.town/api/getMap", params=new_payload)
  map_data = data.json()
  objects = map_data["objects"]
  for obj in objects:
    if obj["_name"] == name:
      obj["highlighted"] = img
      obj["normal"] = img
      break
  map_data["objects"] = objects
  new_payload = make_payload(map_id=map_id, map_content=map_data)
  requests.post(
    "https://gather.town/api/setMap",
    data=json.dumps(new_payload),
    headers=headers,
  )


Handler = functools.partial(
  http.server.SimpleHTTPRequestHandler,
  directory=STATIC_FOLDER,
)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
  thread = threading.Thread(target = httpd.serve_forever)


while True:
  response = requests.get(
    'https://api.twitter.com/2/users/{}/tweets?max_results=5'.format(twitter_userid),
    headers={'Authorization': 'Bearer {}'.format(twitter_token)})
  try:
    json = response.json()
    tweet = json['data'][0]
    text = tweet['text']
    tweet_id = tweet['id']
    img = Image.new('RGB', (256, 64), color = BACKGROUND_COLOR)

    d = ImageDraw.Draw(img)
    d.text((4,4), textwrap.fill(text, width = 42), fill = TEXT_COLOR)

    if not os.path.exists(STATIC_FOLDER):
      os.makedirs(STATIC_FOLDER)

    img.save('./{}/{}.png'.format(STATIC_FOLDER, tweet_id))

    update_object_image(gather_map_id, gather_object_name, '{}/{}.png'.format(domain, tweet_id))
  except:
    print('Could not retrieve tweet')

  sleep(60)
