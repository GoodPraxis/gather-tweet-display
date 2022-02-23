Gather Tweet Display
====================

This is a simple script used to display the latest Tweet from a given account in
[Gather Town](https://gather.town). The script generates an image for the tweet
and displays it on a given map.

This script assumes that you are able to serve the generated images on a web
server you own.

Setup
-----
Clone or download the repo.

Install python dependencies

    pip install -r requirements.txt

Make a copy of the `config.ini.example` file to create `config.ini`

    cp config.ini.example config.ini

Fill in all the fields:

* `DOMAIN` specifies the domain at which the images will be served
* `TOKEN` is your Twitter [app only Bearer Token](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens)
* `USERID` is the ID of the target Twitter user
* `API_KEY` is your [Gather API key](https://help.gathercontent.com/en/articles/369871-generating-an-api-key-the-api-documentation)
* `SPACE_ID` is your Gather Space ID
* `OBJECT_NAME` is the name of the object which will be updated on the map
* `MAP_ID` is the id of the Gather map

In Gather, create a new object with a name set to the `OBJECT_NAME` value you
have (e.g. `tweetd`).

Now setup a web server to host the generated images under `DOMAIN`. Make sure
you set an `Access-Control-Allow-Origin` header to either a wildcard `*` or to
`https://gather.town`. The generated images will be in a folder called `static`.

Finally, run `app.py` either in a `screen` or as a service.
