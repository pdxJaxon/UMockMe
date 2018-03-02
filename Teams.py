

import sqlite3 as lite
import requests
from bs4 import BeautifulSoup
import re
import datetime
import json
import DBLib
import os.path




class Team:



    def getStoredNeedsByTeam(teamAbbr):
        needs = DBLib.DB.getAllNeedsForTeam(teamAbbr)
        return needs





    def getNeedsByTeam(city,teamAbr,teamName,year):

        #todo: Cache this crap

        needs = ""

        if(teamAbr=="PIT"):
            # [('CHI', 'CB', 90, 1), ('CHI', 'OL', 85, 1), ('CHI', 'TE', 80, 1), ('CHI', 'LB', 75, 1),('CHI', 'S', 70, 1), ('CHI', 'QB', 65, 1)]
            #needs="[('PIT', 'ILB', 100, 1), ('PIT', 'S', 95, 1), ('PIT', 'EDGE', 80, 1), ('PIT', 'DL', 75, 1),('PIT', 'RB', 75, 1), ('PIT', 'WR', 65, 1)]"
            needs="ILB:S:EDGE:DLN:RB:WR:CB"


        else:



            timeStamp = datetime.datetime.now().strftime("%f")

            #url = "http://www.nfl.com/widget/draft/2017/tracker/teams/{}/profile?year=2017&team={}&random={}".format(teamAbr,teamName,str(timeStamp))

            #http://www.nfl.com/widget/draft/2017/tracker/teams/pittsburghsteelers/profile?year=2017&team=PIT&random=1496251240000
            url = "http://www.nfl.com/widget/draft/{}/tracker/teams/{}{}/profile?year={}&team={}&random={}".format(year,city,teamName,year,teamAbr,str(timeStamp))



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

        print("Needs--->",needs)
        return needs

    def DeleteAllTeamNeeds():
        DBLib.DB.DeleteAllTeamNeeds()


    def RefreshTeamNeeds():

        Team.DeleteAllTeamNeeds()

        Teams = Team.getAllTeamsAsJSON()




        #for each team call getNeedsByTeam2()
        for t in Teams:

            t=json.dumps(t)

            t=json.loads(t)

            needs=Team.getNeedsByTeam2(t['City'],t['Abbr'],t['Nickname'],"2018")

            needs = json.dumps(needs)
            needs=json.loads(needs)


            #for each need, Save to DB
            for n in needs:
                print("N:",n)
                Team.AddTeamNeed(n['Abbr'],n['Pos'],n['Score'],n['Count'])




    def getNeedsByTeam2(city,teamAbr,teamName,year):

        #Hard coding this shit because we were screen scraping from nfl.com and their needs were complete SHIT.

        #This Data Coming from www.drafttek.com/teamneeds2018.asp


        #todo: Cache this crap

        needs = ""

        if(teamAbr=="ARI"):
            needs = [('ARI', 'QB', 100, 1), ('ARI', 'WR', 90, 1), ('ARI', 'OLG', 80, 1), ('ARI', 'TE', 75, 1),('ARI', 'OLC', 75, 1), ('ARI', 'RB', 30, 1),('ARI','EDGE',80,1),('ARI','DLT',80,1),('ARI','ILB',75,1),('ARI','CB',90,1)]
        elif(teamAbr=="ATL"):
            needs = [('ATL', 'ILB', 100, 1)]
        elif (teamAbr == "BAL"):
            needs = [('BAL', 'ILB', 100, 1)]
        elif (teamAbr == "BUF"):
            needs = [('BUF', 'ILB', 100, 1)]
        elif (teamAbr == "CAR"):
            needs = [('CAR', 'ILB', 100, 1)]
        elif (teamAbr == "CHI"):
            needs = [('CHI', 'ILB', 100, 1)]
        elif (teamAbr == "CIN"):
            needs = [('CIN', 'ILB', 100, 1)]
        elif (teamAbr == "CLE"):
            needs = [('CLE', 'ILB', 100, 1)]
        elif (teamAbr == "DAL"):
            needs = [('DAL', 'ILB', 100, 1)]
        elif (teamAbr == "DEN"):
            needs = [('DEN', 'ILB', 100, 1)]
        elif (teamAbr == "DET"):
            needs = [('DET', 'ILB', 100, 1)]
        elif (teamAbr == "GB"):
            needs = [('GB', 'ILB', 100, 1)]
        elif (teamAbr == "HOU"):
            needs = [('HOU', 'ILB', 100, 1)]
        elif (teamAbr == "IND"):
            needs = [('IND', 'ILB', 100, 1)]
        elif (teamAbr == "JAX"):
            needs = [('JAX', 'ILB', 100, 1)]
        elif (teamAbr == "KC"):
            needs = [('KC', 'ILB', 100, 1)]
        elif (teamAbr == "MIA"):
            needs = [('MIA', 'ILB', 100, 1)]
        elif (teamAbr == "MIN"):
            needs = [('MIN', 'ILB', 100, 1)]
        elif (teamAbr == "NE"):
            needs = [('NE', 'ILB', 100, 1)]
        elif (teamAbr == "NO"):
            needs = [('NO', 'ILB', 100, 1)]
        elif (teamAbr == "NYG"):
            needs = [('NYG', 'ILB', 100, 1)]
        elif (teamAbr == "NYJ"):
            needs = [('NYJ', 'ILB', 100, 1)]
        elif (teamAbr == "OAK"):
            needs = [('OAK', 'ILB', 100, 1)]
        elif (teamAbr == "PHI"):
            needs = [('PHI', 'ILB', 100, 1)]
        elif (teamAbr == "PIT"):
            needs=[('PIT', 'ILB', 100, 1), ('PIT', 'S', 95, 1), ('PIT', 'EDGE', 80, 1), ('PIT', 'DL', 75, 1),('PIT', 'RB', 80, 1), ('PIT', 'WR', 75, 1),('PIT','TE',70,1)]
        elif (teamAbr == "LA"):
            needs = [('LA', 'ILB', 100, 1)]
        elif (teamAbr == "LAR"):
            needs = [('LAR', 'ILB', 100, 1)]
        elif (teamAbr == "SF"):
            needs = [('SF', 'ILB', 100, 1)]
        elif (teamAbr == "SEA"):
            needs = [('SEA', 'ILB', 100, 1)]
        elif (teamAbr == "TB"):
            needs = [('TB', 'ILB', 100, 1)]
        elif (teamAbr == "TEN"):
            needs = [('TEN', 'ILB', 100, 1)]
        elif (teamAbr == "WAS"):
            needs = [('WAS', 'ILB', 100, 1)]
        else:
            needs=""


        columns = ('Abbr', 'Pos', 'Score','Count')

        results = []

        for n in needs:
            results.append(dict(zip(columns, n)))


        return results





    def getRawTeamData():
        # nfl.draft.tracker.data.teams    = {



        parsedData=""



        url = "http://www.nfl.com/draft/2017/tracker#dt-tabs:dt-by-grade"

        #url = http://feeds.nfl.com/feeds-rs/teams/2017.json



        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        script = soup.find('script', text=re.compile('nfl\.draft\.tracker\.data'))

        #print(soup)

        #print(script.string)

        print("Team Data Web Scraped");

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




    def AddNeedsForTeam(abbr,city,nickname,year,draftId):

        allPositions = ["OLG","OLT","OLC","DLN","DLE","DLT", "QB", "WR", "TE", "RB","FB", "LB","EDGE","OLB","ILB","CB", "S","P","K","FS","SS","LS"]


        needs = Team.getNeedsByTeam2(city, abbr, nickname, year)

        for n in needs:
            Team.AddTeamNeed(abbr, n, n, 1)


        #IF NEED NOT LISTED AT ALL, WE MARK IT AS A 50 (AVERAGE - TAKE IT OR LEAVE IT)
        for p in allPositions:
            if (p not in needs):
                Team.AddTeamNeed(abbr, p, 50, 1)








    #pass in our JSON Data and pump em into the DB
    def AddBatch(jsonData,year):




            # attributes:
            # {'abbr', 'url', 'city', 'nickName', 'conference', 'division',


            for team in jsonData:
                abbr = jsonData[team]["abbr"]
                url = jsonData[team]["url"].replace("'","''")                #parse any single quotes out of names.....it will blow up our SQL below
                city = jsonData[team]["city"].replace("'","''")               #parse any single quotes out of names.....it will blow up our SQL below
                nickname = jsonData[team]["nickname"]
                conference = jsonData[team]["conference"]
                division = jsonData[team]["division"]



                Team.AddTeam(abbr,url,city,nickname,conference,division)

                print("Team Added",abbr)

                if(year==2017):
                    draftId=1
                else:
                    draftId=2


                Team.AddNeedsForTeam(abbr,city,nickname,year,draftId)








    def AddTeamNeed(abbr,need,score,count,draftId=2):
        DBLib.DB.AddTeamNeedDB(abbr,need,score,count,draftId)





    def AddTeam(abbr,url,city,nickname,conference,division):
        DBLib.DB.AddTeamDB(abbr,url,city,nickname,conference,division)




    def getTeamNeeds(abbr,draftId):
        needs = DBLib.DB.getAllNeedsForTeam(abbr,draftId)
        return needs





    #Will return all Teams from DB
    def getAllTeams():
        teams = DBLib.DB.getAllTeams()
        return teams


    def getAllTeamsAsJSON():
        teams = DBLib.DB.getAllTeamsAsJSON()

        return teams







    def getTeamByAbr(abr):
        team = DBLib.DB.getTeamByAbr(abr)
        return team
