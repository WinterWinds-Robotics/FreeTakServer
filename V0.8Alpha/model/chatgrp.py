#######################################################
# 
# chatgrp.py
# Python implementation of the Class chatgrp
# Generated by Enterprise Architect
# Created on:      11-Feb-2020 11:08:10 AM
# Original author: Corvo
# 
#######################################################


class chatgrp:
   def __init__(self, uid0 = None, uid1 = None, id = None, chatType = None):  
       case = {
            'chatToGroup': self.chatToGroupFunc,
            'chatToTeam': self.chatToTeamFunc,
            'chatToAll': self.chatToAllFunc
            }
       case[chatType](uid0 = uid0, uid1 = uid1, id = id)

   # uid0 getter
   
   def chatToTeamFunc(self, uid0, uid1, id):
       self.setuid0(uid0)
       self.setuid1(uid1)
       self.setid(id)

   def chatToGroupFunc(self, uid0, uid1, id):
       self.setuid0(uid0)
       self.setuid1(uid1)
       self.setid(id)
    
   def chatToAllFunc(self, uid0, uid1, id):
       self.setuid0(uid0)
       self.setuid1(uid1)
       self.setid(id)
   
   def getuid0(self):
      return self.uid0 

   # uid0 setter 
   def setuid0(self, uid0=0):  
      self.uid0=uid0 

   # uid1 getter 
   def getuid1(self): 
      return self.uid1 

   # uid1 setter 
   def setuid1(self, uid1=0):  
      self.uid1=uid1 

   # id getter 
   def getid(self): 
      return self.id 

   # id setter 
   def setid(self, id=0):  
      self.id=id 
     
     