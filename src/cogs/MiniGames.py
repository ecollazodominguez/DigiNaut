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
        
        intentos = 5 # intentos
        nCorrecto = random.randint(1,100) # numero a acertar
        
        while intentos > 0:
            #mientras tengas intentos puedes adivinar el numero
            await ctx.send("```Elige un número```")
            msg = (await self.bot.wait_for('message', check= self.utils.checkNumber(ctx.author), timeout=5000)).content
            nJugador = int(msg)        
            
            diferencia = abs(nJugador-nCorrecto) #Diferencia entre el numero a acertar y el que el jugador dice
            intentos -=1
            
            if diferencia == 0:
                #Ganas
                win = await ctx.send("🎉🎉 🎊 🎈¡¡Has acertado!!🎈🎊🎉🎉 ")
                await win.add_reaction('🎉') # \:tada:
                await win.add_reaction('🎊') # \:confetti_ball:
                await win.add_reaction('🎈') # \:balloon:
                intentos = -1
            elif diferencia <= 5:
                #Muy cerca
                await ctx.send(f"""Dios, ¡Que te derrites!
Te quedan {intentos} intentos""")
            elif diferencia <= 10:
                #Cerca
                await ctx.send(f"""Ay, ¡Que te quemas!
Te quedan {intentos} intentos""")
            elif diferencia <= 25:
                #Cerquita
                await ctx.send(f"""Caliente, caliente~                
Te quedan {intentos} intentos""")
            elif diferencia <= 50:
                #Lejos
                await ctx.send(f"""Frío                
Te quedan {intentos} intentos""")
            else:
                #Muy lejos
                await ctx.send(f"""Brrr... ¿No hace DEMASIADO frío aquí?              
Te quedan {intentos} intentos""")
                
        
        if intentos == 0:
            #Si te quedas sin intentos
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="Lo siento...", value=f"Has perdido, el número era {nCorrecto}. vuelve a intentarlo.", inline=False)
            await ctx.send(embed=embed)
            
            
    async def TrivAnime(self,ctx):
        embed=discord.Embed(color=0xff7700)
        embed.add_field(name="Has elegido trivial de anime.", value="Tendrás que responder 5 preguntas para ganar. Empezando el juego...", inline=False)
        await ctx.send(embed=embed)
        
        preguntas = 1 # pregunta actual
        bien = 0 # correctas
        mal = 0 # incorrectas
        while preguntas <6: #ponemos 5 preguntas
            #recogemos los datos del json
            pregunta, rCorrecta, listaR, disposicion = self.loadQuestions("cogs/animeTrivia.json")
        
            if disposicion == 1:
                # 1 disposicion de las preguntas
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {rCorrecta}
- {listaR[0]}
- {listaR[1]}
- {listaR[2]}```""", inline=False)
                await ctx.send(embed=embed)
            elif disposicion == 2:
                # 2 disposicion de las preguntas
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {listaR[0]}
- {rCorrecta}
- {listaR[2]}
- {listaR[1]}```""", inline=False)
                await ctx.send(embed=embed)
            elif disposicion == 2:
                # 3 disposicion de las preguntas
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {listaR[1]}
- {listaR[2]}
- {rCorrecta}
- {listaR[0]}```""", inline=False)
                await ctx.send(embed=embed)
            else:
                # 4 disposicion de las preguntas
                embed=discord.Embed(color=0xff7700)
                embed.add_field(name=f"{pregunta}", value=f"""```
- {listaR[2]}
- {listaR[1]}
- {listaR[0]}
- {rCorrecta}```""", inline=False)
                await ctx.send(embed=embed)
        
            preguntas += 1
            
            msg = (await self.bot.wait_for('message', check= self.utils.check(ctx.author), timeout=5000)).content
            #Recibimos el mensaje del jugador y comprobamos si la respuesta es correcta y sumamos
            if rCorrecta.lower() == msg.lower():
                bien+=1
                b = await ctx.send("Correcto.")
                await b.add_reaction('💯') # \:100:
            else:
                mal+=1
                m = await ctx.send(f"Incorrecto, la respuesta era ```{rCorrecta}.```")
                await m.add_reaction('💩') # \:poop:
                
        await self.checkResults(ctx, bien, mal) # Comprobamos resultados
        
    
    async def Trivial(self,ctx):
        #Lo mismo que el trivial Anime pero cargando otro .json
        embed=discord.Embed(color=0xff7700)
        embed.add_field(name="Has elegido trivial de cultura general.", value="Tendrás que responder 5 preguntas para ganar. Empezando el juego...", inline=False)
        await ctx.send(embed=embed)
        
        preguntas = 1
        bien = 0
        mal = 0
        while preguntas <6:
            pregunta, rCorrecta, listaR, disposicion = self.loadQuestions("cogs/Trivia.json")
        
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
    
    async def TresEnRaya(self,ctx):
        embed=discord.Embed(color=0xff7700)
        embed.add_field(name="Has elegido Tres en Raya.", value="¡Haz una línea de 3 para ganar!", inline=False)
        await ctx.send(embed=embed)
        
        mode = await self.chooseMode(ctx)
        # Creamos la tabla
        theBoard = ["1","2","3","4","5","6","7","8","9"]
        
        #Comprobamos el modo de juego
        
        if mode == "1p":
            
            playerLetter, computerLetter = await self.inputPlayerLetter(ctx,mode,None) #Cogemos el X o O
            turn = self.whoGoesFirst(mode,None) # Decidimos quien va primero
            await ctx.send(f"```El {turn} irá primero```")
            gameIsPlaying = True
        
            while gameIsPlaying:
                #Empieza el juego
                if turn == 'jugador':
                    # Turno del jugador.
                    await self.drawBoard(theBoard,ctx) #Mostramos tabla
                    move = await self.getPlayerMove(theBoard,ctx) #Elegimos movimiento
                    self.makeMove(theBoard, playerLetter, move) #Hacemos movimiento
        
                    if self.isWinner(theBoard, playerLetter): #Comprobamos si ganamos
                        await self.drawBoard(theBoard,ctx) 
                        await self.checkBoard(ctx,True) # Printeamos que ha ganado el jugador
                        gameIsPlaying = False
                    else:
                        if self.isBoardFull(theBoard): # Comprobamos si la tabla está llena
                            await self.drawBoard(theBoard,ctx)
                            await self.checkBoard(ctx,None) # Printeamos que hay un empate
                            gameIsPlaying = False
                        else:
                            turn = 'bot' #Le pasamos el turno al bot
        
                else:
                    # Turno del bot.
                    move = self.getComputerMove(theBoard, computerLetter) #El bot elige movimiento
                    self.makeMove(theBoard, computerLetter, move) #Hacemos movimiento
        
                    if self.isWinner(theBoard, computerLetter): #Comprueba si ha ganado
                        await self.drawBoard(theBoard,ctx) #Printeamos que ha ganado el bot
                        await self.checkBoard(ctx,False)
                        gameIsPlaying = False
                    else:
                        if self.isBoardFull(theBoard):
                            await self.drawBoard(theBoard,ctx)
                            await self.checkBoard(ctx,None)
                            gameIsPlaying = False
                        else:
                            turn = 'jugador'
        
        elif mode == "2p":
            players = await self.getPlayers(ctx)
            turn = self.whoGoesFirst(mode,players) # Decidimos quien va primero
            await ctx.send(f"```{turn} irá primero```")
            player1, player2 = await self.inputPlayerLetter(ctx,mode,turn) #Cogemos el X o O
            gameIsPlaying = True
            
            while gameIsPlaying:
                #Empieza el juego
                if turn == players[0]:
                    # Turno del jugador.
                    await self.drawBoard(theBoard,ctx) #Mostramos tabla
                    move = await self.getPlayerMove(theBoard,ctx) #Elegimos movimiento
                    self.makeMove(theBoard, player1, move) #Hacemos movimiento
        
                    if self.isWinner(theBoard, player1): #Comprobamos si ganamos
                        await self.drawBoard(theBoard,ctx) 
                        await self.checkBoard(ctx,True) # Printeamos que ha ganado el jugador
                        gameIsPlaying = False
                    else:
                        if self.isBoardFull(theBoard): # Comprobamos si la tabla está llena
                            await self.drawBoard(theBoard,ctx)
                            await self.checkBoard(ctx,None) # Printeamos que hay un empate
                            gameIsPlaying = False
                        else:
                            turn = players[1] #Le pasamos el turno al otro jugador
        
                else:
                    # Turno del otro jugador.
                    await self.drawBoard(theBoard,ctx) #Mostramos tabla
                    move = await self.getPlayerMove(theBoard,ctx) #Elegimos movimiento
                    self.makeMove(theBoard, player2, move) #Hacemos movimiento
        
                    if self.isWinner(theBoard, player2): #Comprobamos si ganamos
                        await self.drawBoard(theBoard,ctx) 
                        await self.checkBoard(ctx,True) # Printeamos que ha ganado el jugador
                        gameIsPlaying = False
                    else:
                        if self.isBoardFull(theBoard): # Comprobamos si la tabla está llena
                            await self.drawBoard(theBoard,ctx)
                            await self.checkBoard(ctx,None) # Printeamos que hay un empate
                            gameIsPlaying = False
                        else:
                            turn = players[0]
            
            
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
            
    async def drawBoard(self,board,ctx):
        #Dibujamos la tabla
        await ctx.send(f"""```     |     |
  {board[0]}  |  {board[1]}  |  {board[2]}
     |     |
ーーーーーーーーーーー
     |     |
  {board[3]}  |  {board[4]}  |  {board[5]}
     |     |
ーーーーーーーーーーー
     |     |
  {board[6]}  |  {board[7]}  |  {board[8]}
     |     |```""")
    async def inputPlayerLetter(self,ctx,mode,turn):
        
        if mode == "1p":
            # Dejamos al jugador elegir la letra, siendo la contraria el bot
            letter = ''
            while not (letter.upper() == 'X' or letter.upper() == 'O'):
                await ctx.send('```¿Quieres ser X o O?```')
                letter = (await self.bot.wait_for('message', check= self.utils.check(ctx.author), timeout=5000)).content
    
            # El primer elemento de la tupla será el jugador y el segundo el bot
            if letter.upper() == 'X':
                return ['X', 'O']
            else:
                return ['O', 'X']
        
        if mode == "2p":
            
                        # Dejamos al jugador elegir la letra, siendo la contraria el bot
            letter = ''
            while not (letter.upper() == 'X' or letter.upper() == 'O'):
                await ctx.send('```¿Quieres ser X o O?```')
                letter = (await self.bot.wait_for('message', check=lambda message: not message.author.bot, timeout=5000)).content
                if str(ctx.message.author) != turn:
                    letter = (await self.bot.wait_for('message', check=lambda message: not message.author.bot, timeout=5000)).content
            # El primer elemento de la tupla será el jugador y el segundo el bot
            if letter.upper() == 'X':
                return ['X', 'O']
            else:
                return ['O', 'X']
        
    def whoGoesFirst(self,mode,players):
        # Se elige aleatoriamente quién empieza el juego
        if mode == "1p":
            if random.randint(0, 1) == 0:
                return 'bot'
            else:
                return 'jugador'
        elif mode == "2p":
            if random.randint(0, 1) == 0:
                return players[0]
            else:
                return players[1]
            
    def makeMove(self,board, letter, move):
        # Realizamos el movimiento
        # Reemplaza el numero de la tabla por la letra del jugador
        board[move-1] = letter
    
    def isWinner(self,board, letter):
        
        #Comprobamos en la tabla y la letra de un jugador si se ha hecho
        # una linea de 3 y envia True si el jugador ha ganado
        return ((board[6] == letter and board[7] == letter and board[8] == letter) or # linea horizontal arriba
        (board[3] == letter and board[4] == letter and board[5] == letter) or # linea horizontal centrica
        (board[0] == letter and board[1] == letter and board[2] == letter) or # linea horizontal baja
        (board[6] == letter and board[3] == letter and board[0] == letter) or # linea vertical izquierda
        (board[7] == letter and board[4] == letter and board[1] == letter) or # linea vertical centrica
        (board[8] == letter and board[5] == letter and board[2] == letter) or # linea vertical derecha
        (board[6] == letter and board[4] == letter and board[2] == letter) or # diagonal 1
        (board[8] == letter and board[4] == letter and board[0] == letter)) # diagonal 2
    
    def isSpaceFree(self,board, move):
        # Devuelve True si el numero(movimient) recibido está libre en el tablon
        return board[move-1].isdigit()
    
    async def getPlayerMove(self,board,ctx):
        # El jugador elige el movimiento
        move = ' '
        #Comprobamos que sea un numero del 1 al 9 y que esté libre, sino hay que elegir otro
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceFree(board, int(move)):
            await ctx.send('```Elige tu movimiento. (1-9)```')
            move = (await self.bot.wait_for('message', check= self.utils.checkNumber(ctx.author), timeout=5000)).content
        return int(move)
    
    def chooseRandomMoveFromList(self,board, movesList):
        #El método devolverá uno de los distintos movimientos posibles a través de una lista recibida
        possibleMoves = []
        for i in movesList:
            if self.isSpaceFree(board, i):
                possibleMoves.append(i)
    
        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None
        
    def getBoardCopy(self,board):
        # Hace un duplicado de la tabla para uso del bot.
        dupeBoard = []
    
        for i in board:
            dupeBoard.append(i)
    
        return dupeBoard
        
    def getComputerMove(self,board, computerLetter):
        # Con la tabla y la letra del bot determina qué movimiento hacer
        if computerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'
    
        # Algoritmo del bot:
        # Primero probamos si puede ganar en el siguiente turno
        # Hace una copia de la tabla y recorre en cada movimiento la
        # Tabla para comprobar si ganaría, si lo hace, devuelve
        # El movimiento con el que ganaría
        for i in range(0, 9):
            copy = self.getBoardCopy(board)
            if self.isSpaceFree(copy, i):
                self.makeMove(copy, computerLetter, i)
                if self.isWinner(copy, computerLetter):
                    return i
    
        # Luego probamos si puede ganar el jugador con el mismo sistema
        # pero aplicando la letra del jugador y así poder evitar que gane
        for i in range(0, 9):
            copy = self.getBoardCopy(board)
            if self.isSpaceFree(copy, i):
                self.makeMove(copy, playerLetter, i)
                if self.isWinner(copy, playerLetter):
                    return i
    
        #Si nadie va a ganar intentamos coger alguna de las esquinas de la tabla si está libre
        move = self.chooseRandomMoveFromList(board, [0, 2, 6, 8])
        if move != None:
            return move
    
        #Si no hay esquinas libres intentamos coger el centro.
        if self.isSpaceFree(board, 5):
            return 5
    
        #Si el centro no está disponible intentamos coger los lados
        return self.chooseRandomMoveFromList(board, [1, 3, 5, 7])    
    
    def isBoardFull(self,board):
        #Comprueba si la tabla está llena o no
        for i in range(0, 9):
            if self.isSpaceFree(board, i):
                return False
        return True        
    
    async def checkBoard(self,ctx,booleano):
        #Mostramos segun hayamos ganado, perdido o haya empate.
        if booleano == True:
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="¡Enhorabuena!", value=f"¡Has ganado!", inline=False)
            w = await ctx.send(embed=embed)
            await w.add_reaction('🎉') # \:tada:
            await w.add_reaction('🎊') # \:confetti_ball:
            await w.add_reaction('🎈') # \:balloon:
        elif booleano == False:
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="Has perdido", value=f"¡Una pena!", inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xff7700)
            embed.add_field(name="¡Empate!", value=f"Vuelve a intentarlo.", inline=False)
            await ctx.send(embed=embed)
            
    async def chooseMode(self,ctx):
        
        embed=discord.Embed(color=0xff7700)
        embed.add_field(name="Elige el modo.", value="""```1 - 1 Jugador
2 - 2 Jugadores```""", inline=False)
        await ctx.send(embed=embed)
        #Recibimos el mensaje de la persona especifica
        msg = (await self.bot.wait_for('message', check=self.utils.checkNumber(ctx.author), timeout=5000)).content
        if msg == "1":
            return "1p"
            
        elif msg == "2":
            return "2p"
            
    async def getPlayers(self,ctx):
        players= []
        
        while not len(players)==2:
            if players == []:
                await ctx.send("Jugador uno que se presente con ```play```")
                msg = (await self.bot.wait_for('message', check=lambda message: not message.author.bot, timeout=5000)).content
                if msg == "play":
                    players.append(str(ctx.message.author))
                    embed=discord.Embed(color=0xff7700)
                    embed.add_field(name="Jugador 1", value=f"{players[0]}", inline=False)
                    await ctx.send(embed=embed)
            elif len(players) == 1:
                await ctx.send("Jugador dos que se presente con ```play```")
                msg = (await self.bot.wait_for('message', check=lambda message: not message.author.bot, timeout=5000)).content
                if msg == "play":
                    players.append(str(ctx.message.author))
                    embed=discord.Embed(color=0xff7700)
                    embed.add_field(name="Jugador 2", value=f"{players[1]}", inline=False)
                    await ctx.send(embed=embed)
            else:
                print ("mec")
        return players
                
            
            