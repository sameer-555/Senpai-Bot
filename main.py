import discord
import os
import requests
import re
from keep_alive import keep_alive

client = discord.Client()

def get_ip_location(ip):
  response = requests.get("https://freegeoip.app/json/{}".format(ip))
  return response.json()

def get_jokes():
  response = requests.get("https://official-joke-api.appspot.com/jokes/random")
  return response.json()['setup'],response.json()['punchline']

@client.event
async def on_ready():
  print("We are using {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith("$hello"):
    await message.channel.send("hello {0}!".format(message.author))

  if message.content.startswith("$joke"):
    setup, punchline = get_jokes()
    joke = """{0}
    ...
    {1}
    """.format(setup,punchline)
    await message.channel.send(joke)

  if message.content.startswith("$findip"):
    ip = message.content.split("$findip ",1)[1].strip()
    if re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip):
      try:
        location = get_ip_location(ip)
        country_code = location['country_code']
        country_name = location['country_name']
        region_name = location['region_name']
        city = location['city']
        zipcode = location['zip_code']
        latitude = location['latitude']
        longitude = location['longitude']

        address = """Country Code : {0}
Country Name : {1}
Region Name  : {2} 
City         : {3} 
Zipcode      : {4} 
Latitude     : {5} 
Longitude    : {6}
        """.format(country_code,country_name,region_name,city,zipcode,latitude,longitude)
        await message.channel.send(address)
      except:
        await message.channel.send("make sure ip is in valid format")
    else:
      await message.channel.send("make sure ip is valid kid.")

  if message.content.startswith("$senpai?"):
    await message.channel.send("i can do :- $hello, $findip, $joke")
keep_alive()
client.run(os.getenv('TOKEN'))