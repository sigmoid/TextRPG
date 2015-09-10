#Lab 02
#09-09-15
#Adam Waggoner - u1014822

from random import randint

class Entity:
    def __init__(self, name="MISSINGNO", health=0, damage=0, age=0):
        self.name = name
        self.health = health
        self.damage = damage
        self.age = age
        self.dead = 0
        
class Player(Entity):
    def __init__(self, name = '', strength = 0,agility = 0,intelligence = 0):
        self.name = name
        self.strength = randint(8,10)
        self.agility = randint(5,10)
        self.intelligence= randint(5,10)
        self.damage = self.agility * 5
        self.health = self.strength * 10
        self.mana = self.intelligence * 30
        self.dead = 0

class Monster(Entity):
    def __init__(self, name='', health=0,damage=0):
        self.name = name
        self.health = randint(25,100)
        self.damage = randint(5,25)
        self.dead = 0

def DisplayRooms():
    print('----')
    print('|1|2|')
    print('|- -|')
    print('|3|4|')
    print('----')

def DisplayStatus(currentroom,Entities):
    print ('\nRoom: '+currentroom['name'])
    print ('-------------')
    print (Entities[0].name + ' Health: ' + str(Entities[0].health))
    print('---ENEMIES---')
    for i in currentroom['monsters']:
        if(i.dead == 0):
            print (i.name)
            print ('Health: ' + str(i.health))
    print('------------')
    availActions = "Available Actions:"
    if 'north' in currentroom:
        availActions += "\n-Move north"
    if 'east' in currentroom:
        availActions += "\n-Move east"
    if 'south' in currentroom:
        availActions += "\n-Move south"
    if 'west' in currentroom:
        availActions += "\n-Move west"

    for e in currentroom['monsters']:
        if e.dead == 0:
            availActions += "\n-Attack"
            break;
        
    print(availActions + '\n')

def Attack(sender,reciever):
    dmg = randint(0,sender.damage)    
    reciever.health -= dmg
    print("\n"+sender.name+" hit "+reciever.name + " for " + str(dmg) + " damage!")
    if (reciever.health <=0):
        reciever.dead = 1;
        print(reciever.name + " has died!")

def MonsterAttackTurn(Player, Room):
    for e in Room["monsters"]:
        if(e.dead == 0):
            Attack(e,Player)
    
def Update():
    print(EntityList)
    
def main():
    #Global Variables
    PLAYERID = 0
    currentRoom = 1

    #Create dictionary of Rooms
    Rooms = { 1: {"name":"Hall",
                  "south":3,
                  "east":2,
                  "monsters":[]},
              
              2: {"name":"Bedroom",
                  "south":4,
                  "west":1,
                  "monsters":[]},

              3: {"name":"Kitchen",
                  "north":1,
                  "east":4,
                  "monsters":[]},

              4: {"name":"Bathroom",
                  "north": 2,
                  "west":3,
                  "monsters":[]}
        }
    RoomCount = 4

        #Enter Playername
    cachedPlayer = Player(input('Player Name: '))
    cachedPlayer.age = eval(input('Player Age: '))

    #Enter numMonsters and Monster names
    numMonst = eval(input('How many monsters? '))

    EntityList = [Entity()] * (numMonst + 1)

    #Populate Monster list and get names
    for e in range(1,len(EntityList)):
        EntityList[e] = Monster()
        EntityList[e].name = input('Monster ' + str(e) +': ')
    
    #Add Player to list of Entities
    EntityList[PLAYERID] = cachedPlayer

    #print Data to player
    print("\n---Player---")

    player = EntityList[PLAYERID]

    print('\nName: ' + player.name)
    print('Strength: ' + str(player.strength))
    print('Agility: ' + str(player.agility))
    print('Intelligence: ' + str(player.intelligence))
    print('Health: ' + str(player.health))
    print('Damage: ' + str(player.damage))
    print('Mana: ' + str(player.mana))
    
    print("\n---Monsters---")
    
    for e in range(1,len(EntityList)):
           print('\nName: ' + EntityList[e].name)
           print('Health: ' + str(EntityList[e].health))
           print('Damage: ' + str(EntityList[e].damage))

    #Place monsters in rooms
    for i in range(1,len(EntityList)):
        Rooms[randint(1,RoomCount)]['monsters'].append(EntityList[i])

    #Get start Room
    DisplayRooms()
    currentRoom = Rooms[eval(input('Which room would you like to start in? (1-4) '))]
    DisplayStatus(currentRoom,EntityList)

    #Update loop
    isRunning = 1;

    while(isRunning):
        if EntityList[PLAYERID].dead == 1:
            #really long ASCII art
            print ('_____.___.              ________  .__           .___\n\\__  |   | ____  __ __  \\______ \\ |__| ____   __| _/\n /   |   |/  _ \\|  |  \\  |    |  \\|  |/ __ \\ / __ |\n \\____   (  <_> )  |  /  |    `   \\  \\  ___// /_/ |\n / ______|\\____/|____/  /_______  /__|\\___  >____ |\n \\/                             \\/        \\/     \\/ ')
            return
        
        #Gets case insensitive player input and splits it into list
        inp = input(">").lower().split()

        if 'move' == inp[0] and len(inp) > 1:
            if(inp[1] in currentRoom):
                currentRoom = Rooms[currentRoom[inp[1]]]
                DisplayStatus(currentRoom,EntityList)
                continue 
                
            else:
                print('Unable to move: "' + inp[1])
                continue

            
        if 'attack' == inp[0] and len(inp) > 1:
            enemyFound = 0
            for e in EntityList:
                if inp[1] == e.name and e.dead == 0:
                    Attack(EntityList[PLAYERID],e)
                    MonsterAttackTurn(EntityList[PLAYERID],currentRoom)
                    DisplayStatus(currentRoom,EntityList)
                    enemyFound=1
                    break

            if(enemyFound == 0):
                print("There is no monster " + inp[1] + " in this room!")
                DisplayStatus(currentRoom,EntityList)
                continue
            else:
                continue
                
        if 'closegame' == inp[0]:
            isRunning = 0
            continue

        print('Cannot do ' + str(inp))

        
        
        
        
        

main()
    
        
