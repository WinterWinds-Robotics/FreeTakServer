#######################################################
# 
# track.py
# Python implementation of the Class track
# Generated by Enterprise Architect
# Created on:      11-Feb-2020 11:08:09 AM
# Original author: Corvo
# 
#######################################################


class track:
    def __init__(self):  
        self.course = "0.00000000"
        self.speed = "0.00000000" 
     # speed getter 
    def getspeed(self): 
        return self.speed 
 
     # speed setter 
    def setspeed(self, speed=0):  
        self.speed=speed 

     # course getter 
    def getcourse(self): 
        return self.course 
 
     # course setter 
    def setcourse(self, course=0):  
        self.course=course 
     