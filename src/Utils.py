




class Utils():
    def __init__(self):
        pass
        
    def check(self,author):
        #Recibe el author
        def inner_check(message): 
            #Checkea si el mensaje del autor es de el autor y número y devuelve boolean
            if message.author != author:
                return False
            try: 
                int(message.content) 
                return True 
            except ValueError: 
                return False
        return inner_check