import discord
import os
import json

class Users():
    allusers = []
    def __init__(self):
        self.getusers()
    def adduser(self, id, pmlevel):
        with open("users", 'a') as file:
            file.write('{"name":"'+id+'", "pm":"'+pmlevel+'"}')
    def deluser(self, id):
        save = []
        with open("users", "r")as file:
            for x in file:
                a = json.loads(x)
                if not a["name"] == id:
                    save.append(x)
        #print(save)
        with open("users", "w") as file:
            file.write("")
        with open("users", "a")as file:
            for x in save:
                file.write(x)
        #print(self.allusers)
    def getusers(self):
        self.allusers = []
        with open("users", "r")as file:
            for x in file:
                a = json.loads(x)
                self.allusers.append([a["name"],a["pm"]])
        print(self.allusers)
    def checkpm(self, id, reqlevel):
        pm = 0
        for a in self.allusers:
            if a[0] == id:
                pm = a[1]
                break
        print((pm, reqlevel, pm > reqlevel))
        if pm > reqlevel:
            return True
        else:
            return False



class jokes():
    def __init__(self):
        pass
class wisdom():
    def __init__(self):
        pass

class MyClient(discord.Client):
    #Einloggen
    us = Users()
    async def on_ready(self):
        print("I'm in")
    async def on_message(self, message):
        if message.author == client.user:
            return
        print("From " + str(message.id) + " with " + str(message.content))
        if not message.content.startswith("/"):
            return
        com = message.content[1:]
        splitcom = com.split()
        #Return id of sender
        if(splitcom[0] == "myid"):
            await message.channel.send(str(message.author.id))
        #Commands for user class
        if(splitcom[0] == "user"):
            #User adden
            if(splitcom[1] == "add"):
                print("adding")
                self.us.adduser(splitcom[2],splitcom[3])
            elif(splitcom[1]== "delete"):
                print("deleting")
                self.us.deluser(splitcom[2])
            #User updaten
            elif(splitcom[1] == "update"):
                print("updating")
                self.us.getusers()
            elif(splitcom[1] == "checkpm"):
                print(self.us.checkpm(splitcom[2], splitcom[3]))
        await message.reply(splitcom)

client = MyClient()
client.run("ODk5NzMyMDY0NTE2MDU1MTIw.YW3CyA.mw0tWK_XZ11JLV2JVKD8_j3eqd0")