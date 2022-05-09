import discord
import uberduck as ud
import time
import os
import asyncio 

client = discord.Client()
loop = asyncio.get_event_loop()
queue = asyncio.Queue()
ready = True

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
       
    if message.author == client.user or message.content.strip() == '!jerry':
        print('no message')
        return
    
    await queue.put(message)
    while not client.is_ready:
        await asyncio.sleep(1)
    client.is_ready = False
    loop.create_task(play_audio())
    
        



async def play_audio():    
    print('playaudio started')
    
    message = await queue.get()
    words = message.content.replace('!jerry', '').strip()
    user = message.author
    if message.content.startswith('!jerry') and user.voice is not None: 
        
        voicechannel = user.voice.channel
        audio = ud.get_audio(words)
        path = 'results/audio.wav'

        if audio == 'success':
            await asyncio.sleep(2)
            vc = await voicechannel.connect()
            await asyncio.sleep(2)
            vc.play(discord.FFmpegPCMAudio(path))
            while vc.is_playing():
                await asyncio.sleep(2)
            await vc.disconnect()
                
                
        else:
            await message.channel.send('Unable to retrieve voice. Try again')
    else:
        await message.channel.send('Join a voice channel and try again')
    client.is_ready= True
 

if __name__=='__main__':
    my_secret = 'OTcyNDYzMjc3ODM1NzA2Mzk4.YnZbAA.dKWDQlMY3MKBoQZ7-D_pNecHpx4'
      
    client.run(my_secret)
    
    