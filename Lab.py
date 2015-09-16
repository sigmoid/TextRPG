#Lab 02
#09-09-15
#Adam Waggoner - u1014822

from random import randint

class Spell:
    def __init__(self,manaCost = 0, healthEffect = 0):
        self.manaCost = manaCost
        self.healthEffect = healthEffect

class Entity:
    def __init__(self, name="MISSINGNO", health=0, damage=0, age=0):
        self.name = name
        self.health = health
        self.healthPool = health
        self.damage = damage
        self.age = age
        self.dead = 0
        
class Player(Entity):
    def CalculateStats(self):
        self.damage = self.agility * 5
        self.health = self.strength * 10
        self.healthPool = self.strength * 10
        self.mana = self.intelligence * 25
        self.manaPool = self.intelligence * 25
        
    def __init__(self, name = '', strength = 0,agility = 0,intelligence = 0):
        self.name = name
        self.strength = 5
        self.agility = 5
        self.intelligence= 0
        self.damage = self.agility * 5
        self.health = self.strength * 10
        self.healthPool = self.strength * 10
        self.mana = self.intelligence * 25
        self.manaPool = self.intelligence * 25
        self.dead = 0
        self.spells = {
            'heal':Spell(25,-15),
            'fireball':Spell(50,30)
                       }

class Monster(Entity):
    def __init__(self, name='', health=0,damage=0):
        self.name = name
        self.health = randint(25,75)
        self.healthPool = self.health
        self.damage = randint(5,15)
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
    print (Entities[0].name + ' Health: ' + str(Entities[0].health) + '/' + str(Entities[0].healthPool))
    print (Entities[0].name + ' Mana: ' + str(Entities[0].mana) + '/' + str(Entities[0].manaPool))

    enemyCount=0
    enemyOutput = ''
    for i in currentroom['monsters']:
        if(currentroom['monsters'][i].dead == 0):
            enemyOutput += '\n'+currentroom['monsters'][i].name
            enemyOutput += '\nHealth: ' + str(currentroom['monsters'][i].health)
            enemyCount+=1
            
    if enemyCount >0:        
        print('---ENEMIES---')
        print(enemyOutput)
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

    availActions += "\n-Wait"

    for e in currentroom['monsters']:
        if currentroom['monsters'][e].dead == 0:
            availActions += "\n-Attack"
            break;

    for spell in Entities[0].spells:
        if(Entities[0].mana >= Entities[0].spells[spell].manaCost):
            availActions += "\n-Cast " + spell
        
    print(availActions + '\n')

#Actions
def TakeDamage(sender,reciever,dmg):
    if(dmg>0):
        reciever.health -= dmg
        print("\n"+sender.name+" hit "+reciever.name + " for " + str(dmg) + " damage!")
        if (reciever.health <=0):
            reciever.dead = 1;
            print(reciever.name + " has died!")
    elif(dmg<0):
        reciever.health -= dmg
        reciever.health = Clamp(reciever.health,0,reciever.healthPool)
        print("\n" +reciever.name + " gained " + str(-dmg) + " hp!")

def Attack(sender,reciever, nerf=1):
    dmg = int(randint(int(sender.damage/1.25),sender.damage) * nerf)    
    TakeDamage(sender,reciever,dmg)

def Cast(sender, spell, reciever):
    s = sender.spells[spell]
    
    if sender.mana >= s.manaCost:
        sender.mana-= s.manaCost
        print (sender.name + " cast " + spell + " on " + reciever.name)
        TakeDamage(sender,reciever,s.healthEffect)
    else:
        print ('Not enough mana!')
    

#Turn Attributes
def MonsterAttackTurn(Player, Room, nerfFrac=1):
    for e in Room["monsters"]:
        ent = Room["monsters"][e]
        if(ent.dead == 0):
            Attack(ent,Player,nerfFrac)

def ManaTurn(Player):
    Player.mana += 5 + int(Player.intelligence/2) * 5
    Player.mana = Clamp(Player.mana, 0, Player.manaPool)

def Clamp(val, min, max):
    if(val<min):
        return min
    if(val>max):
        return max
    return val

monsPrefixes = ['Cloud','Ember','Dust','Plasma','Flux','Venom','Acid','Bane','Poison','Germ','Nether','Rot','Sorrow','Half']
monsSuffixes = ['bane','body','lurker','morph','walker','crawler','creeper','fang','rat','giant','dwarf','wraith']
def GenMonsterName():
    return monsPrefixes[randint(0,len(monsPrefixes)-1)] + monsSuffixes[randint(0,len(monsSuffixes)-1)]
    
    

#Global Vars
EntityList = [Entity()]
PLAYERID = 0

#Create dictionary of Rooms
Rooms = { 1: {"name":"Hall",
                 "south":3,
                  "east":2,
                  "monsters":{}},
              
              2: {"name":"Bedroom",
                  "south":4,
                  "west":1,
                  "monsters":{}},

              3: {"name":"Kitchen",
                  "north":1,
                  "east":4,
                  "monsters":{}},

              4: {"name":"Bathroom",
                  "north": 2,
                  "west":3,
                  "monsters":{}}
        }
#Global Variables contd
currentRoom = 1

def main():
    RoomCount = len(Rooms)

    #Enter Playername
    cachedPlayer = Player(input('Player Name: '))
    cachedPlayer.age = eval(input('Player Age: '))

    #Customize Stats
    statPoints = 5
    while(statPoints >0):
        print("Points to assign: " + str(statPoints))
        inp = input("Which stat would you like to assign? ([S]trengh/[I]ntelligence/[A]gility)\n").upper()
        if(inp == 'S'):
            cachedPlayer.strength += 1
            statPoints -= 1
            continue
        if(inp == 'A'):
            cachedPlayer.agility += 1
            statPoints -= 1
            continue
        if(inp == 'I'):
            cachedPlayer.intelligence +=1
            statPoints -=1
            continue
        
        print ("Can't assign " + inp)
    #Recalculate stats
    cachedPlayer.CalculateStats()
    
    #Enter numMonsters and Monster names
    numMonst = eval(input('How many monsters? '))

    EntityList = [Entity()] * (numMonst + 1)

    nameMonst = input('Give Monsters custom names? Y/N ').upper()
    
    if(nameMonst == 'Y'):
        #Populate Monster list and get names
        for e in range(1,len(EntityList)):
            EntityList[e] = Monster()
            EntityList[e].name = input('Monster ' + str(e) +': ')
    else:
        #Populate Monster list and get names
        for e in range(1,len(EntityList)):
            EntityList[e] = Monster()
            EntityList[e].name = GenMonsterName()
    
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
        Rooms[randint(1,RoomCount)]['monsters'][EntityList[i].name.lower()]=EntityList[i]

    #Get start Room
    DisplayRooms()
    try:
        currentRoom = Rooms[eval(input('Which room would you like to start in? (1-4) '))]
    except:
        currentRoom = Rooms[1]
        print("I'm going to assume you meant '1'")
        
    DisplayStatus(currentRoom,EntityList)

    #Update loop
    isRunning = 1;

    while(isRunning):
        if EntityList[PLAYERID].dead == 1:
            #really long ASCII art, http://bigtext.org/, font = fender
            #print ('_____.___.              ________  .__           .___\n\\__  |   | ____  __ __  \\______ \\ |__| ____   __| _/\n /   |   |/  _ \\|  |  \\  |    |  \\|  |/ __ \\ / __ |\n \\____   (  <_> )  |  /  |    `   \\  \\  ___// /_/ |\n / ______|\\____/|____/  /_______  /__|\\___  >____ |\n \\/                             \\/        \\/     \\/ ')
            print("'\\\\  //`                        ||`                 ||` \n  \\\\//                          ||   ''             ||  \n   ||    .|''|, '||  ||`    .|''||   ||  .|''|, .|''||  \n   ||    ||  ||  ||  ||     ||  ||   ||  ||..|| ||  ||  \n  .||.   `|..|'  `|..'|.    `|..||. .||. `|...  `|..||. ")
            isRunning = 0
            break
        
        #Gets case insensitive player input and splits it into list
        inp = input(">").lower().split()

        #Process a turn
        if 'move' == inp[0] and len(inp) > 1:
            if(inp[1] in currentRoom):
                MonsterAttackTurn(EntityList[0],currentRoom,.5)
                currentRoom = Rooms[currentRoom[inp[1]]]
                DisplayStatus(currentRoom,EntityList)
                continue 
                
            else:
                print('Unable to move: "' + inp[1])
                continue

        if 'cast' == inp[0]:
            if len(inp) ==2 and inp[1] in EntityList[0].spells:
                #make player cast on self if there's no other input
                Cast(EntityList[0],inp[1],EntityList[0])
                MonsterAttackTurn(EntityList[0],currentRoom)
                DisplayStatus(currentRoom,EntityList)
                continue
            
            if len(inp) == 3 and inp[1] in EntityList[0].spells:
                if inp[2] in currentRoom['monsters']:
                    Cast(EntityList[0],inp[1],currentRoom['monsters'][inp[2]])
                    MonsterAttackTurn(EntityList[0],currentRoom)
                    DisplayStatus(currentRoom, EntityList)
                    continue
                else:
                    print ('There is no monster ' + inp[2] + ' in this room!')
        
        if 'attack' == inp[0] and len(inp) > 1:
            if(inp[1] in currentRoom['monsters']):
                Attack(EntityList[0],currentRoom['monsters'][inp[1]])
                MonsterAttackTurn(EntityList[0],currentRoom)
                ManaTurn(EntityList[0])
                DisplayStatus(currentRoom,EntityList)
                continue
            else:
                print('There is no monster named ' + inp[1] + ' in this room')
                
        if 'wait' == inp[0]:
            MonsterAttackTurn(EntityList[0],currentRoom)
            ManaTurn(EntityList[0])
            print (EntityList[0].name+ ' waited!')
            DisplayStatus(currentRoom,EntityList)
            continue
                
        if 'closegame' == inp[0]:
            isRunning = 0
            continue

        print('Cannot do ' + str(inp))


main()
    
        
