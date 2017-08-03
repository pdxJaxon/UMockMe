
import requests


import DBLib
import Teams




class User:


    def ValidateLogin(email,password):
        usr=DBLib.DB.getUserByEmailAndPassword(email,password)
        return usr







    def AddUser(email,fname,lname,userName,Password,TeamAbbr):

        DBLib.DB.AddUser(email,userName,Password,TeamAbbr,fname,lname)

        u = DBLib.DB.getUserByEmail(email)

        return u

