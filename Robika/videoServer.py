#!/usr/bin/env python
import pygame
import pygame.freetype
from pygame.pixelcopy import *
from pygame.locals import *
from threading import Thread
import socket
import struct # to send `int` as  `4 bytes`
import datetime
import time
from random import randint
import numpy as np
import cv2

# --- constants ---

ADDRESS = ("localhost", 8888)

VIDEO_SIZE = (640, 480)

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)

# --- classes ---

class Streaming(Thread):

    def __init__(self):
        Thread.__init__(self)
        pygame.init()
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640);
        self.cam.set(4, 480);
        self.screen = pygame.display.set_mode((640, 480),HWSURFACE | DOUBLEBUF)
        self.image = pygame.surface.Surface(VIDEO_SIZE)
        self.serverfont = pygame.freetype.Font(None, 12)

    def get_image(self):
        retval, frame = self.cam.read()
        #cv2.imshow('Captured image',frame)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        self.image = pygame.surfarray.make_surface(frame)
        # Draw rect and render text on the image
        crect = pygame.draw.rect(self.image, GREEN, (270,190,100,100), 2)
        self.serverfont.render_to(self.image, (20, 20),
                                  "Temp: " + str(randint(20,25)) + " Cdeg",
                                  GREEN)
        self.serverfont.render_to(self.image, (20,35),
                                  "Hum: " + str(randint(30,50)) + " %",
                                  GREEN)
        self.serverfont.render_to(self.image, (20,50),
                                  "Press: " + str(randint(1000,1005)) + " Pa",
                                  GREEN)
        self.serverfont.render_to(self.image, (20,65),
                                  "Dir: " + str(randint(0,359)) + " deg",
                                  GREEN)
        now = datetime.datetime.now()
        self.serverfont.render_to(self.image, (20,80),
                                  "Dtg: " + str(now.replace(microsecond=0)),
                                  GREEN)
        return self.image

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(ADDRESS)
        s.listen(5)
        print("Wait for connection...")
        try:
            sc, info = s.accept()
            print("Video client connected: ", info)
            while True:
                # get image from camera
                image = self.get_image()
                
                # show image on screen
                self.screen.blit(image, (0,0))
                pygame.display.update()
                
                # convert image to string
                img_str = pygame.image.tostring(image, 'RGB')
                print('len: ', len(img_str))

                # send string size
                len_str = struct.pack('!i', len(img_str))
                sc.send(len_str)

                # send string image
                sc.send(img_str)


        except Exception as e:
            print(e)
        finally:
            # exit
            print("Closing socket and exit!")
            sc.close()
            s.close()
            pygame.quit()

# --- main ---
server = Streaming()
server.run()
