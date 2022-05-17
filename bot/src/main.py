from unicodedata import name
import discord #importamos para conectarnos con el bot
from discord.ext import commands #importamos los comandos
import datetime
import train_chatbot
import chat
import admin

client = commands.Bot(command_prefix='!', description="this is a testing bot")

#Ping-pong
@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command()
async def talk(ctx, *question):
    str = ' '.join(question)
    print(question)
    await ctx.send(chat.chatbot_response(str))

@client.command()
async def train(ctx, cantidad:int):
    history = train_chatbot.trainBot(cantidad)
    chat.load()
    loss = history['loss']
    accuracy = history['accuracy']
    for id  in range(cantidad):
        string = 'epoch: ' + str(id+1) + '/' + str(cantidad) + '\n\tloss: ' + str(loss[id]) + '\n\taccuracy: ' + str(accuracy[id])
        await ctx.send(string)
    await ctx.send('>TRAINING FINALIZADO!')

@client.command(name='add')
async def admin_intent(ctx, tag, pattern, response):
    admin.agregar_nuevo_intent(tag, pattern, response)
    await ctx.send('Intent Agregado con Exito')

@client.command()
async def tags(ctx):
    await ctx.send(admin.get_tags())

@client.command()
async def infotag(ctx, tag):
    await ctx.send(admin.get_responses_and_patterns(tag))

@client.command()
async def ayuda(ctx):
    des = """
    Comandos de TestBot\n

    > ping: El bot te responde pong

    > talk <parameters>: El bot te responde con información aprendida

    > train <numero>: El bot entrega con una cantidad de aproach dada por el numero

    > add <tag> <"pattern"> <"response">: El bot agrega un intent con tag patter y response (colocar entre comillas si son más de dos palabras)

    > tags: El bot responde con los tags existentes

    > infotag <tag>: El bot responde con los patterns y response del tag proporcionado

    > Prefix:  !\n
    Hecho con esfuezo en Python\n

    """
    embed = discord.Embed(title="I'm Isma Bot",url="https://www.facebook.com/profile.php?id=100010464276656",description= des,
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.blue())
    embed.set_footer(text="solicitado por: {}".format(ctx.author.name))
    embed.set_author(name="Bryan, Sergio y Mario",       
    icon_url="https://scontent.fgua10-1.fna.fbcdn.net/v/t1.6435-1/176055185_1367928206899309_7650928260753548797_n.jpg?stp=dst-jpg_p320x320&_nc_cat=111&ccb=1-6&_nc_sid=7206a8&_nc_ohc=-BdGYs-roPcAX-6HIp5&_nc_ht=scontent.fgua10-1.fna&oh=00_AT-dQfMR85Y-3EEGgsAmNOaMNhWRntkbXdXFh6WAoaZyOw&oe=62A8D755")
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    train_chatbot.trainBot(200)
    chat.load()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="tik tok"))
    print('My bot is ready')

client.run('OTc1MTYzMzI1MjI0NzE0MzMw.GeBj1D.XqYHXw54HJwWLfmELmzrathTdzVKIN6cHcO57s')