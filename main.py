#Libraries
import discord
import asyncio
import random
import requests
import io
import safygiphy

client = discord.Client()
Username = "User_ID" #You should write the ID and the name of the user who can change the bot's game information here.
minutes = 0 #Minutes variable for uptime command.
hour = 0 #Hour variable for uptime command.
g = safygiphy.Giphy()

#Console output
@client.event
async def on_ready():
    print('Connected')
    print(client.user.name)
    print(client.user.id)
    print('-----------')
    await client.change_presence(game=discord.Game(name="Hello World"))#Here you can write what you want to write in the game info when the bot is first active.

#Commands
@client.event
async def on_message(message):
    if message.content.lower().startswith('!hi'):
        await client.send_message(message.channel, "Hello")

    #Coinflip
    if message.content.lower().startswith('!coinflip'):
        choice = random.randint(1,2)
        if choice == 1:
            await client.add_reaction(message, '🌑')
        if choice == 2:
            await client.add_reaction(message, '🌕')

    #You can change bot's game info
    if message.content.startswith('!game') and message.author.id == User_ID:
        game = message.content[6:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Game info has been changed to "+game)

    #Send a picture
    if message.content.startswith('!pic'):
            response = requests.get("https://cdn.pixabay.com/photo/2017/04/11/21/34/giraffe-2222908_960_720.jpg",stream=True)
            await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='pic1.png',content='Test Pic')

    #uptime
    if message.content.startswith('!uptime'):
        await client.send_message(message.channel,"`This bot is {0} hours and {1} minutes active in {2} Server.`".format(hour, minutes,message.server))

    #Send random GIF' s from giphy.com
    if message.content.startswith('!gif'):
        gif_tag = message.content[5:]
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

    #Send random funny GIF' s from giphy.com
    if message.content.startswith('!fun'):
        gif_tag = "fun"
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

        # User Info's
        if message.content.startswith('!user'):
            try:
                user = message.mentions[0]
                userjoinedat = str(user.joined_at).split('.', 1)[0]
                usercreatedat = str(user.created_at).split('.', 1)[0]

                userembed = discord.Embed(
                    title="Username:",
                    description=user.name,
                    color=0xe67e22
                )
                userembed.set_author(
                    name="User Info"
                )
                userembed.add_field(
                    name="Joined the server at:",
                    value=userjoinedat
                )
                userembed.add_field(
                    name="User Created at:",
                    value=usercreatedat
                )
                userembed.add_field(
                    name="Discriminator:",
                    value=user.discriminator
                )
                userembed.add_field(
                    name="User ID:",
                    value=user.id
                )

                await client.send_message(message.channel, embed=userembed)
            except IndexError:
                await client.send_message(message.channel, "User cannot find.")
            except:
                await client.send_message(message.channel, "Sorry Error")
            finally:
                pass

    #Leave and join messages
    @client.event
    async def on_member_join(member):
        serverchannel = member.server.default_channel
        msg = "Welcome to {0} Server {1}".format(member.server.name, member.mention)
        await client.send_message(serverchannel, msg)

    @client.event
    async def on_member_remove(member):
        serverchannel = member.server.default_channel
        msg = "Bye Bye {0}".format(member.mention)
        await client.send_message(serverchannel, msg)

    #Timer for !uptime command
    async def tutorial_uptime():
        await client.wait_until_ready()
        global minutes
        minutes = 0
        global hour
        hour = 0
        while not client.is_closed:
            await asyncio.sleep(60)
            minutes += 1
            if minutes == 60:
                minutes = 0
                hour += 1
    client.loop.create_task(tutorial_uptime())

client.run('Your Token')
