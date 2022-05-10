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
    
    message = await queue.get()
    cmdkey = {
        '!jerry': 'jerry-lawler',
        '!sponge': 'spongebob', 
        '!hank': 'hank-hill', 
        '!nile':'nilered', 
        '!pstew':'patrickstewart',
        '!samj':'slj',
        '!norm':'norm-macdonald',
        '!arnold':'arnold-schwarzenegger',
        '!hal': 'hal-9000',
        '!gg': 'gottfried',
        '!vince':'vince-mcmahon',
        

        }
    voice = None
    words = ''
    command = message.content
    if '!' in command:
        command = command[command.index('!'):command.index(' ')].replace(' ', '')
        words = message.content.replace(command, '').strip()
        
    if command in cmdkey:
        voice = cmdkey[command]
    
    
    user = message.author
    if voice and user.voice is not None: 
        
        voicechannel = user.voice.channel
        audio = ud.get_audio(words, voice=voice)
        path = 'results/audio.wav'

        if audio == 'success':
            vc = await voicechannel.connect()
            await asyncio.sleep(2)
            vc.play(discord.FFmpegPCMAudio(path))
            while vc.is_playing():
                await asyncio.sleep(2)
            await vc.disconnect()
                
                
        else:
            await message.channel.send('Unable to retrieve voice. Try again')
    
    elif user.voice is None:
        await message.channel.send('Join a voice channel and try again')
    client.is_ready= True
 

if __name__=='__main__':
    my_secret = os.environ['token']
      
    client.run(my_secret)
    
    