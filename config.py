



class Config():
    # I defined them here so the IDE proposes them to me for auto completion
    token = str()
    channel = int()
    embed_color = 0xFFFFFF
    calendarId = str()

    test_channel = int()

    def __init__(self) :
        self.channel = 581198974917279755
        self.embed_color = 0xFFFFFF
                
        with open('botToken','r') as f :
            self.token = f.read()

        with open('calendarid','r') as f :
            self.calendarId = f.read()


try :
    config = Config()
except Exception as e :
    print("Exception on config : \n\n",e)
    input()
    exit()