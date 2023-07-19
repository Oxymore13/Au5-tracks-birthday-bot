
#----------------------------------------------------------------------------------------------------
# CREDITS :
#
# Discord bot made by Oxymore
# Calendar checker library made by Krohne
# Google calendar made by Norhkuna
#----------------------------------------------------------------------------------------------------

## I sometimes get errors on the imports so this makes sure the window doesn't close before I can see what happened
try :
    from datetime import datetime
    import discord
    from discord import app_commands
    from discord.ext import commands, tasks
    import os

    from config import config
    from birthday import CalendarChecker, get_date_string_from_event
except Exception as e :
    print("Exception during imports :\n\n",e)
    input()
    exit()


## When the token is wrong removing it can solve the issue
try :
    checker = CalendarChecker(config.calendarId)
except Exception as e :
    if os.path.exists("token.pickle") :
        os.remove("token.pickle")
        try :
            checker = CalendarChecker(config.calendarId)
        except Exception as e :
            print("Exception on calendar_checker :\n\n",e)
            input()
            exit()
    else :
        print("Exception on calendar_checker :\n\n",e)
        input()
        exit()





#----------------------------------------------------------------------------------------------------
# TOOLS
#----------------------------------------------------------------------------------------------------


## Thanks papa GPT
def levenshtein_distance(str1, str2):
    # Create a matrix with dimensions (len(str1) + 1) x (len(str2) + 1)
    rows = len(str1) + 1
    cols = len(str2) + 1
    matrix = [[0] * cols for _ in range(rows)]

    # Initialize the first row and column of the matrix
    for i in range(rows):
        matrix[i][0] = i
    for j in range(cols):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, rows):
        for j in range(1, cols):
            if str1[i - 1] == str2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1,      # deletion
                               matrix[i][j - 1] + 1,      # insertion
                               matrix[i - 1][j - 1] + substitution_cost)  # substitution

    return matrix[rows - 1][cols - 1]





#----------------------------------------------------------------------------------------------------
# BOT
#----------------------------------------------------------------------------------------------------


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

## Checking daily if there's a birthday
@tasks.loop(hours=24)
async def daily_check():
    events = checker.get_event_for_date(datetime.utcnow())
    
    if not events :
        print("no event today !")
        return
    
    for event in events :
        
        event_name = event['summary']
        title = f"Today is {event_name}'s brithday !"
        
        if "recurringEventId" in event :
            original_date_string = get_date_string_from_event(checker.get_original_event_from_recurring_event(event))
            description = f"released on {original_date_string}"
            await bot.get_channel(config.test_channel).send(embed=discord.Embed(title=title, description=description, color=config.embed_color))
        else :
            await bot.get_channel(config.test_channel).send(embed=discord.Embed(title=title, color=config.embed_color))
    

## Startup event
@bot.event
async def on_ready():
    if not daily_check.is_running() :
        daily_check.start()

    try :
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e :
        print(e)

    print("The bot is ready !")





#----------------------------------------------------------------------------------------------------
# COMMANDS
#----------------------------------------------------------------------------------------------------


## Ping command
@bot.tree.command(name = "ping")
async def ping(interaction:discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Pong !", description=f"The ping is {int(bot.latency*1000)}ms"))

## This command displays the release date of the requested track
@bot.tree.command(name = "birthday")
@app_commands.describe(track_name = "The name of the track you're looking for")
async def birthday(interaction:discord.Interaction, track_name:str):

    ## Finding the event
    events = checker.get_all_source_events()
    date_string = None
    closest = None
    min_dist = 99999

    for event in events:
        event_name = event['summary']
        dist = levenshtein_distance(event_name, track_name)
    
        if dist == 0 :
            date_string = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).strftime('%A, %d. %B %Y')
            break
    
        if dist < min_dist :
            min_dist = dist
            closest = event_name


    ## User has skill issue 
    if not date_string :
        msg = f"I'm sorry, I couldn't find *`{track_name}`*."
        if closest :
            msg += f" Did you mean ***`{closest}`*** ?"
        await interaction.response.send_message(msg)
        return

    await interaction.response.send_message(f"{track_name} was released on {date_string}")


## Running the bot
if __name__ == '__main__':
    bot.run(config.token)