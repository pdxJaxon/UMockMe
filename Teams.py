

import sqlite3 as lite
import requests
from bs4 import BeautifulSoup
import re
import datetime
import json
import DBLib



class Team:




    def getNeedsByTeam(city,teamAbr,teamName):

        #todo: Cache this crap

        needs = ""

        timeStamp = datetime.datetime.now().strftime("%f")

        #url = "http://www.nfl.com/widget/draft/2017/tracker/teams/{}/profile?year=2017&team={}&random={}".format(teamAbr,teamName,str(timeStamp))

        #http://www.nfl.com/widget/draft/2017/tracker/teams/pittsburghsteelers/profile?year=2017&team=PIT&random=1496251240000
        url = "http://www.nfl.com/widget/draft/2017/tracker/teams/{}{}/profile?year=2017&team={}&random={}".format(city,teamName,teamAbr,str(timeStamp))



        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        lstNeeds = soup.find("ul", {"id": "team-needs-positions-list"})



        iCount=1
        for li in lstNeeds.find_all('li'):
            if(iCount==1):
                needs=li.text
            else:
                needs+=":" + li.text
            iCount+=1


        return needs








    def getRawTeamData():
        # nfl.draft.tracker.data.teams    = {

        url = "http://www.nfl.com/draft/2017/tracker#dt-tabs:dt-by-grade"

        #url = http://feeds.nfl.com/feeds-rs/teams/2017.json






        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        script = soup.find('script', text=re.compile('nfl\.draft\.tracker\.data'))

        #print(soup)

        #print(script.string)



        # m = re.search("^\s+nfl.global.dt.data\s+=\s+{\"picks\".+",script.string,flags=re.IGNORECASE | re.MULTILINE)
        #m = re.search("^\s+nfl.draft.tracker.data.teams\s+=\s+{\\r\\n", script.string, flags=re.IGNORECASE | re.MULTILINE)


        iFoundStart = script.string.find("nfl.draft.tracker.data.teams")
        iFoundEnd = script.string.find(";",iFoundStart+1)

        ParsedData = script.string[iFoundStart:iFoundEnd]

        #print(ParsedData)

        return ParsedData












    def stringToJson(rawString):


        iFoundStart=rawString.find("{")

        jsonString = rawString[iFoundStart:]



        #print(jsonString)
        obj = json.loads(jsonString)



        return obj









    #pass in our JSON Data and pump em into the DB
    def AddBatch(jsonData):



            # attributes:
            # {'abbr', 'url', 'city', 'nickName', 'conference', 'division',


            for team in jsonData:
                abbr = jsonData[team]["abbr"]
                url = jsonData[team]["url"].replace("'","''")                #parse any single quotes out of names.....it will blow up our SQL below
                city = jsonData[team]["city"].replace("'","''")               #parse any single quotes out of names.....it will blow up our SQL below
                nickname = jsonData[team]["nickname"]
                conference = jsonData[team]["conference"]
                division = jsonData[team]["division"]
                needs = Team.getNeedsByTeam(city,abbr,nickname)

                #print(abbr,url,city,nickname,conference,division,needs)

                Team.AddTeam(abbr,url,city,nickname,conference,division,needs)









    def AddTeam(abbr,url,city,nickname,conference,division,needs):
        DBLib.DB.AddTeamDB(abbr,url,city,nickname,conference,division,needs)







    #Will return all Teams from DB
    def getAllTeams():
        teams = DBLib.DB.getAllTeams()
        return teams



    def getTeamByAbr(abr):
        team = DBLib.DB.getTeamByAbr(abr)
        return team
