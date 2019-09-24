import pygame
from threading import Thread
import socket
import struct

# --- constants ---

ADDR_RASPBERRY = ("10.50.177.17", 8888)
ADDR_LOCAL = ("raspberrypi.local", 8888)
SURFACE_SIZE = (640, 480)

# --- classes ---

class Receiving(Thread):

    def __init__(self):
        Thread.__init__(self)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR_LOCAL)
        try:
            running = True
            while running:
                
                # receive size
                len_str = s.recv(4)
                size = struct.unpack('!i', len_str)[0]
                print('size:', size)
                
                # receive string
                img_str = b''
                while size > 0:
                    if size >= 4096:
                        data = s.recv(4096)
                    else:
                        data = s.recv(size)
                    if not data:
                        break
                    size -= len(data)
                    img_str += data
                print('len:', len(img_str))

                # convert string to surface
                image = pygame.image.fromstring(img_str, SURFACE_SIZE, 'RGB')
                image_rect = image.get_rect(center=self.screen_rect.center)

                # blit
                self.screen.blit(image, image_rect)
                pygame.display.flip()

                # wait for ESC or close window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

        except Exception as e:
            print(e)
        finally:
            # exit
            print("Closing socket and exit")
            s.close()
            pygame.quit()

# --- main ---

Receiving().run()
