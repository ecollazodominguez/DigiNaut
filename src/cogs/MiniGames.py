import discord
import os
import random
from discord.ext import commands
import json
from Utils import Utils

if not os.path.exists("cogs/animeTrivia.json"):
    data = {}
    with open('cogs/animeTrivia.json', 'w') as outfile:
        json.dump(data, outfile)

class MiniGames(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        
    @commands.command()
    async def games(self,ctx, msg =""):
        #Si no indicamos el mensaje pasamos por el if
        if msg == "":
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="Elige una opción.", value="""```1 - Adivina el número
2 - Trivial (Anime)
3 - Trivial (Cultura general)
4 - Tres en raya```""", inline=False)
            await ctx.send(embed=embed)
            #Recibimos el mensaje de la persona especifica
            msg = (await self.bot.wait_for('message', check=self.utils.checkNumber(ctx.author), timeout=5000)).content
        if msg == "1" or msg.lower() == "adivina" or msg.lower() == "numero":
            await self.AdivNum(ctx)
            
        elif msg == "2" or msg.lower() == "anime" or msg.lower() == "trivialanime":
            await self.TrivAnime(ctx)
            
        elif msg == "3" or msg.lower() == "cultura" or msg.lower() == "trivial":
            await self.Trivial(ctx)
            
        elif msg == "4" or msg.lower() == "tres" or msg.lower() == "raya" or msg.lower() == "tresenraya":
            await self.TresEnRaya(ctx)
            
    async def AdivNum(self,ctx):
        embed=discord.Embed(color=0xff7700)
        embed.add_field(name="Has elegido adivina el número.", value="Tendrás que adivinar un número entre el 1 y el 100. Empezando el juego...", inline=False)
        await ctx.send(embed=embed)
        
        intentos = 5
        nCorrecto = random.randint(1,100)
        
        while intentos > 0:
            await ctx.send("```Elige un número```")
            msg = (await self.bot.wait_for('message', check= self.utils.checkNumber(ctx.author), timeout=5000)).content
            nJugador = int(msg)        
            
            diferencia = abs(nJugador-nCorrecto)
            intentos -=1
            
            if diferencia == 0:
                win = await ctx.send("🎉🎉 🎊 🎈¡¡Has acertado!!🎈🎊🎉🎉 ")
                await win.add_reaction('🎉') # \:tada:
                await win.add_reaction('🎊') # \:confetti_ball:
                await win.add_reaction('🎈') # \:balloon:
                intentos = -1
            elif diferencia <= 5:
                await ctx.send(f"""Dios, ¡Que te derrites!
Te quedan {intentos} intentos""")
            elif diferencia <= 10:
                await ctx.send(f"""Ay, ¡Que te quemas!
Te quedan {intentos} intentos""")
            elif diferencia <= 25:
                await ctx.send(f"""Caliente, caliente~                
Te quedan {intentos} intentos""")
            elif diferencia <= 50:
                await ctx.send(f"""Frío                
Te quedan {intentos} intentos""")
            else:
                await ctx.send(f"""Brrr... ¿No hace DEMASIADO frío aquí?              
Te quedan {intentos} intentos""")
                
        
        if intentos == 0:
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="Lo siento...", value=f"Has perdido, el número era {nCorrecto}. vuelve a intentarlo.", inline=False)
            await ctx.send(embed=embed)
            
            
    async def TrivAnime(self,ctx):
        embed=discord.Embed(color=0xff7700)
        embed.add_field(name="Has elegido trivial de anime.", value="Tendrás que responder 5 preguntas para ganar. Empezando el juego...", inline=False)
        await ctx.send(embed=embed)
        
        preguntas = 1
        bien = 0
        mal = 0
        while preguntas <6:
            pregunta, rCorrecta, listaR, disposicion = self.loadQuestions("cogs/animeTrivia.json")
        
            if disposicion == 1:
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {rCorrecta}
- {listaR[0]}
- {listaR[1]}
- {listaR[2]}```""", inline=False)
                await ctx.send(embed=embed)
            elif disposicion == 2:
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {listaR[0]}
- {rCorrecta}
- {listaR[2]}
- {listaR[1]}```""", inline=False)
                await ctx.send(embed=embed)
            elif disposicion == 2:
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {listaR[1]}
- {listaR[2]}
- {rCorrecta}
- {listaR[0]}```""", inline=False)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {listaR[2]}
- {listaR[1]}
- {listaR[0]}
- {rCorrecta}```""", inline=False)
                await ctx.send(embed=embed)
        
            preguntas += 1
            
            msg = (await self.bot.wait_for('message', check= self.utils.check(ctx.author), timeout=5000)).content
            if rCorrecta.lower() == msg.lower():
                bien+=1
                b = await ctx.send("Correcto.")
                await b.add_reaction('💯') # \:100:
            else:
                mal+=1
                m = await ctx.send(f"Incorrecto, la respuesta era ```{rCorrecta}.```")
                await m.add_reaction('💩') # \:poop:
                
        await self.checkResults(ctx, bien, mal)
        
    
    async def Trivial(self,ctx):
        pass
    
    async def TresEnRaya(self,ctx):
        pass
    
            
    def loadJson(self,path):
        #Carga los datos del Json
        if os.path.exists(path):
            with open(path, encoding='utf-8-sig') as json_file:
                data = json.load(json_file)
        return data           
            
    def loadQuestions(self,path):
        jsonData = self.loadJson(path)
        #Pregunta
        nPregunta= str(random.randint(1,len(jsonData)))
        pregunta = jsonData.get(nPregunta)["P"]
        #Respuesta correcta
        rCorrecta = jsonData.get(nPregunta)["Rc"]
        #Respuestas incorrectas
        listaR=[]
        listaR.append(jsonData.get(nPregunta)["R2"])
        listaR.append(jsonData.get(nPregunta)["R3"])
        listaR.append(jsonData.get(nPregunta)["R4"])
        #Disposición de las preguntas
        disposicion = random.randint(1,4)
        
        return pregunta, rCorrecta, listaR, disposicion
        
        
    async def checkResults(self,ctx,bien,mal):
        if bien == 5:
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="¡Enhorabuena, un pleno!", value=f"```{bien} correctas | {mal} incorrectas```", inline=False)
            p = await ctx.send(embed=embed)
            await p.add_reaction('🎉') # \:tada:
            await p.add_reaction('🎊') # \:confetti_ball:
            await p.add_reaction('🎈') # \:balloon:
        else:
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="Has conseguido una puntuación de:", value=f"```{bien} correctas | {mal} incorrectas```", inline=False)
            await ctx.send(embed=embed)        
            
            
            
            
            
            
            
            
            