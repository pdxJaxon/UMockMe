import sqlite3 as lite2
import psycopg2 as lite
import urllib.parse as urlparse

import os
import sys
from random import *
from datetime import datetime, timedelta
import time
import json




class DB:

    def getConnection():

        conStart = time.time()

        if ("HEROKU_POSTGRESQL_ONYX_URL" in os.environ):
            urlparse.uses_netloc.append("postgres")
            url = urlparse.urlparse(os.environ["HEROKU_POSTGRESQL_ONYX_URL"])

            con = lite.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            con = lite2.connect("UMockMe.db")

        conStop = time.time()

        timeDiff = conStop - conStart

        print("Connect Time:",str(timeDiff))

        return con





    def TearDownDB():

        con = DB.getConnection()


        try:
            with con:
                cur = con.cursor()

                cur.execute("DROP TABLE if exists UMMUser")
                cur.execute("DROP TABLE if exists UserTeamNeed")
                cur.execute("DROP TABLE if exists Prospect")
                cur.execute("DROP TABLE if exists Team")
                cur.execute("DROP TABLE if exists TeamNeed")
                cur.execute("DROP TABLE if exists College")

                cur.execute("DROP TABLE if exists Draft")


                cur.execute("DROP TABLE if exists Meeting")
                cur.execute("DROP TABLE if exists MeetingType")

                cur.execute("DROP TABLE if exists Round")
                cur.execute("DROP TABLE if exists Pick")
                cur.execute("DROP TABLE if exists DeragatoryRemark")
                cur.execute("DROP TABLE if exists ProspectDeragatoryRemark")

                cur.execute("DROP TABLE if exists BigBoard")
                cur.execute("DROP TABLE if exists BigBoardProspect")
                cur.execute("DROP TABLE if exists UserSession")
                cur.execute("DROP TABLE if exists SessionProspect")
                cur.execute("DROP TABLE if exists SessionTeamNeed")

        except:
            print("")




    #Build our database if its not already created
    def createDB():
        con = DB.getConnection()



        try:
            with con:

                cur = con.cursor()

                if ("DATABASE_URL" in os.environ):
                    print("1a1")
                    cur.execute("CREATE TABLE if not exists Prospect(ProspectId integer, lastName varchar(50), firstName varchar(50), pos varchar(50), height varchar(50), weight varchar(50), expertGrade real,DraftProjectedRound integer, DraftProjectedPick integer,uMockMeGrade real,school varchar(50),DraftId integer, CONSTRAINT pkProspectId PRIMARY KEY(ProspectId))")
                    print("1a2")
                    cur.execute("CREATE TABLE if not exists Team(Abbr varchar(50),URL varchar(50),City varchar(50),Nickname varchar(50),Conference varchar(50),Division varchar(50), CONSTRAINT pkAbbr PRIMARY KEY(Abbr))")
                    print("1a3")
                    cur.execute("CREATE TABLE if not exists TeamNeed(Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer, CONSTRAINT pkTeamNeed PRIMARY KEY(Abbr,Need))")
                    print("1a4")
                    cur.execute("CREATE TABLE if not exists UMMUser(email varchar(75), UserName varchar(50), Password varchar(25), FavoriteTeam varchar(50), fName varchar(50), lname varchar(50), CONSTRAINT pkUserEmail PRIMARY KEY(email))")
                    cur.execute("CREATE TABLE if not exists UserTeamNeed(userEmail varchar(75), TeamAbbr varChar(50), pos varchar(50), needScore integer, needCount integer)")
                    cur.execute("CREATE TABLE if not exists College(CollegeId integer, Name varchar(50), Conference varchar(50), CONSTRAINT pkCollegeId PRIMARY KEY(CollegeId))")
                    print("1a5")

                    cur.execute("CREATE TABLE if not exists UserSession(SessionId varchar,UserEmail varchar(75),TheKey varchar(50), TheValue varchar, theDate timestamp, CONSTRAINT pkSessionId PRIMARY KEY(SessionId))")
                    cur.execute("CREATE TABLE if not exists SessionProspect(SessionId varchar,ProspectId integer, CONSTRAINT pkSessionProspect PRIMARY KEY(SessionId,ProspectId))")
                    cur.execute("CREATE TABLE if not exists SessionTeamNeed(SessionId varchar,Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer, CONSTRAINT pkSessionTeamNeed PRIMARY KEY(SessionId,Abbr,Need))")

                    cur.execute("CREATE TABLE if not exists Meeting(MeetingId integer, MeetingName varchar(50), PointValue integer, CONSTRAINT pkMeetingId PRIMARY KEY(MeetingId))")
                    print("1a6")
                    cur.execute("CREATE TABLE if not exists TeamPlayerMeeting(MeetingID integer,TeamId integer,ProspectId integer, CONSTRAINT pkTeamMeetingPlayer PRIMARY KEY(MeetingId,TeamId,ProspectId))")
                    print("1a7")
                    cur.execute("CREATE TABLE if not exists Draft(DraftID integer, Year integer, CONSTRAINT pkDraftId PRIMARY KEY(DraftId))")

                    print("2a")

                    #populate static data for 2017 - we dont import draft info yet as this version is just an MVP
                    cur.execute("INSERT INTO DRAFT VALUES(1,2017)")
                    cur.execute("INSERT INTO DRAFT VALUES(2,2018)")

                    print("3a")

                    cur.execute("CREATE TABLE if not exists Round(DraftID integer,RoundId integer,Round integer, CONSTRAINT pkRound PRIMARY KEY(DraftId,RoundId))")
                    cur.execute("INSERT INTO ROUND VALUES(1,1,1)")
                    cur.execute("INSERT INTO ROUND VALUES(1,2,2)")
                    cur.execute("INSERT INTO ROUND VALUES(1,3,3)")
                    cur.execute("INSERT INTO ROUND VALUES(1,4,4)")
                    cur.execute("INSERT INTO ROUND VALUES(1,5,5)")
                    cur.execute("INSERT INTO ROUND VALUES(1,6,6)")
                    cur.execute("INSERT INTO ROUND VALUES(1,7,7)")

                    cur.execute("INSERT INTO ROUND VALUES(2,8,1)")
                    cur.execute("INSERT INTO ROUND VALUES(2,9,2)")
                    cur.execute("INSERT INTO ROUND VALUES(2,10,3)")
                    cur.execute("INSERT INTO ROUND VALUES(2,11,4)")
                    cur.execute("INSERT INTO ROUND VALUES(2,12,5)")
                    cur.execute("INSERT INTO ROUND VALUES(2,13,6)")
                    cur.execute("INSERT INTO ROUND VALUES(2,14,7)")

                    print("4a")

                    cur.execute("CREATE TABLE if not exists Pick(RoundId integer, RoundPickNum integer, OverallPickNum integer, TeamAbbr varchar(50), ProspectId integer, SessionId varchar(50), CreateDate varchar(50), CONSTRAINT pkPickId PRIMARY KEY(RoundId, RoundPickNum,SessionId))")
                    print("5a")



                    cur.execute("CREATE TABLE if not exists DeragatoryRemark(RemarkId integer, Name varchar(50), PointValue integer)")
                    cur.execute("CREATE TABLE if not exists ProspectDeragatoryRemark(RemarkId integer, ProspectId integer)")
                    print("6a")
                    cur.execute("CREATE TABLE if not exists BigBoard(BigBoardId integer, DraftId integer, TeamId integer, sourceId varchar(50))")
                    cur.execute("CREATE TABLE if not exists BigBoardProspect(BigBoardId integer, ProspectId integer, Rank integer)")
                    print("7a")
                else:
                    print("1a1")
                    cur.execute("CREATE TABLE if not exists Prospect(ProspectId integer, lastName text, firstName text, pos text, height text, weight text, expertGrade real,DraftProjectedRound integer, DraftProjectedPick integer,uMockMeGrade real,school text, PRIMARY KEY(ProspectId))")
                    print("1aq1")
                    cur.execute("CREATE TABLE if not exists Team(Abbr varchar(50),URL varchar(50),City varchar(50),Nickname varchar(50),Conference varchar(50),Division varchar(50), PRIMARY KEY(Abbr))")
                    print("1aq2")
                    cur.execute("CREATE TABLE if not exists TeamNeed(Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer, CONSTRAINT pkTeamNeed PRIMARY KEY(Abbr,Need))")
                    print("1aq3")
                    cur.execute("CREATE TABLE if not exists UMMUser(email varchar(75), UserName varchar(50), Password varchar(25), FavoriteTeam varchar(50), fName varchar(50), lname varchar(50), PRIMARY KEY(email))")
                    cur.execute("CREATE TABLE if not exists UserTeamNeed(userEmail varchar(75), TeamAbbr varChar(50), pos varchar(50), needScore integer, needCount integer)")
                    cur.execute("CREATE TABLE if not exists College(CollegeId integer, Name varchar(50), Conference varchar(50), PRIMARY KEY(CollegeId))")
                    print("1aq4")

                    cur.execute("CREATE TABLE if not exists UserSession(SessionId varchar,UserEmail varchar(75),TheKey varchar(50), TheValue varchar, theDate timestamp, PRIMARY KEY(SessionId))")
                    cur.execute("CREATE TABLE if not exists SessionProspect(SessionId varchar,ProspectId integer,PRIMARY KEY(SessionId,ProspectId))")
                    cur.execute("CREATE TABLE if not exists SessionTeamNeed(SessionId varchar,Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer, PRIMARY KEY(SessionId,Abbr,Need))")

                    cur.execute("CREATE TABLE if not exists Meeting(MeetingId integer, MeetingName varchar(50), PointValue integer,PRIMARY KEY(MeetingId))")
                    print("1aq5")
                    cur.execute("CREATE TABLE if not exists TeamPlayerMeeting(MeetingID integer,TeamId integer,ProspectId integer,PRIMARY KEY(MeetingId,TeamId,ProspectId))")
                    print("1aq6")
                    cur.execute("CREATE TABLE if not exists Draft(DraftID integer, Year integer,PRIMARY KEY(DraftId))")

                    print("2a")

                    # populate static data for 2017 - we dont import draft info yet as this version is just an MVP
                    cur.execute("INSERT INTO DRAFT VALUES(1,2017)")
                    cur.execute("INSERT INTO DRAFT VALUES(2,2018)")

                    print("3a")

                    cur.execute("CREATE TABLE if not exists Round(DraftID integer,RoundId integer,Round integer,PRIMARY KEY(DraftId,RoundId))")
                    cur.execute("INSERT INTO ROUND VALUES(1,1,1)")
                    cur.execute("INSERT INTO ROUND VALUES(1,2,2)")
                    cur.execute("INSERT INTO ROUND VALUES(1,3,3)")
                    cur.execute("INSERT INTO ROUND VALUES(1,4,4)")
                    cur.execute("INSERT INTO ROUND VALUES(1,5,5)")
                    cur.execute("INSERT INTO ROUND VALUES(1,6,6)")
                    cur.execute("INSERT INTO ROUND VALUES(1,7,7)")

                    cur.execute("INSERT INTO ROUND VALUES(2,8,1)")
                    cur.execute("INSERT INTO ROUND VALUES(2,9,2)")
                    cur.execute("INSERT INTO ROUND VALUES(2,10,3)")
                    cur.execute("INSERT INTO ROUND VALUES(2,11,4)")
                    cur.execute("INSERT INTO ROUND VALUES(2,12,5)")
                    cur.execute("INSERT INTO ROUND VALUES(2,13,6)")
                    cur.execute("INSERT INTO ROUND VALUES(2,14,7)")



                    print("4a")

                    cur.execute("CREATE TABLE if not exists Pick(RoundId integer, RoundPickNum integer, OverallPickNum integer, TeamAbbr varchar(50), ProspectId integer, SessionId varchar(50), CreateDate varchar(50), PRIMARY KEY(RoundId, RoundPickNum,SessionId))")
                    print("5a")

                    cur.execute("CREATE TABLE if not exists DeragatoryRemark(RemarkId integer, Name varchar(50), PointValue integer)")
                    cur.execute("CREATE TABLE if not exists ProspectDeragatoryRemark(RemarkId integer, ProspectId integer)")
                    print("6a")
                    cur.execute("CREATE TABLE if not exists BigBoard(BigBoardId integer, DraftId integer, TeamId integer, sourceId varchar(50))")
                    cur.execute("CREATE TABLE if not exists BigBoardProspect(BigBoardId integer, ProspectId integer, Rank integer)")
                    print("7a")

        except:
            print("Error - db already exists")          #This error just means the DB already exists......no biggy
            print("Error: ", sys.exc_info()[0])






    #Whack the DB records to start clean with each test run
    def truncateDB():
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Prospect")
            cur.execute("DELETE FROM Team")
            cur.execute("DELETE FROM TeamNeed")
            cur.execute("DELETE FROM College")
            cur.execute("DELETE FROM Meeting")
            cur.execute("DELETE FROM TeamPlayerMeeting")

            cur.execute("DELETE FROM DeragatoryRemark")
            cur.execute("DELETE FROM ProspectDeragatoryRemark")




    def ExecuteSQL(sql):
        con = DB.getConnection()
        con.set_isolation_level(0)
        with con:
            cur = con.cursor()
            try:
                cur.execute(sql)
            except:
                print("sql error " + sql)





    def xescape(Value):
        return Value.replace("'","''")


    def xunescape(Value):
        return Value.replace("''","'")





    def AddSessionData(sessionId,userEmail,Key,Value):
        theTime = datetime.now()
        Value = json.dumps(Value)
        sql="INSERT INTO UserSession Values('{}' ,'{}' ,'{}' , '{}','{}')".format(sessionId,userEmail,Key,Value,theTime)
        DB.ExecuteSQL(sql)



    def AddCollegeDB(Id,Name,Conference):
        sql = "INSERT INTO College VALUES({},'{}','{}')".format(Id, Name, Conference)
        #print(sql)
        DB.ExecuteSQL(sql)











    def AddTeamDB(abbr,url,city,nickname,conference,division):
        sql = "INSERT INTO Team VALUES('{}','{}','{}','{}','{}','{}')".format(abbr,url,city,nickname,conference,division)
        #print(sql)

        try:
            DB.ExecuteSQL(sql)
        except:
            print("Generic Error with SQL Execute")





    def AddTeamNeedDB(abbr,need,needScore,needCount):

        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT 1 FROM TeamNeed WHERE Abbr='{}' AND need='{}'".format(abbr,need))

            teamNeeds = cur.fetchall()


        if(len(teamNeeds)>0):
            sql="UPDATE TeamNeed SET needScore={}, needCount={} WHERE Abbr='{}' AND Need='{}'".format(needScore,needCount,abbr,need)
        else:
            sql = "INSERT INTO TeamNeed VALUES('{}','{}',{},{})".format(abbr, need, needScore, needCount)

        DB.ExecuteSQL(sql)









    def CacheTeamNeedsForSession(sessionId):
        #SessionTeamNeed(SessionId varchar,Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer

        sql = "DELETE FROM SessionTeamNeed WHERE SessionId='{}'".format(sessionId)
        DB.ExecuteSQL(sql)

        sql = "INSERT INTO SessionTeamNeed(SessionId,Abbr,Need,NeedScore,NeedCount) SELECT DISTINCT '" + str(sessionId) + "',Abbr,Need,NeedScore,NeedCount FROM TeamNeed"
        DB.ExecuteSQL(sql)


    def PopulateSessionProspects(sessionId):
        # SessionTeamNeed(SessionId varchar,Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer

        sql = "DELETE FROM SessionProspect WHERE SessionId='{}'".format(sessionId)
        DB.ExecuteSQL(sql)

        sql = "INSERT INTO SessionProspect(SessionId,ProspectId) SELECT DISTINCT '" + str(
            sessionId) + "',ProspectId FROM Prospect"
        DB.ExecuteSQL(sql)




    def AddProspectDB(id,lname,fname,pos,height,weight,grade,uMockMeGrade,College,DraftId):

        sql = "INSERT INTO Prospect VALUES({},'{}','{}','{}','{}','{}','{}',{},{},{},'{}',{})".format(id, lname, fname, pos, height, weight,grade,0,0,uMockMeGrade,College,DraftId)
        print(sql)

        DB.ExecuteSQL(sql)




    def AddProspectForSessionDB(sessionId,id):
        sql = "INSERT INTO SessionProspect VALUES('{}',{})".format(sessionId,id)
        # print(sql)
        DB.ExecuteSQL(sql)



    def DeleteProspectForSessionDB(sessionId,ProspectId):
        sql = "DELETE FROM SessionProspect WHERE SessionId='{}' AND ProspectId={}".format(sessionId,ProspectId)
        DB.ExecuteSQL(sql)


    def DeleteAllProspectsForSessionDB(sessionId):
        sql = "DELETE FROM SessionProspect WHERE SessionId='{}'".format(sessionId)
        DB.ExecuteSQL(sql)






    def AddTeamNeedForSessionDB(sessionId,team,pos,needScore,needCount):

        #SessionId varchar,Abbr varchar(50), Need varchar(50)


        sql = "DELETE FROM SessionTeamNeed WHERE SessionId='{}' AND Abbr='{}' AND Need='{}'".format(sessionId,team,pos)
        DB.ExecuteSQL(sql)


        sql = "INSERT INTO SessionTeamNeed VALUES('{}','{}','{}',{},{})".format(sessionId, team,pos,needScore,needCount)
        # print(sql)
        DB.ExecuteSQL(sql)






    def UpdateTeamNeedForSessionDB(sessionId,team,pos,needScore,needCount):
        sql = "UPDATE SessionTeamNeed SET needScore={}, needCount={} WHERE sessionId='{}' AND team='{}' AND pos='{}'".format(needScore,needCount,sessionId,team,pos)
        # print(sql)
        DB.ExecuteSQL(sql)





    def DeleteTeamNeedsForSessionDB(sessionId):
        sql = "DELETE FROM SessionTeamNeed WHERE sessionId='{}'".format(sessionId)

        # print(sql)
        DB.ExecuteSQL(sql)







    def getNeedsForAllTeams(sessionId):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM SessionTeamNeed WHERE sessionId='{}'".format(sessionId))

            teamNeeds = cur.fetchall()

            return teamNeeds




    def getProspectById(PlayerId):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Prospect Where ProspectId='{}'".format(PlayerId))

            p = cur.fetchall()

            return p







    def getAllNeedsForSessionTeam(sessionId,abbr):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM SessionTeamNeed WHERE team='{}' AND sessionId='{}'".format(abbr,sessionId))

            teamNeeds = cur.fetchall()

            return teamNeeds






    def getAllTeams():
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Team Order By conference,division")

            teams = cur.fetchall()

            return teams







    def getAllNeedsForTeam(abbr):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM TeamNeed WHERE Abbr='{}'".format(abbr))

            teamNeeds = cur.fetchall()

            return teamNeeds





    def getSessionValue(sessionId,Key):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT TheValue FROM UserSession WHERE SessionId='{}' AND TheKey='{}'".format(sessionId,Key))

            value = cur.fetchall()

            return value



    def getAllColleges():
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM College Order By conference")

            colleges = cur.fetchall()

            return colleges




    #Will return all prospects from DB sorted by Expert Grade in DESC Order (Best player at top)
    def getAllProspects():
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Prospect Order By Expertgrade desc")

            prospects = cur.fetchall()

            return prospects





    def getAllProspectsForSession(sessionId):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT p.* FROM SessionProspect as s INNER JOIN Prospect as p on p.ProspectId = s.ProspectId WHERE s.SessionId='{}' Order By Expertgrade desc".format(sessionId))

            prospects = cur.fetchall()

            return prospects









    def getAllRemarksForProspect(ProspectId):
        return True




    def AddRemarkDB(id, name, pointValue):
        return True







    def AddDraftDB(id, Year):

        sql = "INSERT INTO Draft VALUES({},'{}')".format(id, Year)
        DB.ExecuteSQL(sql)
        return True











    def getDraftByYear(Year):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Draft WHERE Year={}".format(Year))

            TheDraft = cur.fetchall()

            return TheDraft






    def getAllRoundsByDraft(Year):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            'lookup draft id by year'


            cur.execute("SELECT r.* FROM Round as r inner join Draft as d on d.draftid = r.draftid WHERE d.year={}".format(Year))

            TheDraft = cur.fetchall()

            return TheDraft




    def GetAllPicksForRoundDB(year,round,sessionid):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT p.* From Pick as p where roundId={} and SessionId='{}' ".format(round,sessionid))

            Picks = cur.fetchall()

            return Picks



    def GetAllPickDetailsForYearDB(year, sessionid):


        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute(
                "SELECT p.RoundId,p.RoundPickNum,p.OverallPickNum,p.TeamAbbr,p.ProspectId, x.firstName,x.LastName,x.pos,x.expertGrade, x.school From Draft as d INNER JOIN  Pick as p on p.DraftID = d.DraftID inner join Prospect x on x.Id = p.ProspectId where d.Year={} and p.SessionId='{}' ORDER BY p.OverallPickNum ".format(
                    year, sessionid))

            PickDetails = cur.fetchall()

        return PickDetails





    def GetAllPickDetailsForRoundDB(year, round,sessionid):

        #Prospect(Id Int, lastName Text, firstName Text, pos Text, height Text, weight Text, expertGrade float,DraftProjectedRound int, DraftProjectedPick int)")
        #Pick(RoundId int, RoundPickNum int, OverallPickNum int, TeamAbbr Text, ProspectId int)")


        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT p.RoundId,p.RoundPickNum,p.OverallPickNum,p.TeamAbbr,p.ProspectId, x.firstName,x.LastName,x.pos,x.expertGrade, x.school From Pick as p inner join Prospect x on x.ProspectId = p.ProspectId where p.roundId={} and p.SessionId='{}' ORDER BY p.OverallPickNum ".format(round,sessionid))

            PickDetails = cur.fetchall()

        return PickDetails




    def GetCollegeById(id=-1):
        con = DB.getConnection()
        sql = "SELECT * FROM College WHERE Collegeid={}".format(id)

        with con:
            cur = con.cursor()
            cur.execute(sql)

            data = cur.fetchall()

        return data









    def GetProspectId(Name, POS, School,pickNum):
        con = DB.getConnection()

        vals = str.split(Name," ")
        fname = str(vals[0].replace("'","''"))
        lname = str(vals[1].replace("'","''"))

        sql = "SELECT ID FROM PROSPECT WHERE LastName='{}' AND FirstName='{}'".format(lname,fname)
        #print(sql)

        with con:
            cur = con.cursor()

            cur.execute(sql)

            data = cur.fetchall()



            if(len(data)>0):
                retVal=data[0]
            else:
                x=randint(-99999999,99999999)


                expertGrade=0
                print(School)
                DB.AddProspectDB(x,lname,fname,POS,0,0,expertGrade,0,School.replace("'","''"))
                retVal=x



        return retVal









    def AddBoardProspect(BigBoardId,ProspectId,Rank):
        sql = "INSERT INTO BigBoardProspect VALUES({},'{}',{})".format(BigBoardId, ProspectId,Rank)
        #print(sql)
        DB.ExecuteSQL(sql)




    def AddBigBoard(BoardId,DraftId,TeamId,SourceId):
        sql = "INSERT INTO BigBoard VALUES({},{},'{}','{}')".format(BoardId,DraftId,TeamId,SourceId)

        DB.ExecuteSQL(sql)






    def getBigBoard(boardId=1):

        #cur.execute("CREATE TABLE if not exists BigBoard(BigBoardId int, DraftId int, TeamId Int, sourceId text)")
        #cur.execute("CREATE TABLE if not exists BigBoardProspect(BigBoardId int, ProspectId int, Rank int)")

        con = DB.getConnection()

        with con:
            cur = con.cursor()

            sql = "SELECT * FROM BigBoardProspect ORDER BY Rank ASC"
            #print(sql)
            cur.execute(sql)

            t = cur.fetchall()

        return t






    def getBigBoardForTeam(teamId):

        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM BigBoard WHERE TeamId='{}'".format(teamId))

            t = cur.fetchall()

        return t






    def getBigBoardForSource(Source=1):

        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM BigBoard WHERE SourceId={}".format(Source))

            t = cur.fetchall()

        return t





    def getUser(email):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM UMMUser WHERE email='{}'".format(email))

            u=cur.fetchall()

            return u





    def getFavoriteTeamNeedsByUser(email,abbr):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM UserTeamNeeds WHERE userEmail='{}' and TeamAbbr='{}'".format(email,abbr))

            n=cur.fetchall()

            return n





    def getTeamByAbr(abr):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM Team WHERE Abbr='{}'".format(abr))

            t=cur.fetchall()

            return t







    def UpdatePick(rnd,PickNum,OverallPickNum,Team,Player,sessionid):

        #Pick(RoundId int, RoundPickNum int, OverallPickNum int, TeamAbbr Text, ProspectId int)

        sql = "Update Pick SET TeamAbbr = '{}', ProspectId={} WHERE RoundId={} AND RoundPickNum={} AND OverallPickNum={} and SessionId='{}'".format(Team,Player,rnd,PickNum,OverallPickNum,sessionid)
        print(sql)
        DB.ExecuteSQL(sql)








    def DeletePicksForSession(sessionid):
        sql="DELETE FROM PICK WHERE SessionId='{}'".format(sessionid)

        DB.ExecuteSQL(sql)






    def DeleteStalePicks():
        StaleDate = str(datetime.now() - datetime.timedelta(days=1))
        sql="DELETE FROM PICK WHERE CreateData <'{}'".format(StaleDate)

        DB.ExecuteSQL(sql)





    def DeleteStaleSessionData():
        StaleDate = str(datetime.now() - timedelta(days=1))


        sql="DELETE FROM SessionProspect WHERE SessionID in (SELECT SessionId FROM UserSession WHERE theDate <='" + StaleDate + "')"

        DB.ExecuteSQL(sql)

        sql = "DELETE FROM SessionTeamNeed WHERE SessionID in (SELECT SessionId FROM UserSession WHERE theDate <='" + StaleDate + "')"

        DB.ExecuteSQL(sql)

        sql = "DELETE FROM UserSession WHERE theDate <='" + StaleDate + "'"

        DB.ExecuteSQL(sql)







    def getAllPicksForUser(sessionId):
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT p.RoundId, p.RoundPickNum, p.OverallPickNum, p.TeamAbbr,t.ProspectId, t.firstName,t.lastName,t.pos, t.school FROM PICK AS p LEFT OUTER JOIN Prospect AS t on t.ProspectId = p.ProspectId WHERE p.SessionId='{}' ORDER BY p.OverallPickNum ASC".format(sessionId))

            p = cur.fetchall()

            return p








    def getNextPickForUser(sessionId):
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM PICK WHERE ProspectId is null AND SessionId='{}' ORDER BY OverallPickNum ASC LIMIT 1".format(sessionId))

            p = cur.fetchall()

            return p






    def getLastPlayerPicked(sessionId):
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM PICK WHERE ProspectId is not null AND SessionId='{}' ORDER BY OverallPickNum DESC LIMIT 1".format(
                    sessionId))

            p = cur.fetchall()
            print("Picky:",p)

            return p






    def getPicksForUser(sessionId):
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM PICK WHERE SessionId='{}'".format(sessionId))

            p = cur.fetchall()

            return p






    def PopulatePicks(sessionid):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("DELETE FROM PICK WHERE SessionId='{}'".format(sessionid))

            theTime = time.time()

            # 1 - 32 picks
            cur.execute("INSERT INTO PICK VALUES(1,1,1,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,2,2,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,3,3,'CHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,4,4,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,5,5,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,6,6,'NYJ',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,7,7,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,8,8,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,9,9,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,10,10,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,11,11,'NO',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,12,12,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,13,13,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,14,14,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,15,15,'IND',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,16,16,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,17,17,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,18,18,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,19,19,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,20,20,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,21,21,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,22,22,'MIA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,23,23,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,24,24,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,25,25,'HOU',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,26,26,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,27,27,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,28,28,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,29,29,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,30,30,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,31,31,'ATL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(1,32,32,'NO',null,'{}','{}')".format(sessionid,theTime))










            # 2 - 32 picks
            cur.execute("INSERT INTO PICK VALUES(2,1,33,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,2,34,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,3,35,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,4,36,'CHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,5,37,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,6,38,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,7,39,'NYJ',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,8,40,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,9,41,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,10,42,'NO',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,11,43,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,12,44,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,13,45,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,14,46,'IND',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,15,47,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,16,48,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,17,49,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,18,50,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,19,51,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,20,52,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,21,53,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,22,54,'MIA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,23,55,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,24,56,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,25,57,'HOU',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,26,58,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,27,59,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,28,60,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,29,61,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,30,62,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,31,63,'ATL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(2,32,64,'CAR',null,'{}','{}')".format(sessionid,theTime))







            # 3
            # 43  'Compensatory Picks
            cur.execute("INSERT INTO PICK VALUES(3,1,65,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,2,66,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,3,67,'CHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,4,68,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,5,69,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,6,70,'NYJ',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,7,71,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,8,72,'NE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,9,73,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,10,74,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,11,75,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,12,76,'NO',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,13,77,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,14,78,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,15,79,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,16,80,'IND',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,17,81,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,18,82,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,19,83,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,20,84,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,21,85,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,22,86,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,23,87,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,24,88,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,25,89,'HOU',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,26,90,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,27,91,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,28,92,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,29,93,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,30,94,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,31,95,'ATL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,32,96,'NE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,33,97,'MIA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,34,98,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,35,99,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,36,100,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,37,101,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,38,102,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,39,103,'NO',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,40,104,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,41,105,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,42,106,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(3,43,107,'NYJ',null,'{}','{}')".format(sessionid,theTime))




            # 4
            # 38
            cur.execute("INSERT INTO PICK VALUES(4,1,108,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,2,109,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,3,110,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,4,111,'CHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,5,112,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,6,113,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,7,114,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,8,115,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,9,116,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,10,117,'CHI',null,'{}','{}')".format(sessionid,theTime))
            #cur.execute("INSERT INTO PICK VALUES(4,11,75,'NE',null,'{}','{}')".format(sessionid,theTime)) - NE LOST PICK
            cur.execute("INSERT INTO PICK VALUES(4,12,118,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,13,119,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,14,120,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,15,121,'IND',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,16,122,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,17,123,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,18,124,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,19,125,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,20,126,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,21,127,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,22,128,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,23,129,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,24,130,'HOU',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,25,131,'NE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,26,132,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,27,133,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,28,134,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,29,135,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,30,136,'ATL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,31,137,'IND',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,32,138,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,33,139,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,34,140,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,35,141,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,36,142,'HOU',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,37,143,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(4,38,144,'IND',null,'{}','{}')".format(sessionid,theTime))




            # 5
            # 41
            cur.execute("INSERT INTO PICK VALUES(5,1,145,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,2,146,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,3,147,'CHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,4,148,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,5,149,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,6,150,'NYJ',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,7,151,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,8,152,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,9,153,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,10,154,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,11,155,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,12,156,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,13,157,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,14,158,'IND',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,15,159,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,16,160,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,17,161,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,18,162,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,19,163,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,20,164,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,21,165,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,22,166,'MIA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,23,167,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,24,168,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,25,169,'HOU',null,'{}','{}')".format(sessionid,theTime))
            #cur.execute("INSERT INTO PICK VALUES(5,26,90,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,27,170,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,28,171,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,29,172,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,30,173,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,31,174,'ATL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,32,175,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,33,176,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,34,177,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,35,178,'MIA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,36,179,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,37,180,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,38,181,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,39,182,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,40,183,'NE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(5,41,184,'MIA',null,'{}','{}')".format(sessionid,theTime))


            # 6
            # 35
            cur.execute("INSERT INTO PICK VALUES(6,1,185,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,2,186,'BAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,3,187,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,4,188,'CLE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,5,189,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,6,190,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,7,191,'NYJ',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,8,192,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,9,193,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,10,194,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,11,195,'BUF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,12,196,'NO',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,13,197,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,14,198,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,15,199,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,16,200,'NE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,17,201,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,18,202,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,19,203,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,20,204,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,21,205,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,22,206,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,23,207,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,24,208,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,25,209,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,26,210,'SEA',null,'{}','{}')".format(sessionid,theTime))
            #cur.execute("INSERT INTO PICK VALUES(6,27,91,'KC',null,'{}','{}')".format(sessionid,theTime)) PICK YANKED
            cur.execute("INSERT INTO PICK VALUES(6,28,211,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,29,212,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,30,213,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,31,214,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,32,215,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,33,216,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,34,217,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(6,35,218,'KC',null,'{}','{}')".format(sessionid,theTime))




            # 7
            # 35
            cur.execute("INSERT INTO PICK VALUES(7,1,219,'SF',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,2,220,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,3,221,'CHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,4,222,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,5,223,'MIA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,6,224,'NYJ',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,7,225,'LAC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,8,226,'SEA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,9,227,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,10,228,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,11,229,'NO',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,12,230,'PHI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,13,231,'ARI',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,14,232,'MIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,15,233,'CAR',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,16,234,'LA',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,17,235,'WAS',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,18,236,'TEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,19,237,'TB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,20,238,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,21,239,'NE',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,22,240,'JAX',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,23,241,'NYG',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,24,242,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,25,243,'HOU',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,26,244,'OAK',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,27,245,'KC',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,28,246,'DAL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,29,247,'GB',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,30,248,'PIT',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,31,249,'ATL',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,32,250,'DET',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,33,251,'CIN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,34,252,'DEN',null,'{}','{}')".format(sessionid,theTime))
            cur.execute("INSERT INTO PICK VALUES(7,35,253,'DEN',null,'{}','{}')".format(sessionid,theTime))

            theTimeEnd = time.time()

            diffy = theTimeEnd - theTime

            print("Pop Picks Time:",str(diffy))



    def getUserByEmail(email):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM UMMUser WHERE Email='{}'".format(email))

            u = cur.fetchall()

            print(u[0])

            return u





    def getUserByEmailAndPassword(email,pwd):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM UMMUser WHERE Email='{}' AND Password='{}'".format(email,pwd))

            u = cur.fetchall()

            if(u):
                print(u[0])

            return u








    def AddUser(email,userName,Password,FavoriteTeam,Fname,Lname):
        sql = "INSERT INTO UMMUser VALUES('{}','{}','{}','{}','{}','{}')".format(email,userName,Password,FavoriteTeam,Fname,Lname)
        # print(sql)

        #Todo: Will need to check for EMAIL Uniqueness
        DB.ExecuteSQL(sql)





    def UpdateUser(email,userName,Password,FavoriteTeam,Fname,Lname):
        sql = "UPDATE UMMUser SET(userName='{}',Password='{}',FavoriteTeam='{}',Fname='{}',LName='{}' WHERE Email='{}')".format(userName,Password,FavoriteTeam,Fname,Lname,email)
        # print(sql)

        #Todo: Will need to check for EMAIL Uniqueness
        DB.ExecuteSQL(sql)





    def WireTeamPlayerMeeting():


        sql="INSERT INTO Meeting Values(1,'Combine Meeting',3)"
        DB.ExecuteSQL(sql)

        sql = "INSERT INTO Meeting Values(2,'Player Team Facility Visit',4)"
        DB.ExecuteSQL(sql)

        sql = "INSERT INTO Meeting Values(3,'Pro Day Visit',3)"
        DB.ExecuteSQL(sql)

        sql = "INSERT INTO Meeting Values(4,'Private Meeting - Dinner',5)"
        DB.ExecuteSQL(sql)


        sql = "DROP TABLE TeamPlayerMeeting"
        DB.ExecuteSQL(sql)

        #this relationship says.....As Per This UMockMe User, This Team, Had THIS meeting, With THIS Player. This data is stored at the UMockMeUser Level.
        sql = "CREATE TABLE if not exists TeamPlayerMeeting(MeetingID integer, TeamId integer, ProspectId integer, userEmail varchar(75), PRIMARY KEY(MeetingId, TeamId, ProspectId, userEmail))"
        DB.ExecuteSQL(sql)














