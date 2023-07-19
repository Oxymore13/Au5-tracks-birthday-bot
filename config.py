



class Config():
    # I defined them here so the IDE proposes them to me for auto completion
    token = str()
    channel = int()
    embed_color = 0xFFFFFF
    calendarId = str()

    test_channel = int()

    def __init__(self) :
        self.token = 'MTEyMTkwODAyNzcwNTAyMDUzNg.G6pyu1.AB4CJEE3Fq-BHGhkDqzk2OPrvQ3v9OqOKdb8RY'
        self.channel = 581198974917279755
        self.embed_color = 0xFFFFFF
        self.calendarId = 'konsta.pylkko@gmail.com'

        self.test_channel = 1121910774831513811

try :
    config = Config()
except Exception as e :
    print("Exception on config : \n\n",e)
    input()
    exit()