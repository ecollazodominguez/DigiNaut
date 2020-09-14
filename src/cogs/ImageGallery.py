import discord
import os
import random
from discord.ext import commands
import json
from datetime import datetime
from Utils import Utils

#Si no existe el json lo crea
if not os.path.exists("cogs/dataImage.json"):
    data = {}
    with open('cogs/dataImage.json', 'w') as outfile:
        json.dump(data, outfile)

class ImageGallery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
    

    @commands.command()
    async def images(self,ctx, msg =""):
        #Cogemos el canal que enviaremos los mensajes
        #channel = bot.get_channel(753156816438951940)
        #Configurando formato de fecha
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y")
        #Cargamos el Json con las imagenes
        dataJson= self.loadJson()
        #Asignamos la ruta donde está las imagenes
        imageFolder= "D:\Edu\CARPETA DE LUA"
        #Recogemos todas las imagenes de la carpeta y la metemos en una lista
        img_list = os.listdir(imageFolder)
        #Si no indicamos el mensaje pasamos por el if
        if msg == "":
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="Elige una opción.", value="""```1 - Imágenes nuevas
2 - Imágenes del día
3 - Imagen aleatoria
4 - Selección de imagen```""", inline=False)
            await ctx.send(embed=embed)
            #Recibimos el mensaje de la persona especifica
            msg = (await self.bot.wait_for('message', check=self.utils.check(ctx.author), timeout=5000)).content
        if msg == "1" or msg.lower() == "new" or msg.lower() == "nuevo" or msg.lower() == "nuevas":
            await self.newImages(ctx,dataJson,imageFolder,img_list,date_time)
            
        elif msg == "2" or msg.lower() == "dia" or msg.lower() == "día" or msg.lower() == "today":
            await self.todayImages(ctx,dataJson,imageFolder,date_time)
            
        elif msg == "3" or msg.lower() == "aleatoria" or msg.lower() == "random":
            img = img_list[random.randint(0,len(img_list)-1)]
            embed = self.imgEmbed(img, footer="Imagen aleatoria")
            await ctx.send(file=discord.File(imageFolder+ "/"+img), embed=embed)
            
        elif msg == "4" or msg.lower() == "selección" or msg.lower() == "seleccion" or msg.lower() == "seleccionar":
            await self.selectImages(ctx, imageFolder, img_list)
    
    async def newImages(self,ctx,dataJson,imageFolder,img_list,date_time):
        #Inicializamos una variable donde guardaremos las imagenes nuevas
        jsonImages=[]
        #Recorremos los datos del Json para recoger la ruta de las imagenes y las guardamos en una lista
        for image in dataJson.values():
            jsonImages.append(image['ruta'])
        #Comparamos las imagenes de la carpeta con las del json para encontrar diferencias
        newImg = list(set(img_list) - set(jsonImages))
        #Si encontramos minimo 1 diferencia procedemos
        if len(newImg) >=1:
            #Recorremos la lista de las diferencias y las mostramos en discord además de decir la cantidad
            for image in newImg:
                    embed = self.imgEmbed(image, footer="Imagen nueva")
                    await ctx.send(file=discord.File(imageFolder+ "/"+image),embed=embed)
            await ctx.send("```Aquí tienes "+str(len(newImg))+" imágenes nuevas.```")
            #Guardamos las nuevas imagenes en el Json
            self.saveJson(dataJson,newImg,date_time)
        else:
            img = img_list[random.randint(0,len(img_list)-1)]
            embed = self.imgEmbed(img, footer="Imagen aleatoria")
            await ctx.send(file=discord.File(imageFolder+ "/"+img), embed=embed)
            await ctx.send("```No hay ninguna imagen nueva, pero como quieres una... ¡Aquí tienes!```")
            
    async def todayImages(self,ctx,dataJson,imageFolder,date_time):
        #Buscamos las imagenes añadidas a dia de hoy
            todayImages = []
            todayImages = self.searchTodayImg(dataJson,date_time)
            #Si no hay, se indica
            if todayImages == []:
                await ctx.send("```No hay imágenes del día.```")
            else:
            #Si hay, las mostramos
                for image in todayImages:
                    try:
                        embed = self.imgEmbed(image, footer="Imagen del día.")
                        await ctx.send(file=discord.File(imageFolder+ "/"+image),embed=embed)                    
                    except:
                        self.deleteJson(dataJson,image)
                await ctx.send("```Aquí tienes las imágenes del día.```")
                
    async def selectImages(self,ctx,imageFolder,img_list):
        #Preguntamos por numero
        await ctx.send(f"```Selecciona un número entre el 1 y {len(img_list)}.```")
        #Lo recogemos
        msg = (await self.bot.wait_for('message', check= self.utils.check(ctx.author), timeout=5000)).content
        number = int(msg)
        #Comparamos y mostramos
        if number >=1 and number <= len(img_list):
            embed = self.imgEmbed(img_list[number-1], footer=f"Imagen número {number}")
            await ctx.send(file=discord.File(imageFolder+ "/"+img_list[number-1]),embed=embed)
        else:
            #Si escribe mal, insiste
            return await self.selectImages(ctx,imageFolder,img_list)
        
    def deleteJson(self,jsonData,image):
        #Elimina la imagen que ya no existe en el directorio.
        
        #Hacemos una copia del json para poder manipularlo
        copiaJson= jsonData.copy()
        
        #Accedemos a las keys y los values
        for key, values in copiaJson.items():
            #Buscamos que la ruta sea la misma que la imagen
            if values['ruta'] == image:
                #Eliminamos la entrada usando la key
                print(jsonData.pop(key))
                
                #Usamos la ultima entrada para rellenar ese hueco vacio
                print (jsonData.setdefault(key, jsonData.get(str(len(jsonData)+1))))
                #Eliminamos la última entrada al estar ya cambiado
                jsonData.pop(str(len(jsonData)))
        
        
        with open('cogs/dataImage.json', 'w') as outfile:
            json.dump(jsonData, outfile)
                    
        print("Eliminado y añadido")
    
    def saveJson(self,jsonData,newImages,date_time):
        #Guarda los datos en el Json. {numero:{ruta:x,fecha:y}}
        for image in newImages:
            jsonData[str(1+len(jsonData))] = {
            'ruta': image,
            'fecha': date_time
            }
    
        with open('cogs/dataImage.json', 'w') as outfile:
            json.dump(jsonData, outfile, indent=2)
    
    def loadJson(self):
        #Carga los datos del Json
        if os.path.exists("cogs/dataImage.json"):
            with open('cogs/dataImage.json', 'r') as json_file:
                data = json.load(json_file)
        return data
    
    def searchTodayImg(self,jsonData,date_time):
        #Busca si hay imagenes del dia de hoy
        newImages=[]
        for image in jsonData.values():
            if image['fecha'] == date_time:
                newImages.append(image['ruta'])
        return newImages
    
    def imgEmbed(self,img,footer):
        #Incorporamos la imagen a un recuadro de texto
        embed = discord.Embed(color=0xff7700)
        embed.set_image(url="attachment://"+img)
        embed.set_footer(text=footer)
        return embed