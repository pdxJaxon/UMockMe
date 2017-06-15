


import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class College:


    def getCollegeData():
        #nfl.global.dt.data.colleges			= {
        url = "http://www.nfl.com/draft/2017/tracker#dt-tabs:dt-by-grade"

        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        script = soup.find('script', text=re.compile('nfl\.global\.dt\.data\.colleges'))


        iFoundStart = script.string.find("nfl.global.dt.data.colleges")
        iFoundEnd = script.string.find(";",iFoundStart+1)

        ParsedData = script.string[iFoundStart:iFoundEnd]

        #print(ParsedData)

        return ParsedData



    def stringToJson(rawString):
        iFoundStart = rawString.find("{")

        jsonString = rawString[iFoundStart:]


        obj = json.loads(jsonString)

        return obj




     # pass in our JSON Data and pump em into the DB
    def AddBatch(jsonData):
        # attributes:
        # {id,name,conference}


        for college in jsonData:
            id = jsonData[college]["id"]
            name = jsonData[college]["name"].replace("'",
                                                    "''")  # parse any single quotes out of names.....it will blow up our SQL below
            conference = jsonData[college]["conf"]

            # print(id,name,conference)

            College.AddCollege(id,name,conference)


    def getCollegeById(id=-1):
        college = DBLib.DB.GetCollegeById(id)

        if(college):
            return college
        else:
            return [{-1,"Unknown",""}]







    def AddCollege(id,name, conference):
        DBLib.DB.AddCollegeDB(id,name, conference)






    # Will return all Teams from DB
    def getAllColleges():
        colleges = DBLib.DB.getAllColleges()
        return colleges

