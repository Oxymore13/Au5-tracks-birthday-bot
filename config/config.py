import json

class Config():
    # I defined them here so the IDE proposes them to me for auto completion
    token = str()
    channel = int()
    embed_color = 0xFFFFFF
    calendarId = str()

    test_channel = int()

    def __init__(self) :
        with open('config/botConfig.json','r') as f:
            config_file = json.load(f)

            self.channel = config_file['channel']
            self.embed_color = 0xFFFFFF
            self.token = config_file['botToken']
            self.calendarId = config_file['calendarId']

try :
    config = Config()
except Exception as e :
    print("Exception on config : \n\n",e)
    exit()