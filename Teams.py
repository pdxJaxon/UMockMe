
#this is a comment by GreggyPoo

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

        retVal = Team.getNeedsByTeam2(city,teamAbr,teamName,year)

        return retVal






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

                Team.AddTeamNeed(n['Abbr'],n['Pos'],n['Score'],n['Count'])




    def getNeedsByTeam2(teamAbr,year=2018):

        #Hard coding this shit because we were screen scraping from nfl.com and their needs were complete SHIT.

        #This Data Coming from www.drafttek.com/teamneeds2018.asp


        #todo: Cache this crap

        needs = ""

        if(teamAbr=="ARI"):
            needs = [('ARI', 'QB', 100, 1), ('ARI', 'WR', 90, 1), ('ARI', 'OLG', 80, 1), ('ARI', 'TE', 75, 1),('ARI', 'OLC', 75, 1), ('ARI', 'RB', 30, 1),('ARI','EDGE',80,1),('ARI','DLT',80,1),('ARI','ILB',75,1),('ARI','CB',90,1)]
        elif(teamAbr=="ATL"):
            needs = [('ATL', 'WR', 90, 1),('ATL', 'TE', 90, 1),('ATL', 'OLG', 90, 1),('ATL', 'OLT', 70, 1),('ATL', 'CB', 90, 1),('ATL', 'DLN', 90, 1),('ATL', 'DLT', 80, 1),('ATL', 'OLB', 80, 1),('ATL', 'DLE', 90, 1),('ATL', 'EDGE', 60, 1),('ATL', 'ILB', 60, 1)]
        elif (teamAbr == "BAL"):
            needs = [('BAL', 'DLE', 100, 1),('BAL', 'S', 70, 1),('BAL', 'CB', 70, 1),('BAL', 'WR', 100, 2),('BAL', 'TE', 80, 1),('BAL', 'OLT', 80, 1),('BAL', 'OLG', 80, 1),('BAL', 'OLC', 60, 1)]
        elif (teamAbr == "BUF"):
            needs = [('BUF', 'QB', 100, 1),('BUF', 'RB', 80, 1),('BUF', 'WR', 90, 1),('BUF', 'OLG', 90, 1),('BUF', 'OLC', 90, 1),('BUF', 'TE', 60, 1),('BUF', 'OLT', 80, 1),('BUF', 'ILB', 90, 1),('BUF', 'OLB', 90, 1),('BUF', 'EDGE', 80, 1),('BUF', 'DLT', 90, 1),('BUF', 'DLN', 90, 1),('BUF', 'CB', 70, 1)]
        elif (teamAbr == "CAR"):
            needs = [('CAR', 'RB', 70, 1),('CAR', 'WR', 80, 1),('CAR', 'OLT', 70, 1),('CAR', 'OLG', 70, 1),('CAR', 'TE', 70, 1),('CAR', 'OLC', 80, 1),('CAR', 'EDGE', 80, 1),('CAR', 'OLB', 70, 1),('CAR', 'S', 80, 1),('CAR', 'CB', 70, 1)]
        elif (teamAbr == "CHI"):
            needs = [('CHI', 'DLN', 70, 1),('CHI', 'DLE', 80, 1),('CHI', 'EDGE', 70, 1),('CHI', 'OLB', 70, 1),('CHI', 'ILB', 90, 1),('CHI', 'S', 70, 1),('CHI', 'CB', 90, 1)]
        elif (teamAbr == "CIN"):
            needs = [('CIN', 'OLB', 90, 1),('CIN', 'S', 80, 1),('CIN', 'QB', 70, 1),('CIN', 'OLT', 100, 1),('CIN', 'OLG', 90, 1),('CIN', 'TE', 80, 1),('CIN', 'OLC', 80, 1)]
        elif (teamAbr == "CLE"):
            needs = [('CLE', 'QB', 100, 1),('CLE', 'RB', 90, 1),('CLE', 'WR', 90, 1),('CLE', 'OLT', 80, 1),('CLE', 'TE', 70, 1),('CLE', 'DLT', 90, 1),('CLE', 'ILB', 70, 1),('CLE', 'S', 80, 1),('CLE', 'CB', 90, 1)]
        elif (teamAbr == "DAL"):
            needs = [('DAL', 'WR', 80, 1),('DAL', 'OLT', 80, 1),('DAL', 'OLG', 70, 1),('DAL', 'TE', 60, 1),('DAL', 'DLN', 80, 1),('DAL', 'DLT', 60, 1),('DAL', 'EDGE', 80, 1),('DAL', 'CB', 80, 1),('DAL', 'S', 60, 1),('DAL', 'OLB', 60, 1),('DAL', 'ILB', 60, 1)]
        elif (teamAbr == "DEN"):
            needs = [('DEN', 'QB', 100, 1),('DEN', 'RB', 70, 1),('DEN', 'OLT', 90, 1),('DEN', 'OLG', 80, 1),('DEN', 'DLN', 80, 1),('DEN', 'EDGE', 70, 1),('DEN', 'ILB', 90, 1),('DEN', 'S', 90, 1),('DEN', 'CB', 90, 1)]
        elif (teamAbr == "DET"):
            needs = [('DET', 'RB', 90, 2),('DET', 'OLG', 90, 1),('DET', 'OLC', 90, 1),('DET', 'TE', 90, 1),('DET', 'OLT', 90, 1),('DET', 'DLT', 70, 1),('DET', 'DLE', 70, 1),('DET', 'EDGE', 60, 1),('DET', 'OLB', 80, 1),('DET', 'ILB', 60, 1),('DET', 'S', 80, 1),('DET', 'CB', 80, 1)]
        elif (teamAbr == "GB"):
            needs = [('GB', 'WR', 80, 1),('GB', 'OLT', 70, 1),('GB', 'TE', 70, 1),('GB', 'EDGE', 90, 1),('GB', 'CB', 90, 1),('GB', 'ILB', 60, 1),('GB', 'DLE', 60, 1)]
        elif (teamAbr == "HOU"):
            needs = [('HOU', 'OLT', 80, 1),('HOU', 'OLG', 80, 1),('HOU', 'TE', 70, 1),('HOU', 'ILB', 70, 1),('HOU', 'OLB', 70, 1),('HOU', 'EDGE', 70, 1),('HOU', 'S', 80, 1),('HOU', 'CB', 70, 1)]
        elif (teamAbr == "IND"):
            needs = [('IND', 'RB', 70, 1),('IND', 'WR', 70, 2),('IND', 'OLT', 90, 1),('IND', 'OLG', 90, 1),('IND', 'TE', 70, 1),('IND', 'DLN', 70, 1),('IND', 'DLT', 70, 1),('IND', 'DLE', 70, 1),('IND', 'EDGE', 90, 1),('IND', 'OLB', 70, 1),('IND', 'ILB', 80, 1),('IND', 'S', 70, 1),('IND', 'CB', 90, 1)]
        elif (teamAbr == "JAX"):
            needs = [('JAX', 'QB', 80, 1),('JAX', 'WR', 90, 2),('JAX', 'OLT', 70, 1),('JAX', 'OLG', 80, 1),('JAX', 'TE', 80, 1),('JAX', 'OLC', 70, 1),('JAX', 'DLN', 80, 1),('JAX', 'DLT', 70, 1),('JAX', 'DLE', 70, 1),('JAX', 'EDGE', 80, 1),('JAX', 'OLB', 70, 1),('JAX', 'ILB', 80, 1),('JAX', 'S', 70, 1),('JAX', 'CB', 80, 1)]
        elif (teamAbr == "KC"):
            needs = [('KC', 'QB', 70, 1),('KC', 'WR', 70, 1),('KC', 'OLT', 70, 1),('KC', 'OLG', 80, 1),('KC', 'TE', 70, 1),('KC', 'DLN', 80, 1),('KC', 'DLE', 80, 1),('KC', 'EDGE', 80, 1),('KC', 'OLB', 70, 1),('KC', 'ILB', 80, 1),('KC', 'S', 80, 1),('KC', 'CB', 80, 1)]
        elif (teamAbr == "MIA"):
            needs = [('MIA', 'QB', 70, 1),('MIA', 'RB', 80, 2),('MIA', 'WR', 70, 1),('MIA', 'OLT', 80, 1),('MIA', 'OLG', 100, 1),('MIA', 'TE', 90, 1),('MIA', 'OLC', 70, 1),('MIA', 'DLT', 90, 1),('MIA', 'DLE', 70, 1),('MIA', 'EDGE', 70, 1),('MIA', 'OLB', 70, 1),('MIA', 'ILB', 70, 1),('MIA', 'S', 80, 1),('MIA', 'CB', 80, 1)]
        elif (teamAbr == "MIN"):
            needs = [('MIN', 'WR', 70, 1),('MIN', 'OLT', 70, 1),('MIN', 'OLG', 80, 1),('MIN', 'TE', 60, 1),('MIN', 'DLN', 70, 1),('MIN', 'DLT', 80, 1),('MIN', 'EDGE', 60, 1),('MIN', 'OLB', 70, 1),('MIN', 'S', 70, 1),('MIN', 'CB', 80, 1)]
        elif (teamAbr == "NE"):
            needs = [('NE', 'QB', 80, 1),('NE', 'WR', 80, 2),('NE', 'OLT', 90, 1),('NE', 'OLG', 80, 1),('NE', 'TE', 70, 1),('NE', 'DLN', 80, 1),('NE', 'DLT', 90, 1),('NE', 'EDGE', 100, 1),('NE', 'OLB', 90, 1),('NE', 'ILB', 90, 1),('NE', 'S', 70, 1),('NE', 'CB', 90, 1)]
        elif (teamAbr == "NO"):
            needs = [('NO', 'RB', 70, 1),('NO', 'WR', 70, 1),('NO', 'OLT', 70, 1),('NO', 'OLG', 90, 1),('NO', 'TE', 80, 1),('NO', 'OLC', 70, 1),('NO', 'DLN', 70, 1),('NO', 'DLT', 70, 1),('NO', 'DLE', 70, 1),('NO', 'EDGE', 70, 1),('NO', 'OLB', 90, 1),('NO', 'ILB', 80, 1),('NO', 'S', 80, 1),('NO', 'CB', 70, 1)]
        elif (teamAbr == "NYG"):
            needs = [('NYG', 'QB', 80, 1),('NYG', 'RB', 70, 2),('NYG', 'OLT', 80, 1),('NYG', 'OLG', 80, 1),('NYG', 'OLC', 60, 1),('NYG', 'DLN', 70, 1),('NYG', 'EDGE', 80, 1),('NYG', 'OLB', 70, 1),('NYG', 'ILB', 70, 1),('NYG', 'CB', 80, 1)]
        elif (teamAbr == "NYJ"):
            needs = [('NYJ', 'QB', 100, 1),('NYJ', 'RB', 80, 1),('NYJ', 'OLT', 90, 1),('NYJ', 'OLG', 80, 1),('NYJ', 'TE', 80, 1),('NYJ', 'OLC', 90, 1),('NYJ', 'EDGE', 90, 1),('NYJ', 'ILB', 80, 1),('NYJ', 'CB', 90, 1)]
        elif (teamAbr == "OAK"):
            needs = [('OAK', 'RB', 80, 1),('OAK', 'WR', 80, 1),('OAK', 'OLT', 80, 1),('OAK', 'DLT', 80, 1),('OAK', 'EDGE', 80, 1),('OAK', 'OLB', 90, 1),('OAK', 'ILB', 90, 1),('OAK', 'CB', 100, 1)]
        elif (teamAbr == "PHI"):
            needs = [('PHI', 'RB', 80, 1),('PHI', 'WR', 80, 1),('PHI', 'OLT', 100, 1),('PHI', 'OLG', 70, 1),('PHI', 'OLC', 60, 1),('PHI', 'EDGE', 70, 1),('PHI', 'ILB', 90, 1),('PHI', 'CB', 70, 1)]
        elif (teamAbr == "PIT"):
            needs=[('PIT', 'ILB', 100, 1), ('PIT', 'S', 90, 1),('PIT', 'CB', 70, 1), ('PIT', 'EDGE', 90, 1), ('PIT', 'DLN', 70, 1),('PIT', 'RB', 70, 1), ('PIT', 'WR', 80, 1),('PIT','TE',70,1),('PIT', 'OLG', 50, 1),('PIT', 'OLC', 40, 1)]
        elif (teamAbr == "LA"):
            needs = [('LA', 'QB', 80, 1),('LA', 'OLT', 90, 1),('LA', 'OLC', 70, 1),('LA', 'DLN', 90, 1),('LA', 'ILB', 80, 1),('LA', 'S', 80, 1),('LA', 'CB', 70, 1)]
        elif (teamAbr == "LAR"):
            needs = [('LAR', 'RB', 70, 1),('LAR', 'OLG', 80, 1),('LAR', 'OLC', 70, 1),('LAR', 'DLN', 70, 1),('LAR', 'DLT', 70, 1),('LAR', 'EDGE', 80, 1),('LAR', 'ILB', 90, 1),('LAR', 'S', 80, 1),('LAR', 'CB', 70, 1)]
        elif (teamAbr == "SF"):
            needs = [('SF', 'RB', 70, 1),('SF', 'WR', 90, 1),('SF', 'OLG', 100, 1),('SF', 'OLC', 90, 1),('SF', 'DLN', 80, 1),('SF', 'EDGE', 90, 1),('SF', 'OLB', 80, 1),('SF', 'CB', 90, 1)]
        elif (teamAbr == "SEA"):
            needs = [('SEA', 'OLT', 70, 1),('SEA', 'OLG', 90, 1),('SEA', 'TE', 70, 1),('SEA', 'DLE', 80, 1),('SEA', 'EDGE', 90, 1),('SEA', 'CB', 70, 1)]
        elif (teamAbr == "TB"):
            needs = [('TB', 'DLT', 80, 1),('TB', 'DLE', 70, 1),('TB', 'DLN', 70, 1),('TB', 'EDGE', 100, 1),('TB', 'OLB', 70, 1),('TB', 'ILB', 70, 1),('TB', 'S', 70, 1),('TB', 'CB', 90, 1),('TB', 'RB', 90, 1),('TB', 'WR', 80, 1),('TB', 'OLG', 90, 1)]
        elif (teamAbr == "TEN"):
            needs = [('TEN', 'RB', 70, 1),('TEN', 'WR', 70, 1),('TEN', 'TE', 70, 1),('TEN', 'EDGE', 80, 1),('TEN', 'ILB', 70, 1),('TEN', 'S', 70, 1),('TEN', 'CB', 100, 1)]
        elif (teamAbr == "WAS"):
            needs = [('WAS', 'RB', 90, 1),('WAS', 'WR', 90, 1),('WAS', 'OLT', 70, 1),('WAS', 'OLG', 90, 1),('WAS', 'TE', 80, 1),('WAS', 'OLC', 70, 1),('WAS', 'DLN', 90, 1),('WAS', 'DLT', 90, 1),('WAS', 'DLE', 90, 1),('WAS', 'EDGE', 90, 1),('WAS', 'OLB', 90, 1),('WAS', 'ILB', 90, 1),('WAS', 'S', 90, 1),('WAS', 'CB', 90, 1)]
        else:
            needs=""


        columns = ('Abbr', 'need', 'needScore','Count')

        results = []

        for n in needs:
            results.append(dict(zip(columns, n)))

        #results.sort("needScore")


        return results




    def getNeedsForAllTeams2():

        #Hard coding this shit because we were screen scraping from nfl.com and their needs were complete SHIT.

        #This Data Coming from www.drafttek.com/teamneeds2018.asp


        #todo: Cache this crap

        needs = ""


        needs = [('ARI', 'QB', 90, 1), ('ARI', 'WR', 90, 1), ('ARI', 'OLG', 80, 1), ('ARI', 'TE', 75, 1),('ARI', 'OLC', 75, 1), ('ARI', 'RB', 30, 1),('ARI','EDGE',30,1),('ARI','DLT',80,1),('ARI','ILB',40,1),('ARI','CB',90,1)]

        needs += [('ATL', 'WR', 90, 1),('ATL', 'TE', 90, 1),('ATL', 'OLG', 40, 1),('ATL', 'OLT', 80, 1),('ATL', 'CB', 70, 1),('ATL', 'DLN', 90, 1),('ATL', 'DLT', 90, 1),('ATL', 'OLB', 80, 1),('ATL', 'DLE', 70, 1),('ATL', 'EDGE', 70, 1),('ATL', 'ILB', 50, 1)]

        needs += [('BAL', 'DLE', 90, 1),('BAL', 'S', 70, 1),('BAL', 'CB', 70, 1),('BAL', 'WR', 90, 1),('BAL', 'TE', 80, 1),('BAL', 'OLT', 80, 1),('BAL', 'OLG', 70, 1),('BAL', 'OLC', 70, 1)]

        needs += [('BUF', 'QB', 100, 1),('BUF', 'RB', 90, 1),('BUF', 'WR', 90, 1),('BUF', 'OLG', 90, 1),('BUF', 'OLC', 60, 1),('BUF', 'TE', 90, 1),('BUF', 'OLT', 80, 1),('BUF', 'ILB', 90, 1),('BUF', 'OLB', 90, 1),('BUF', 'EDGE', 80, 1),('BUF', 'DLT', 80, 1),('BUF', 'DLN', 90, 1),('BUF', 'CB', 70, 1)]

        needs += [('CAR', 'RB', 80, 1),('CAR', 'WR', 80, 1),('CAR', 'OLT', 70, 1),('CAR', 'OLG', 70, 1),('CAR', 'TE', 70, 1),('CAR', 'OLC', 80, 1),('CAR', 'EDGE', 80, 1),('CAR', 'OLB', 70, 1),('CAR', 'S', 80, 1),('CAR', 'CB', 80, 1)]

        needs += [('CHI', 'QB', 700, 1),('CHI', 'RB', 70, 1),('CHI', 'WR', 90, 1),('CHI', 'OLG', 80, 1),('CHI', 'DLN', 70, 1),('CHI', 'DLN', 70, 1),('CHI', 'DLE', 80, 1),('CHI', 'EDGE', 70, 1),('CHI', 'OLB', 70, 1),('CHI', 'ILB', 90, 1),('CHI', 'S', 70, 1),('CHI', 'CB', 90, 1)]

        needs += [('CIN', 'EDGE', 80, 1),('CIN', 'OLB', 70, 1),('CIN', 'ILB', 80, 1),('CIN', 'CB', 60, 1),('CIN', 'S', 80, 1),('CIN', 'QB', 70, 1),('CIN', 'OLT', 100, 1),('CIN', 'OLG', 90, 1),('CIN', 'TE', 80, 1),('CIN', 'OLC', 80, 1)]

        needs += [('CLE', 'QB', 100, 1),('CLE', 'RB', 90, 1),('CLE', 'WR', 80, 1),('CLE', 'OLT', 80, 1),('CLE', 'TE', 50, 1),('CLE', 'DLT', 90, 1),('CLE','DLN',90,1),('CLE', 'ILB', 60, 1),('CLE', 'S', 80, 1),('CLE', 'CB', 90, 1)]

        needs += [('DAL', 'WR', 90, 1),('DAL', 'OLT', 60, 1),('DAL', 'OLG', 80, 1),('DAL', 'TE', 40, 1),('DAL', 'DLN', 60, 1),('DAL', 'DLT', 60, 1),('DAL', 'EDGE', 60, 1),('DAL', 'CB', 70, 1),('DAL', 'S', 80, 1),('DAL', 'OLB', 80, 1),('DAL', 'ILB', 80, 1)]

        needs += [('DEN', 'QB', 90, 1),('DEN', 'RB', 70, 1),('DEN', 'OLT', 100, 1),('DEN', 'OLG', 90, 1),('DEN', 'DLT', 90, 1),('DEN', 'EDGE', 80, 1),('DEN', 'ILB', 40, 1),('DEN', 'S', 90, 1),('DEN', 'CB', 90, 1)]

        needs += [('DET', 'RB', 60, 2),('DET', 'OLG', 90, 1),('DET', 'OLC', 60, 1),('DET', 'TE', 100, 1),('DET', 'OLT', 90, 1),('DET', 'DLT', 70, 1),('DET', 'DLE', 70, 1),('DET', 'EDGE', 80, 1),('DET', 'OLB', 50, 1),('DET', 'ILB', 50, 1),('DET', 'S', 60, 1),('DET', 'CB', 50, 1)]

        needs += [('GB', 'WR', 80, 1),('GB', 'OLT', 70, 1),('GB', 'TE', 70, 1),('GB', 'EDGE', 90, 1),('GB', 'CB', 90, 1),('GB', 'ILB', 60, 1),('GB', 'S', 70, 1)]

        needs += [('HOU', 'OLT', 80, 1),('HOU', 'OLG', 80, 1),('HOU', 'TE', 70, 1),('HOU', 'ILB', 70, 1),('HOU', 'OLB', 70, 1),('HOU', 'EDGE', 70, 1),('HOU', 'S', 80, 1),('HOU', 'CB', 70, 1)]

        needs += [('IND', 'RB', 70, 1),('IND', 'WR', 70, 2),('IND', 'OLT', 90, 1),('IND', 'OLG', 90, 1),('IND', 'TE', 70, 1),('IND', 'DLN', 70, 1),('IND', 'DLT', 70, 1),('IND', 'DLE', 70, 1),('IND', 'EDGE', 90, 1),('IND', 'OLB', 90, 1),('IND', 'ILB', 90, 1),('IND', 'S', 70, 1),('IND', 'CB', 90, 1)]

        needs += [('JAX', 'QB', 70, 1),('JAX', 'WR', 90, 2),('JAX', 'OLT', 70, 1),('JAX', 'OLG', 80, 1),('JAX', 'TE', 80, 1),('JAX', 'OLC', 70, 1),('JAX', 'DLN', 80, 1),('JAX', 'DLT', 70, 1),('JAX', 'DLE', 70, 1),('JAX', 'EDGE', 80, 1),('JAX', 'OLB', 70, 1),('JAX', 'ILB', 80, 1),('JAX', 'S', 70, 1),('JAX', 'CB', 80, 1)]

        needs += [('KC', 'QB', 70, 1),('KC', 'WR', 60, 1),('KC', 'OLT', 70, 1),('KC', 'OLG', 80, 1),('KC', 'TE', 70, 1),('KC', 'DLN', 80, 1),('KC', 'DLE', 80, 1),('KC', 'EDGE', 80, 1),('KC', 'OLB', 80, 1),('KC', 'ILB', 20, 1),('KC', 'S', 80, 1),('KC', 'CB', 90, 1)]

        needs += [('MIA', 'QB', 70, 1),('MIA', 'RB', 80, 2),('MIA', 'WR', 70, 1),('MIA', 'OLT', 60, 1),('MIA', 'OLG', 60, 1),('MIA', 'TE', 90, 1),('MIA', 'OLC', 70, 1),('MIA', 'DLT', 90, 1),('MIA', 'DLE', 70, 1),('MIA', 'EDGE', 50, 1),('MIA', 'OLB', 100, 1),('MIA', 'ILB', 70, 1),('MIA', 'S', 80, 1),('MIA', 'CB', 80, 1)]

        needs += [('MIN', 'WR', 70, 1),('MIN', 'OLT', 70, 1),('MIN', 'OLG', 80, 1),('MIN', 'TE', 50, 1),('MIN', 'DLN', 70, 1),('MIN', 'DLT', 70, 1),('MIN', 'EDGE', 60, 1),('MIN', 'OLB', 70, 1),('MIN', 'S', 70, 1),('MIN', 'CB', 80, 1)]

        needs += [('NE', 'QB', 100, 1),('NE', 'WR', 90, 2),('NE', 'OLT', 90, 1),('NE', 'OLG', 50, 1),('NE', 'TE', 80, 1),('NE', 'DLN', 80, 1),('NE', 'DLT', 90, 1),('NE', 'EDGE', 90, 1),('NE', 'OLB', 80, 1),('NE', 'ILB', 90, 1),('NE', 'S', 70, 1),('NE', 'CB', 90, 1)]

        needs += [('NO', 'RB', 70, 1),('NO', 'WR', 70, 1),('NO', 'OLT', 80, 1),('NO', 'OLG', 90, 1),('NO', 'TE', 90, 1),('NO', 'OLC', 70, 1),('NO', 'DLN', 70, 1),('NO', 'DLT', 70, 1),('NO', 'DLE', 70, 1),('NO', 'EDGE', 80, 1),('NO', 'OLB', 90, 1),('NO', 'ILB', 70, 1),('NO', 'S', 70, 1),('NO', 'CB', 70, 1)]

        needs += [('NYG', 'QB', 70, 1),('NYG', 'RB', 80, 2),('NYG', 'OLT', 80, 1),('NYG', 'OLG', 80, 1),('NYG', 'OLC', 60, 1),('NYG', 'DLN', 70, 1),('NYG', 'EDGE', 80, 1),('NYG', 'OLB', 80, 1),('NYG', 'ILB', 70, 1),('NYG', 'CB', 90, 1)]

        needs += [('NYJ', 'QB', 100, 1),('NYJ', 'WR', 70, 1),('NYJ', 'OLT', 90, 1),('NYJ', 'OLG', 80, 1),('NYJ', 'TE', 90, 1),('NYJ', 'OLC', 60, 1),('NYJ', 'EDGE', 90, 1),('NYJ', 'DLT', 90, 1),('NYJ', 'CB', 50, 1)]

        needs += [('OAK', 'TE', 860, 1),('OAK', 'WR', 90, 1),('OAK', 'OLT', 90, 1),('OAK', 'DLG', 80, 1),('OAK', 'EDGE', 80, 1),('OAK', 'OLB', 90, 1),('OAK', 'ILB', 90, 1),('OAK', 'CB', 90, 1)]

        needs += [('PHI', 'RB', 80, 1),('PHI', 'WR', 50, 1),('PHI', 'OLT', 100, 1),('PHI', 'OLG', 70, 1),('PHI', 'OLC', 60, 1),('PHI','TE',80,1),('PHI', 'EDGE', 70, 1),('PHI','OLB',80,1),('PHI', 'ILB', 80, 1),('PHI', 'S', 80, 1)]

        needs += [('PIT', 'ILB', 100, 1), ('PIT', 'S', 90, 1),('PIT', 'CB', 80, 1), ('PIT', 'EDGE', 90, 1),('PIT','QB',70), ('PIT', 'DLN', 70, 1),('PIT', 'RB', 60, 1), ('PIT', 'WR', 80, 1),('PIT','TE',70,1),('PIT', 'OLG', 60, 1),('PIT', 'OLC', 40, 1)]

        needs += [('LA', 'QB', 80, 1),('LA','RB',80,1),('LA','WR',70,1),('LA', 'OLT', 90, 1),('LA', 'OLC', 70, 1),('LA', 'DLT', 90, 1),('LA', 'ILB', 80, 1),('LA', 'S', 80, 1),('LA', 'CB', 70, 1)]

        needs += [('LAR', 'RB', 60, 1),('LAR', 'OLG', 80, 1),('LAR', 'OLC', 70, 1),('LAR', 'DLN', 70, 1),('LAR', 'DLT', 70, 1),('LAR', 'EDGE', 80, 1),('LAR', 'OLB', 80, 1),('LAR', 'ILB', 70, 1),('LAR', 'S', 70, 1),('LAR', 'CB', 50, 1)]

        needs += [('SF', 'RB', 60, 1),('SF', 'WR', 100, 1),('SF', 'OLG', 90, 1),('SF', 'TE', 70, 1),('SF', 'DLT', 80, 1),('SF', 'EDGE', 90, 1),('SF', 'OLB', 70, 1),('SF', 'ILB', 80, 1),('SF', 'CB', 60, 1)]

        needs += [('SEA', 'OLT', 60, 1),('SEA', 'OLG', 80, 1),('SEA', 'TE', 60, 1),('SEA', 'DLE', 80, 1),('SEA', 'EDGE', 60, 1),('SEA', 'OLB', 70, 1),('SEA', 'CB', 90, 1)]

        needs += [('TB', 'DLT', 80, 1),('TB', 'DLE', 70, 1),('TB', 'DLN', 70, 1),('TB', 'EDGE', 80, 1),('TB', 'OLB', 70, 1),('TB', 'ILB', 50, 1),('TB', 'S', 70, 1),('TB', 'CB', 90, 1),('TB', 'RB', 90, 1),('TB', 'WR', 90, 1),('TB', 'OLG', 90, 1)]

        needs += [('TEN', 'RB', 70, 1),('TEN', 'WR', 70, 1),('TEN', 'TE', 70, 1),('TEN', 'EDGE', 80, 1),('TEN', 'ILB', 70, 1),('TEN', 'S', 70, 1),('TEN', 'CB', 50, 1)]

        needs += [('WAS', 'RB', 90, 1),('WAS', 'WR', 100, 1),('WAS', 'OLT', 70, 1),('WAS', 'OLG', 90, 1),('WAS', 'TE', 80, 1),('WAS', 'OLC', 70, 1),('WAS', 'DLN', 90, 1),('WAS', 'DLT', 90, 1),('WAS', 'DLE', 90, 1),('WAS', 'EDGE', 90, 1),('WAS', 'OLB', 90, 1),('WAS', 'ILB', 90, 1),('WAS', 'S', 90, 1),('WAS', 'CB', 90, 1)]



        columns = ('Abbr', 'Need', 'needScore','Count')

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

        allPositions = ["OLG","OLT","OLC","DLN","DLE","DLT", "QB", "WR", "TE", "RB","FB", "EDGE","OLB","ILB","CB", "S","P","K","LS"]


        needs = Team.getNeedsByTeam2(abbr,year)

        for n in needs:
            print("Adding this shit now....",n[1],n[2],n[3])
            Team.AddTeamNeed(abbr,n[1],n[2],n[3])


        #IF NEED NOT LISTED AT ALL, WE MARK IT AS A 30 (Below AVERAGE need)
        for p in allPositions:
            if (p not in needs):
                Team.AddTeamNeed(abbr, p, 30, 1)








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
