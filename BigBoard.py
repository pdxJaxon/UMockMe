import sqlite3 as lite
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib
import Prospects




class Board:





    # Will return all prospects from DB sorted by Expert Grade in DESC Order (Best player at top)
    def getBigBoard(boardId=1):

        board = DBLib.DB.getBigBoard(boardId)

        return board


    def getBigBoardForTeam(teamId):

        board = DBLib.DB.getBigBoardForTeam(teamId)
        return board



    def getBigBoardForSource(Source=1):

        board = DBLib.DB.getBigBoardForSource(Source)
        return board





    def stringToJson(rawString):

        iFoundStart = rawString.find("\"prospects\"")
        iFoundEnd = rawString.find("\"draft\"")

        jsonString = rawString[iFoundStart + 12:iFoundEnd - 1]

        # print("data:\n" + jsonString)



        # print(jsonString)
        obj = json.loads(jsonString)

        return obj











    def getRawBigBoardDataForSource(Source=0):

        lsBoard = []

        pick = 0
        name=""
        pos=""
        school=""

        if(Source==0):

            url = "https://www.profootballfocus.com/nfl-draft/"

            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            print(soup)

            Board = soup.find("table", {"id": "tablepress-1220"})
            body = Board.find('tbody')

            rows = body.find_all('tr')


            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                lsBoard.append([ele for ele in cols if ele])
        elif(Source==1):
            url = "http://walterfootball.com/nfldraftbigboard"

            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            # print(soup)

            iCount=1

            rows = soup.find_all('div',{"class":"divPlayerRanking"})

            for row in rows:

                divs = row.find_all('div', {"class": "cellDiv", "style": "width:93%;border-bottom:solid thin silver; padding-bottom:3px;"})

                for d in divs:
                    # print(d)
                    p = d.find('b')

                    elms = p.text.strip()

                    lsElms=elms.split(",")

                    PickNum=iCount
                    Name=lsElms[0]
                    l = len(lsElms[1])
                    startPos = lsElms[1].rfind(" ", 0, l) +1

                    POS = lsElms[1][startPos:l]

                    l=len(lsElms[2])-1
                    School=lsElms[2].strip()
                    School = lsElms[2][1:l]

                    lsBoard.append([PickNum,Name, POS,0,School])
                    iCount+=1

            for row in rows:

                divs = row.find_all('div',{"class":"cellDiv","style":"width:93%; border-bottom:solid thin silver;"})

                for d in divs:
                    #print(d)
                    p = d.find('b')

                    elms = p.text.strip()

                    lsElms = elms.split(",")

                    PickNum=iCount
                    Name = lsElms[0]
                    l=len(lsElms[1])
                    startPos = lsElms[1].rfind(" ",0,l)+1

                    POS = lsElms[1][startPos:l]

                    l = len(lsElms[2]) - 1
                    School = lsElms[2].strip()
                    School = lsElms[2][1:l]

                    lsBoard.append([PickNum,Name,POS,0,School])

            #print(lsBoard)


        return lsBoard







    # pass in our JSON Data and pump em into the DB
    def AddBatch(BigBoardId,jsonData):

        # attributes:
        '''
        cur.execute("CREATE TABLE if not exists BigBoard(BigBoardId int, DraftId int, TeamId Int, sourceId text")
        cur.execute("CREATE TABLE if not exists BigBoardProspect(BigBoardId int, ProspectId int, Rank int")
        '''



        #Sample: ['1', 'Myles Garrett', 'Edge', '1', 'Texas A&M']
        for dude in jsonData:
            pickNum=dude[0]
            Name=dude[1]
            pos = dude[2]
            School = dude[4]
            ProspectId = Prospects.Prospect.GetProspectId(Name,pos,School,pickNum)

            #print("Pick:{} id:{} Name:{} position:{} School:{}".format(pickNum,ProspectId,Name,pos,School))



            Board.AddBoardProspect(BigBoardId,ProspectId,pickNum)




    def AddBoardProspect(BigBoardId,ProspectId,Rank):
        DBLib.DB.AddBoardProspect(BigBoardId,ProspectId,Rank)


    def AddBoard(id,DraftId,TeamId,SourceId):
        DBLib.DB.AddBigBoard(id,DraftId,TeamId,SourceId)