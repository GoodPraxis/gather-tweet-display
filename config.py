import configparser

config = configparser.RawConfigParser()
config.read("config.ini")

twitter_token = config["TWITTER"]["TOKEN"]
twitter_userid = config["TWITTER"]["USERID"]
gather_api_key = config["GATHER"]["API_KEY"]
gather_space_id = config["GATHER"]["SPACE_ID"]
