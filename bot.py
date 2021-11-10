import random

import discord
import os
import json

class ReaderWriter():
    src = ""
    def __init__(self, f):
        self.src = f
    def readfile(self, va):
        ret = []
        with open(self.src, "r") as file:
            for x in file:
                a = json.loads(x)
                z = []
                for n in va:
                    z.append(a[n])
                ret.append(z)
        return ret
    def writefile(self, id , va): #id value
        with open(self.src, "w") as file:
            j = 0
            for x in id:
                wr  = "{"
                i = 0
                for n in x:
                    wr = wr + '"' + n + '":"' + va[j][i] + '"'
                    if(i < len(x)-1):
                        wr = wr + ","
                    i = i + 1
                wr = wr + "}\n"
                file.write(wr)
                j = j +1
    def deletefile(self):
        with open(self.src, "w") as file:
            file.write("")
    def appendfile(self, id, val):
        with open(self.src, "a") as file:
            for x in id:
                j = 0
                wr  = "{"
                i = 0
                for n in x:
                    wr = wr + '"' + n + '":"' + val[j][i] + '"'
                    if(i < len(x)-1):
                        wr = wr + ","
                    i = i + 1
                wr = wr + "}\n"
                file.write(wr)
                print(id)
                print(val)
                print(wr)
                j = j +1;

class Users():
    rw = None
    allusers = []
    stdva = []
    def __init__(self):
        self.rw = ReaderWriter("users")
        self.stdva = ["id","pm"]
        self.getusers()
    def adduser(self, id, pmlevel):
        self.rw.appendfile([self.stdva],[[str(id), str(pmlevel)]])
    def deluser(self, id):
        beg = self.rw.readfile(self.stdva)
        end =  []
        for x in beg:
            if x[0] != id:
                end.append(x)
        self.rw.deletefile()
        for x in end:
            self.rw.appendfile(self.stdva, [x])

        #print(self.allusers)
    def getusers(self):
        self.allusers = self.rw.readfile(self.stdva)
        print(self.allusers)
    def checkpm(self, id, reqlevel):
        pm = 0
        reqlevel = int(reqlevel)
        for a in self.allusers:
            print((a[0], id))
            if a[0] == str(id):
                pm = int(a[1])
                break
        print((pm, reqlevel, pm >= reqlevel))
        if pm >= reqlevel:
            return True
        else:
            return False


class Jokes():
    us = None
    rw = ReaderWriter("jokes")
    stdva = ['id', 'joke']
    jokes = []
    def __init__(self, zus):
        self.us = zus
        self.update()
    def addjoke(self, jo):
        tid = 0
        if(self.jokes != []):
            for x in self.jokes:
                for b in self.jokes:
                    print((b[0],tid))
                    if(b[0] == tid):
                        tid += 1
        self.rw.appendfile([self.stdva], [[str(tid), jo]])
        return tid
    def remjoke(self,id):
        beg = self.rw.readfile()
        end = []
        for x in beg:
            if(x[0] != id):
                end.append(x)
        for x in end:
            self.rw.writefile([self.stdva], [x])
    def telljoke(self, jid = "-1"):
        tid = 0
        for x in self.jokes:
            if(int(x[0]) > int(tid)):
                tid = int(x[0])
        if(jid == -1):
             resid = random.randint(0,tid)
        else:
            resid = jid
        for x in self.jokes:
            if(x[0] == resid):
                return (x[1],resid)
        if(self.jokes == [] or jid != -1):
            return -1
        elif(jid == -1):
            return self.telljoke()

    def update(self):
        self.jokes = self.rw.readfile(self.stdva)
class wisdom():
    def __init__(self):
        pass

class MyClient(discord.Client):
    #Einloggen
    us = Users()
    jok = Jokes(us)
    async def on_ready(self):
        print("I'm in")
    async def on_message(self, message):
        if message.author == client.user:
            return
        print("From " + str(message.author.id) + " with " + str(message.content))
        if not message.content.startswith("!"):
            return
        #await message.reply("Valid Command")
        com = message.content[1:]
        splitcom = com.split()
        #Return id of sender
        if(splitcom[0] == "myid"):
            await message.reply(str(message.author.id))
        #Commands for user class
        if(splitcom[0] == "user"):
            #User adden
            if(splitcom[1] == "add"):
                if not self.us.checkpm(message.author.id, 10):
                    await message.reply("No permission")
                    return
                print("adding")
                self.us.adduser(splitcom[2],splitcom[3])
            elif(splitcom[1]== "del"):
                if not self.us.checkpm(message.author.id, 10):
                    await message.reply("No permission")
                    return
                print("deleting")
                self.us.deluser(splitcom[2])
            #User updaten
            elif(splitcom[1] == "update"):
                if not self.us.checkpm(message.author.id, 2):
                    await message.reply("No permission")
                    return
                print("updating")
                self.us.getusers()
            elif(splitcom[1] == "checkpm"):
                await message.reply(self.us.checkpm(splitcom[2], splitcom[3]))

        #Commands for joke class
        if(splitcom[0] == "joke"):
            if splitcom[1] == "tell":
                if not self.us.checkpm(message.author.id, 10):
                    await message.reply("No permission")
                    return
                if(len(splitcom) <3):
                    tid = -1
                else:
                    tid = splitcom[2]
                ret = self.jok.telljoke(tid)
                print(ret)
                if ret == -1:
                    await message.reply("Index not forgiven or no item in list!")
                else:
                    await message.reply(ret[0]+ " ("+ret[1]+")")
            if splitcom[1] == "add":
                if not self.us.checkpm(message.author.id, 10):
                    await message.reply("No permission")
                    return
                j = ""
                for i in range(2, len(splitcom)):
                    j = j + splitcom[i]
                    if(i < len(splitcom)-1):
                        j = j + " "
                zid = self.jok.addjoke(j)
                await message.reply("Your Joke has been added. The id is: " + str(zid))
            if splitcom[1] == "del":
                if not self.us.checkpm(message.author.id, 10):
                    await message.reply("No permission")
                    return
                pass
        if(splitcom[0] == "server"):
            if(splitcom[1]=="members"):
                await message.reply(message.guild.members)
        #await message.reply(splitcom)


if(__name__ == "__main__"):
    token = ""
    with open("token","r") as f:
        token = f.readline()
    client = MyClient()
    client.run(token)
