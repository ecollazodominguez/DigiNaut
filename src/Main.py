import discord
import random
from discord.ext import commands
from cogs.ImageGallery import ImageGallery
from cogs.MiniGames import MiniGames
from Utils import Utils



#Prefijo para los comandos
bot = commands.Bot(command_prefix='!')
bot.add_cog(ImageGallery(bot))
bot.add_cog(MiniGames(bot))

utils = Utils()
@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))
@bot.event
#Detecta el mensaje y actua segun lo que trate
async def on_message(message):
	#Canal "General"
	channel = bot.get_channel(753156816438951940)
	#Cogemos contexto
	ctx = await bot.get_context(message)
	if message.author == bot.user:
		return

	if message.content.lower().startswith('Hello'):
		await message.add_reaction('💩') # :poop:
	if message.content.lower().startswith('Loli'):
		await message.add_reaction('🍭') # :lollipop:
	if message.content.lower().startswith('lua'):
		#Recogemos la mención del rol en concreto
		mentions = [role.mention for role in ctx.guild.roles if role.name == "Princesa"]
		await channel.send(mentions[0] +' de mi corazón <3')
	await bot.process_commands(message)

@bot.command()
async def dados(ctx,cara=0,tiradas=0,bonificacion=0):
#TODO: poner imagenes correspondiente a el resultado?

	#Si no se recibe cara se pasa por el if
	if cara == 0:
		await ctx.send("""```Elige el número de caras```""")
		msg = (await bot.wait_for('message', check=utils.check(ctx.author), timeout=5000)).content
		cara = int(msg)
			
		await ctx.send("""```Elige el número de tiradas```""")
		msg = (await bot.wait_for('message', check=utils.check(ctx.author), timeout=5000)).content
		tiradas = int(msg)

		
		await ctx.send("""```Elige el número de bonificación```""")
		msg = (await bot.wait_for('message', check=utils.check(ctx.author), timeout=5000)).content
		bonificacion = int(msg)
	
	#Si son 0 se cambian a 1
	if cara == 0:
		cara = 1
	if tiradas == 0:
		tiradas = 1	
	embed=discord.Embed(color=0xff7700)
	embed.add_field(name=f"Tirando un dado de {cara} cara(s) {tiradas} vez(ces) con una bonificación de +{bonificacion}.", value="...", inline=True)
	await ctx.send(embed=embed)
	
	#Calculamos
	for i in range(tiradas):
		resDado = random.randint(1,cara)
		embed=discord.Embed(color=0xff7700)
		if cara == 6:
			embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/mario/images/0/0c/MP9_4_5_6_Dice_Block.png/revision/latest?cb=20190418033833")
		embed.add_field(name=f"""Tirada {i+1}:""",value=f"""```{resDado} + {bonificacion} = {resDado+bonificacion}```""")
		await ctx.send(embed=embed)
		
	
#TODO: comando minijuegos tipo "adivina el numero", "tres en raya..."

token = open('../token.txt', "r")
bot.run(token.read())	
token.close()