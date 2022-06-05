import nextcord
from nextcord.ext import commands
import random
import requests
import re

#General commands live here.
class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
                    
        #Read in civil engineering insults. Nothing against civEs, this was made to poke fun at a friend.
        self.civsults = open("src/civil_insult.txt","r").readlines()

        #Read in Kevin quotes.
        #Maybe TODO: Make it so this can be dynamically updated, whether that is through Google Docs or putting this in a place where it refreshes or is read more often.
        with open("src/kevin.txt") as f:
            self.quotes = f.readlines()

    #This listener will wait until someone is talking about civil engineering and then insult them.
    @commands.Cog.listener()
    async def on_message(self, message):

        #Avoid the bot responding to itself or other bots.
        if message.author.bot: 
            return

        #If somone mentions civil engineers, do a thing. .lowercase makes things easy to deal with and case insensitive.
        if re.search(r'civils?|cives?\b|civies?\b|civys?\b', message.content.lower()):

            #Pick a random insult.
            await message.channel.send(random.choice(self.civsults))

    commands.group(name="General fun commands")

    #This command gives a random Kevin quote.
    @commands.command(name="kevin")
    async def kevin(self, ctx):
        """Supplies a quote from our benevolent overlord."""
        
        #Send a random Kevin quote.
        await ctx.send(random.choice(self.quotes))

    #Send a random top article from HackerNews.
    @commands.command(name="news")
    async def news(self, ctx):
        """Fetches a top story from Y Combinator's HackerNews."""

        #Get the IDs of all the top stories at the time.
        stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()

        #Get call the API to get the data on a random story.
        newsurl = "https://hacker-news.firebaseio.com/v0/item/{}.json".format(random.choice(stories))

        #Grab the URL for the story and send it!
        news = requests.get(newsurl).json()['url']
        await ctx.send(news)

    #Basic Cowsay.
    @commands.command(name="cowsay")
    async def cowsay(self, ctx):
        """Get a friendly cow to saw whatever your heart desires."""
        #Strip off command prefix.
        text = ctx.message.content.replace("&cowsay ",'')
        
        #Generate the top and bottom length for the speech bubble.
        edge = '-' * len(text)

        #Cow template. Will be formatted with message.
        cow = """
 -{}- 
< {} >
 -{}-
      \   ^__^
       \  (oo)\_______
          (__)\       )\/\\
              ||----w |
              ||     ||""".format(edge,text,edge)

        #Format message as code block to preserve formatting.
        await ctx.send("```{}```".format(cow))
