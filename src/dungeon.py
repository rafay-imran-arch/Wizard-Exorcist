import pygame
import os

pygame.init()


class Room():
    def __init__(self, name, enemy_list, image_name="default_room"):
        self.name = name
        self.enemies = enemy_list
        self.cleared = False
        
        self.connections = {}
        self.hidden_doors = []
        self.is_boss_room = False

        self.background_path = os.path.join("src","assets",'rooms', f"{image_name}.png")

def build_dungeon():

    from sprites import enemy, ghost, bat, slime, pumpkin, oneI

    rooms = {
        "spawn room": Room("The spawn point", [
            oneI(244,555,128,128)  
        ]),

        "the solar": Room("The abandoned solar room",[
            slime(200,100,128,128),
            bat(500,70,128,128)
        ]),
        
        "north vault": Room("The broken vault room",[
            bat(200,50,128,128),
            bat(100,200,128,128),
            bat(600,300,128,128)
        ]),

        "the study": Room("The abandoned Library",[
            slime(500,100,128,128),
            slime(600,20,128,128),
            bat(100,200,128,128),
            bat(200,400,128,128),
        ]),

        'spawn room2' : Room("Lower area of great hall",[
            bat(800,122,128,128),
            bat(400,200,128,128),
            ghost(300,500,128,128)
        ]),

        "lord's chambers": Room('The master bedroom', [
            slime(200,100,128,128),
            slime(100,300,128,128),
            slime(600,250,128,128)
        ]),

        "great dining": Room('The great dining hall',[
            slime(400,120,128,128),
            bat(300,650,128,128),
            ghost(200,450,128,128),
            ghost(40,28,128,128)
        ]),

        "spawn room3": Room("south expansion of great hallway",[
            ghost(10,129,128,128),
            ghost(45,650,128,128),
            pumpkin(500,500,128,128),
        ]),

        "princes room": Room('The grand room of prince',[
            bat(240,120,128,128),
            bat(200,300,128,128),
            pumpkin(500,128,128,128),
            slime(300,650,128,128)
        ]),

        "dungeon stairs": Room('The stairs which lead to dungeon',[
            oneI(700,400,128,128)
        ]),

        "banquet hall": Room('The banquet hall',[
            ghost(432,124,128,128),
            ghost(532,364,128,128)
        ]),

        # WEST WING HALLWAY

        "west wing hallway1": Room("The west wing hallway",[
            slime(120,400,128,128),
            pumpkin(213,435,128,128),
            pumpkin(435,213,128,128),
            ghost(563,124,128,128)
        ]),

        "west wing hallway2": Room("The second part of west wing hallway", [
            slime(313,124,128,128)
        ]),

        "west wing hallway3": Room("The third part fo the west wing hallway", [
            bat(421,145,128,128),
            ghost(241,632,128,128)
        ]),

        'north west guard': Room("North west guardroom",[
            slime(241,124,128,128)
        ]),

        'south west guard': Room('The south east guradroom/tower', [
            ghost(412,524,128,128),
        ]),

        # EAST WING HALLWAY 

        'east wing hallway1': Room("The east wing hallway", [
            slime(300,124,128,128),
            bat(543,532,128,128),
            bat(761,321,128,128)
        ]),
        
        'east wing hallway2': Room("The second part of east wing hallway", [
            ghost(245,12,128,128),
            pumpkin(87,81,128,128),
            ghost(52,29,128,128)
        ]),

        'east wing hallway3': Room("The third part of the east wing hallway", [
            bat(29,12,128,128),
            slime(742,124,128,128)
        ]),

        'north east guard': Room("The guardroom/tower of north east", [
            ghost(214,35,128,128),
            ghost(593,129,128,128),
            ghost(300,295,128,128)
        ]),

        'south east guard': Room('The guardroom/tower of south east side', [
            bat(742,400,128,128),
            pumpkin(444,542,128,128),
            ghost(204,729,128,128),
            ghost(600,600,128,128)
        ])
    
    }
    

    rooms["spawn room"].connections = {'north': "north vault", "east": "the solar", "west": "the study", 'south': "spawn room2"}
    rooms["north vault"].connections = {'south': 'spawn room'}
    rooms["the study"].connections = {'east': 'spawn room', 'west': 'west wing hallway1'}
    rooms["the solar"].connections = {'east': 'east wing hallway1', 'west': 'spawn room'}    
    # The expansiong of spawn hallway towars south hecne named 2
    rooms['spawn room2'].connections = {'north': "spawn room", 'west': "lord's chambers", 'east': 'great dining', 'south': 'spawn room3'}
    rooms["lord's chambers"].connections = {'east': 'spawn room2'}
    rooms['great dining'].connections = {'east': 'east wing hallway2', 'west': 'spawn room2'}

    # Spawn hallway expansion 3
    rooms['spawn room3'].connections = {'north': 'spawn room2', 'east': 'dungeon stairs', 'west': 'banquet hall'}
    rooms['banquet hall'].connections = {'east': 'spawn room3', 'west': 'west wing hallway2'}
    rooms['dungeon stairs'].connections = {'east': 'east wing hallway3', 'west': 'spawn room3'}
    rooms['princes room'].connections = {'west': 'west wing hallway3'}

    #West wing hallway connections
    rooms['west wing hallway1'].connections = {'north':'north west guard', 'south': 'west wing hallway2', 'east': 'the study'} 
    rooms['west wing hallway2'].connections = {'north': 'west wing hallway1', 'south': 'west wing hallway3','east': 'banquet hall'}
    rooms['west wing hallway3'].connections = {'north': 'west wing hallway2', 'east': 'princes room', 'south': 'south west guard'}

    #East wing hallway connections
    rooms['east wing hallway1'].connections = {'north': 'north east guard', 'south': 'east wing hallway2','west': 'the solar'}
    rooms['east wing hallway2'].connections = {'north': 'east wing hallway1', 'south': 'east wing hallway3', 'west': 'great dining'}
    rooms['east wing hallway3'].connections = {'north': 'east wing hallway2', 'west': 'dungeon stairs', 'south': 'south east guard'}

    #Guardrooms/ towers connections
    rooms['north east guard'].connections = {'south': 'east wing hallway1'}
    rooms['south east guard'].connections = {'north': 'east wing hallway3'}
    rooms['north west guard'].connections = {'south': 'west wing hallway1'}
    rooms['south west guard'].connections = {'north': 'west wing hallway3'}


    # The great hallway/ spawn room hallway
    rooms["spawn room"].hidden_doors = ['south']
    rooms['spawn room2'].hidden_doors = ['north', 'south']
    rooms['spawn room3'].hidden_doors = ['north']

    #The West Wing Hallway  
    rooms['west wing hallway1'].hidden_doors = ['south']
    rooms['west wing hallway2'].hidden_doors = ['north', 'south']
    rooms['west wing hallway3'].hidden_doors = ['north']

    #The East Wing Hallway
    rooms['east wing hallway1'].hidden_doors = ['south', 'north']
    rooms['east wing hallway2'].hidden_doors = ['north', 'south']
    rooms['east wing hallway3'].hidden_doors = ['north']

    rooms['dungeon stairs'].is_boss_room = True 

    return rooms 

# NOTES TO SELF :
# THE UPPER ROOMS ie NORTH and the BOTTOM rooms ie SOUTH of Hallway1 and 3 should be ignored respectively

