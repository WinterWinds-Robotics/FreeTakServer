#######################################################
# 
# ClientReceptionHandler.py
# Python implementation of the Class ClientReceptionHandler
# Generated by Enterprise Architect
# Created on:      19-May-2020 7:17:21 PM
# Original author: Natha Paquette
# 
#######################################################
import time
from xml.dom.minidom import parseString
import threading
from queue import Queue
from logging.handlers import RotatingFileHandler
import logging
import sys
from CreateLoggerController import CreateLoggerController
logger = CreateLoggerController("ClientReceptionHandler").getLogger()
from configuration.ClientReceptionLoggingConstants import ClientReceptionLoggingConstants
loggingConstants = ClientReceptionLoggingConstants()
#TODO: add more rigid exception management

class ClientReceptionHandler:
    def __init__(self):
        self.dataPipe = ''
        self.eventPipe = ''
        self.threadDict = {}
        self.dataArray = []

    def startup(self, dataPipe, eventPipe):
        try:
            self.dataPipe = dataPipe
            self.eventPipe = eventPipe
            threading.Thread(target=self.monitorEventPipe, args=(), daemon=True).start()
            threading.Thread(target=self.returnDataToOrchestrator, args=(), daemon=True).start()
            logger.propagate = False
            logger.info(loggingConstants.CLIENTRECEPTIONHANDLERSTART)
            logger.propagate = True
            while True:
                time.sleep(120)
                logger.info('the number of threads is ' + str(threading.active_count()))
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERSTARTUPERROR+str(e))

    def monitorEventPipe(self):
        while True:
            try:
                while self.eventPipe.poll():
                    command = self.eventPipe.recv()
                    if command[0] == loggingConstants.CREATE:
                        self.createClientMonitor(command[1])
                    elif command[0] == loggingConstants.DESTROY:
                        self.destroyClientMonitor(command[1])
            except Exception as e:
                logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITOREVENTPIPEERROR+str(e))

    def returnDataToOrchestrator(self):
        while True:
            try:
                while len(self.dataArray)>0:
                    value = self.dataArray.pop(0)
                    self.dataPipe.send(value)
            except Exception as e:
                logger.error(loggingConstants.CLIENTRECEPTIONHANDLERRETURNDATATOORCHESTRATORERROR+str(e))

    def createClientMonitor(self, clientInformation):
        try:
            alive = threading.Event()
            alive.set()
            clientMonitorThread = threading.Thread(target=self.monitorForData, args = (clientInformation, alive), daemon=True)
            clientMonitorThread.start()
            self.threadDict[clientInformation.ID] = [clientMonitorThread, alive]
            logger.info(loggingConstants.CLIENTRECEPTIONHANDLERCREATECLIENTMONITORINFO)
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERCREATECLIENTMONITORERROR+str(e))

    def destroyClientMonitor(self, clientInformation):
        try:

            thread = self.threadDict.pop(clientInformation.clientInformation.ID)
            logger.info(thread)
            thread[1].clear()
            thread[0].join()
            logger.info(loggingConstants.CLIENTRECEPTIONHANDLERDESTROYCLIENTMONITORINFO)
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERDESTROYCLIENTMONITORERROR+str(e))

    def monitorForData(self, clientInformation, alive):
        '''
        updated receive all 
        '''
        try:
            try:                
                BUFF_SIZE = 8087
                client = clientInformation.socket
                data = b''
            except Exception as e:
                logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORA+str(e))
                self.returnReceivedData(clientInformation, b'')
            while alive.isSet():
                try:
                    part = client.recv(BUFF_SIZE)
                except OSError as e:
                    logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORB+str(e))
                    self.returnReceivedData(clientInformation, b'')
                    break
                try:
                    if part == b'' or part == None:
                        self.returnReceivedData(clientInformation, b'')
                        break
                    elif len(part) < BUFF_SIZE:
                        # either 0 or end of data
                        data += part 
                        self.returnReceivedData(clientInformation, data)
                        data = b''
                    else:
                        data += part
                except Exception as e:
                    logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORC+str(e))
                    self.returnReceivedData(clientInformation, b'')
                    break
            return 1
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORD+str(e))
            self.returnReceivedData(clientInformation, b'')

    def returnReceivedData(self, clientInformation, data):
        try:
            from model.RawCoT import RawCoT
            RawCoT = RawCoT()
            #print(data)
            RawCoT.clientInformation = clientInformation
            RawCoT.xmlString = data
            self.dataArray.append(RawCoT)

        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERRETURNRECEIVEDDATAERROR+str(e))