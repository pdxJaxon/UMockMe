
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class DeragatoryRemark:

    def getRawRemarkData():
        ParsedData = ""



        return ParsedData



    def stringToJson(rawString):
        iFoundStart = rawString.find("{")

        jsonString = rawString[iFoundStart:]


        obj = ""

        return obj





    def AddRemark(id,name, pointValue):
        #cur.execute("CREATE TABLE DeragatoryRemark(RemarkId int, Name Text, PointValue int)")
        DBLib.DB.AddRemarkDB(id,name, pointValue)






