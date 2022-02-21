import configparser

config = configparser.RawConfigParser()
config.read("config.ini")

domain = config["GLOBAL"]["DOMAIN"]
twitter_token = config["TWITTER"]["TOKEN"]
twitter_userid = config["TWITTER"]["USERID"]
gather_api_key = config["GATHER"]["API_KEY"]
gather_space_id = config["GATHER"]["SPACE_ID"]
gather_map_id = config["GATHER"]["MAP_ID"]
gather_object_name = config["GATHER"]["OBJECT_NAME"]
