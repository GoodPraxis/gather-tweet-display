import os
import requests
import textwrap
import json
from time import sleep
from PIL import Image, ImageDraw

from config import (
    twitter_token,
    twitter_userid,
    gather_api_key,
    gather_space_id,
    gather_object_name,
    domain,
    gather_map_id,
)


BACKGROUND_COLOR = (16, 16, 16)
TEXT_COLOR = (251, 224, 114)
STATIC_FOLDER = 'static'

PORT = 8000


def format_tweet_text(text):
    if 'https://t.co' in text:
        link_index = text.index('https://t.co')
        text = text[:link_index]
    if len(text) > 140:
        text = text[:140]
        if ' ' in text:
            for symbol in text[::-1]:
                if symbol == ' ':
                    index_of_first_space_in_returned_text = text[::-1].index(
                        symbol)
                    break
            index_of_last_space = len(
                text) - index_of_first_space_in_returned_text
            text = text[:index_of_last_space]
        text = text[:140] + ' [...]'
    return text


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

last_tweet_id = 0

while True:
    tweet_id = 0

    response = requests.get(
        'https://api.twitter.com/2/users/{}/tweets?max_results=5'.format(
            twitter_userid),
        headers={'Authorization': 'Bearer {}'.format(twitter_token)})
    try:
        jsondata = response.json()
        tweet = jsondata['data'][0]
        text = format_tweet_text(tweet['text'])
        tweet_id = tweet['id']
        if tweet_id != last_tweet_id:
            print("Updating")
            img = Image.new('RGB', (256, 64), color=BACKGROUND_COLOR)

            d = ImageDraw.Draw(img)
            d.text((4, 4), textwrap.fill(text.encode(
                'latin-1', 'ignore').decode(), width=42), fill=TEXT_COLOR)

            if not os.path.exists(STATIC_FOLDER):
                os.makedirs(STATIC_FOLDER)

            img.save('./{}/{}.png'.format(STATIC_FOLDER, tweet_id))
            update_object_image(gather_map_id, gather_object_name,
                            '{}/{}.png'.format(domain, tweet_id))

            last_tweet_id = tweet_id
    except:
        print('Could not update tweet')


    sleep(60)
