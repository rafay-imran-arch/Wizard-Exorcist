import pygame
import os

pygame.init()


class Room():
    def __init__(self, name, enemy_list):
        self.name = name
        self.enemies = enemy_list
        self.cleared = False

        self.connections = {}

def build_dungeon():

    from sprites import enemy, ghost, bat, slime, pumpkin

    rooms = {
        "spawn room": Room("The spawn point", [
            slime(200,20,128,128),
            bat(60,100,128,128)
        ]),

        "east guardroom": Room("The abandoned East Guardroom",[
            slime(200,100,128,128),
            bat(500,70,128,128)
        ]),
        
        "north vault": Room("The broken vault room",[
            bat(200,50,128,128),
            bat(100,200,128,128),
            bat(600,300,128,128)
        ])
    }

    rooms["spawn room"].connections = {'north': "north vault", "east": "east guardroom"}
    rooms["east guardroom"].connections = {'west': "spawn room"}
    rooms['north vault'].connections = {'south': "spawn room"}

    return rooms