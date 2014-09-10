#!/opt/local/bin/python2.7
# -*- coding: Utf-8 -*

import pprint
import pygame
import sys
from pygame.locals import *
import os

# Init framebuffer/touchscreen environment variables
if sys.platform == "linux2":
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV'      , '/dev/fb1')
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
    os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')


# Init pygame and screen
print "Initting..."
pygame.init()
print "Setting Mouse invisible..."
#pygame.mouse.set_visible(False)
print "Setting fullscreen..."
if sys.platform == "darwin":
    fenetre = pygame.display.set_mode((320, 240))
else:
    modes = pygame.display.list_modes(16)
    fenetre = pygame.display.set_mode(modes[0], FULLSCREEN, 16)

pygame.font.init()

updateMainScreen = False
clickZones = []

class MainView:
    def __init__(self, size = (320, 240), name = None):
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        if name is not None:
            pygame.display.set_caption("SVideo_Py")
        self.shouldUpdate = False
    
    def needsUpdate(self):
        self.shouldUpdate = True
    
    def update(self):
        if self.shouldUpdate:
            pygame.display.flip()
            self.shouldUpdate = False

class ClickZone:
    def __init__(self, frame, type, action):
        self.frame = frame
        self.type = type
        self.action = action
    
    def processEvent(self, event):
        if self.frame.collidepoint(pygame.mouse.get_pos()) and self.type == event.type:
            self.action(event)

class Button:
    def __init__(self, view, position, imageName, action):
        self.view = view
        self.image = pygame.image.load(imageName).convert_alpha()
        self.action = action
        self.state = False
        self.frame = pygame.Rect(position, self.image.get_size())
        clickZones.append(ClickZone(self.frame, pygame.MOUSEBUTTONUP, self.clickAction))
        self.view.surface.blit(self.image, self.frame)
    
    def clickAction(self, event):
        if self.action is not None:
            self.action(self)

class ToggleButton:
    def __init__(self, view, position, offImageName, onImageName, action):
        self.view = view
        self.offImage = pygame.image.load(offImageName).convert()
        self.onImage = pygame.image.load(onImageName).convert()
        self.action = action
        self.state = False
        self.frame = pygame.Rect(position, self.offImage.get_size())
        clickZones.append(ClickZone(self.frame, pygame.MOUSEBUTTONUP, self.clickAction))
        self.view.surface.blit(self.offImage, self.frame)
    
    def clickAction(self, event):
        if self.state:
            self.state = False
            self.view.surface.blit(self.offImage, self.frame)
        else:
            self.state = True
            self.view.surface.blit(self.onImage, self.frame)
        if self.action is not None:
            self.action(self)
        self.view.needsUpdate()

def confAction(button):
    print("conf")
    
def aideAction(button):
    print("aide")
    
def infosAction(button):
    print("infos")
        
def droiteAction(toggleButton):
    print("Droite")

def gaucheAction(toggleButton):
    print("Gauche")
    
def stopAction(toggleButton):
    print("Stop Deplacement")
        
def videoAction(toggleButton):
    if toggleButton.state:
        print("start video")
    else:
        print("stop video")


mainView = MainView((320, 240), "SVideo_Py")

fond = pygame.image.load("image/fond_vierge.png").convert()
mainView.surface.blit(fond, (0,0))

Button(mainView, (0,2), "image/Conf.png", confAction)
Button(mainView, (10,185), "image/Aide.png", aideAction)
Button(mainView, (280,5), "image/Infos.png", infosAction)
Button(mainView, (270,185), "image/droite.png", droiteAction)
Button(mainView, (220,185), "image/stop.png", stopAction)
Button(mainView, (170,185), "image/gauche.png", gaucheAction)


ToggleButton(mainView, (60,185), "image/Video_Off.png", "image/Video_On.png", videoAction)
##ToggleButton(mainView, (85,185), "image/Led_Off_1.png", "image/Led_On_1.png", ledAction)

pygame.display.flip()
                   
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for clickZone in clickZones:
                clickZone.processEvent(event)
            if event.type == pygame.QUIT:
                continuer = 0
            mainView.update()