#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cherrypy
from Client import Client
from cherrypy.process.plugins import Daemonizer

class App(object):
    """
    Объект приложения
    """
    homeDir = os.path.join(os.path.dirname(__file__),'html')
    userName = None
    userPassword = None

    def index(self):
        print self.homeDir
        fileTemplate = open(os.path.join(self.homeDir, 'index.html'), 'rb')
        page=fileTemplate.read()
        fileTemplate.close()
        return page
    index.exposed = True
    
    def default(self, *args, **kwargs):
        return "Неверный URL."
    default.exposed = True

    def findClient(self, accountNum = None):
        page = Client(userName = self.userName , password = self.userPassword)
        return page.findClient(accountNum, year, month)
    clientAccount.exposed = True

    # Другие методы...
    def login(self, userName, userPassword):
        self.userName = userName
        self.userPassword = userPassword
        #...............

if  __name__ == '__main__':
    Appconf = os.path.join(os.path.dirname(__file__), 'App.conf')
    d = Daemonizer(cherrypy.engine)
    d.subscribe()

    cherrypy.quickstart(App(), '',  config = Appconf)
    cherrypy.engine.block()


