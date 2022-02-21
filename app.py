import requests
import textwrap
from PIL import Image, ImageDraw
from config import twitter_token, twitter_userid

BACKGROUND_COLOR = (16, 16, 16)
TEXT_COLOR = (251, 224, 114)


response = requests.get(
  'https://api.twitter.com/2/users/{}/tweets?max_results=5'.format(twitter_userid),
  headers={'Authorization': 'Bearer {}'.format(twitter_token)})
try:
  json = response.json()
  text = json['data'][0]['text']
  img = Image.new('RGB', (256, 64), color = BACKGROUND_COLOR)

  d = ImageDraw.Draw(img)
  d.text((4,4), textwrap.fill(text, width = 42), fill = TEXT_COLOR)

  img.save('tweet.png')
except:
  print('Could not retrieve tweet')
