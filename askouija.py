import discord
import json
import traceback
from discord.ext import commands

#CHANGE, DO NOT SHARE
token = "token"

#other params
prefix = "Ouija, "
game = discord.Game("\"Ouija, help\" on #AskOuija")
channel = "ask-ouija"

#commands
help= "help"
question= "question"
goodbye= "goodbye"
reset= "reset"


#messages (some don't actually do anything, check below for more info)
msg_welcome = "*AskOuija bot has been added successfully!!!*"
msg_restart = "*AskOuija bot is back online.*"
msg_help = "Find out more on http://reddit.com/r/AskOuija\n\n__HOW TO DO IT:__\n\n1. Ask a question (start it with `Ouija, `) and have it answered by Ouija. \n2. To help answer a question, send a 1 letter response.\n3. `Goodbye` to end the response. \nIf you are the creator of the question or an admin, you can use `Ouija, reset` to stop answering."
msg_question = "The question, asked by {}, was: \n\n`{}`."
msg_noQuestion = "There is currently no question being asked. Ask a question by starting it with `Ouija, `, followed by your question."
msg_answer = "\n\nThe answer is: \n\n`{}`"
msg_reset = "\n\nThe question was reset."
msg_ownermessage = "Hello. This is the OuijaBot that was recently added onto {}. \n\nI am sending this message to inform you, the owner, that the channel `#AskOuija` has not been created. \n\nI only function in that channel, so please create one named `#AskOuija` or kick me from the server. \n\nAlso, if not done so already, be sure to give me permissions to send and read messages, as well as delete them. Thanks!"
msg_error = "Uh oh! there was a problem in processing the last message. Nothing has been changed; if there is an issue, ask an admin to use `Ouija, reset`."
bot = discord.Client()
users, questions, answers, guilds, askingQuestion, prevUser = [], [], [], [], [], []


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=game)

@bot.event
#joins a guild, checks if channel #askouija exists, if it doesn't then message mod or something
async def on_guild_join(guild):
    global msg_ownermessage
    print("new guild joined!")
    for x in guild.text_channels:
        if x.name is channel: 
            return
    await guild.owner.send(msg_ownermessage.format(guild.name))


@bot.event
async def on_message(message):
    global msg_question
    global msg_noQuestion
    global msg_answer
    global msg_reset
    global msg_help
    global help
    global question
    global reset
    global noQuestion
    global msg_error
    if not message.guild in guilds:
        guilds.append(message.guild)
        answers.append("")
        questions.append("")
        askingQuestion.append(False)
        users.append(message.author)
        prevUser.append("")
    index = guilds.index(message.guild)
    try:
        if  not (message.channel.name == channel):
            return
    except: 
        return
    if(message.author.id == bot.user.id):
        return
    try:
        if askingQuestion[index] == False:
            if(prefix in message.content and message.content.index(prefix) == 0):
                if(message.content[len(prefix) : len(message.content)].lower() == help):
                    await message.author.send(msg_help)
                    await message.delete()
                    return
                
                elif(message.content[len(prefix) : len(message.content)].lower() == question):
                    await message.author.send(msg_noQuestion)
                    await message.delete()
                    return
                
                elif(message.content[len(prefix) : len(message.content)].lower() == reset):
                    await message.author.send(msg_noQuestion)
                    await message.delete()
                    return
                else:
                    questions[index] = message.content[len(prefix) : len(message.content)]
                    users[index] = message.author
                    askingQuestion[index] = True
                    await message.channel.send(msg_question.format(users[index].mention, questions[index]))
                    return
        else:
            if((prefix in message.content) and message.content.index(prefix) == 0):
                if(message.content[len(prefix) : len(message.content)].lower() == msg_question):
                    await message.author.send(msg_question.format(users[index].mention, questions[index]))
                    await message.delete()
                    return
                elif(message.content[len(prefix) : len(message.content)].lower() == help):
                    await message.author.send(msg_help)
                    await message.delete()
                    return
                elif (message.content[len(prefix) : len(message.content)].lower() == reset and (message.author.top_role.permissions.administrator or message.author == users[index])):
                    askingQuestion[index] = False
                    await message.channel.send(msg_question.format(users[index].mention, questions[index]) + msg_reset)
                    questions[index] = ""
                    answers[index] = ""
                    users[index] = ""
                    prevUser[index] = ""
                    return
                else:
                    await message.delete()
                    return
            elif(message.author == users[index] or message.author == prevUser[index] or ( "<@!" + str(message.author.id) + ">") in questions[index]) :
                await message.delete()
                return
            elif(len(message.content[0]) > 255):
                answers[index] += message.content
                prevUser[index] = message.author
                return
            elif(message.content.lower() == goodbye):
                askingQuestion[index] = False
                await message.channel.send(msg_question.format(users[index].mention, questions[index]) + msg_answer.format(answers[index]))
                questions[index] = ""
                answers[index] = ""
                users[index] = ""
                prevUser[index] = ""
                return
            elif (len(message.content) > 1):
                await message.delete()
                return
            else:
                answers[index] += message.content
                prevUser[index] = message.author
                return
    except Exception as e:
        traceback.print_exc()
        print(e)
        await message.channel.send(msg_error)
        return
bot.run(token)