#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------#
# Socketservers to provide sensor and videodata #
# Date: 2019.02.04.                             #
# Author: Tibor Borbas                          #
# Platform: Raspberry Pi 3B                     #
#-----------------------------------------------#

from sense_hat import SenseHat
import picamera
import socketserver
import logging
import threading

sensors = SenseHat()
camera = PiCamera()

# Config of logging
logging.basicConfig(level=logging.DEBUG, format='<%(asctime)s>%(name)s: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')

# Functions to retrive sensor data from the sense hat
def getHumidity(n):
    return round(sensors.get_humidity(),n)

def getTemperature(n):
    return round(sensors.get_temperature(),n)

def getPressure(n):
    return round(sensors.get_pressure(),n)

def getCompass(n):
    return round(sensors.get_compass(),n)

# Handling the requests coming for the sensors
class SensorHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('SensorRequestHandler')
        self.logger.debug('init sensor handler...')
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        return
    
    def handle(self):
        # Expand with motion and orientation sensors
        data = str(getTemperature(2)) + str(getHumidity(2)) + str(getPressure(2)) + \
               str(getCompass(2))
        self.wfile.write(data)
        self.logger.debug('Sending sensor data to client...')
        pass

# Handling the requests coming for the video
class VideoHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('VideoRequestHandler')
        self.logger.debug('init video handler...')
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        return
    
    def handle(self):
        pass

# Server class instanced in the main module
class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# main module
if __name__ == '__main__':
    # Define general data
    HOST = 'localhost'
    SENSOR_PORT = 8530
    VIDEO_PORT = 8531
    
    # Set up logging for main module
    logger = logging.getLogger('Main server module')
    logger.info('Sensor server on localhost:8530')
    logger.info('Video server on localhost:8531')

    # Set up server for sensors and start it
    SensorServer = Server((HOST, SENSOR_PORT), SensorHandler)
    SensorThread = threading.Thread(target=SensorServer.serve_forever)
    SensorThread.daemon = True
    SensorThread.start()
    logger.debug('Sensor server started!')

    # Set up server for video and start it
    VideoServer = Server((HOST, VIDEO_PORT), VideoHandler)
    VideoThread = threading.Thread(target=VideoServer.serve_forever)
    VideoThread.daemon = True
    VideoThread.start()
    logger.debug('Video server started!')

    try:
        while True:
            # count the ellapsed time
            pass
        
    except KeyboardInterrupt:
            # Clean up
            SensorServer.shutdown()
            SensorServer.server_close()
            logger.debug('Sensor server closed!')
            VideoServer.shutdown()
            VideoServer.server_close()
            logger.debug('Video server closed!')
