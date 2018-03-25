import sqlite3 as lite2
import psycopg2 as lite
import urllib.parse as urlparse
import Teams
import os
import sys
from random import *
from datetime import datetime, timedelta
import time
import json




class DB:

    def getConnection():



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



        return con





    def TearDownDB():

        con = DB.getConnection()


        try:
            with con:
                cur = con.cursor()

                cur.execute("DROP TABLE if exists UMMUser")
                cur.execute("DROP TABLE if exists UserProspect")
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
                    cur.execute("CREATE TABLE if not exists Prospect(ProspectId integer, lastName varchar(50), firstName varchar(50), pos varchar(50), height varchar(50), weight varchar(50), expertGrade real,DraftProjectedRound integer, DraftProjectedPick integer,uMockMeGrade real,sparqScore real,school varchar(50),DraftId integer, CONSTRAINT pkProspectId PRIMARY KEY(ProspectId))")
                    print("1a2")
                    cur.execute("CREATE TABLE if not exists Team(Abbr varchar(50),URL varchar(50),City varchar(50),Nickname varchar(50),Conference varchar(50),Division varchar(50), CONSTRAINT pkAbbr PRIMARY KEY(Abbr))")
                    print("1a3")
                    cur.execute("CREATE TABLE if not exists TeamNeed(Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer, DraftId int, CONSTRAINT pkTeamNeed PRIMARY KEY(Abbr,Need))")
                    print("1a4")
                    cur.execute("CREATE TABLE if not exists UMMUser(email varchar(75), UserName varchar(50), Password varchar(25), FavoriteTeam varchar(50), fName varchar(50), lname varchar(50), CONSTRAINT pkUserEmail PRIMARY KEY(email))")
                    cur.execute("CREATE TABLE if not exists UserProspect(email varchar(75),draftId integer, ProspectId integer, expertGrade real, sparqScore real, CONSTRAINT pkUserProspect PRIMARY KEY(email,ProspectId))")
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




                    cur.execute("INSERT INTO Meeting Values(1,'Pre Draft Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(2,'Combine Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(3,'Private Combine Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(4,'Sr Bowl Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(5,'Private Sr Bowl Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(6,'Pro Day Visit Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(7,'Pro Day Private Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(8,'Other Group Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(9,'Other Private Meeting',2)")



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
                    cur.execute("CREATE TABLE if not exists Prospect(ProspectId integer, lastName text, firstName text, pos text, height text, weight text, expertGrade real,DraftProjectedRound integer, DraftProjectedPick integer,uMockMeGrade real, sparqScore real,school text, draftId int, PRIMARY KEY(ProspectId))")
                    print("1aq1")
                    cur.execute("CREATE TABLE if not exists Team(Abbr varchar(50),URL varchar(50),City varchar(50),Nickname varchar(50),Conference varchar(50),Division varchar(50), PRIMARY KEY(Abbr))")
                    print("1aq2")
                    cur.execute("CREATE TABLE if not exists TeamNeed(Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer, DraftId int, CONSTRAINT pkTeamNeed PRIMARY KEY(Abbr,Need))")
                    print("1aq3")
                    cur.execute("CREATE TABLE if not exists UMMUser(email varchar(75), UserName varchar(50), Password varchar(25), FavoriteTeam varchar(50), fName varchar(50), lname varchar(50), PRIMARY KEY(email))")
                    cur.execute("CREATE TABLE if not exists UserProspect(email varchar(75), ProspectId integer, expertGrade real, sparqScore real, CONSTRAINT pkUserProspect PRIMARY KEY(email,ProspectId))")
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

                    cur.execute("INSERT INTO Meeting Values(1,'Pre Draft Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(2,'Combine Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(3,'Private Combine Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(4,'Sr Bowl Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(5,'Private Sr Bowl Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(6,'Pro Day Visit Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(7,'Pro Day Private Meeting',2)")
                    cur.execute("INSERT INTO Meeting Values(8,'Other Group Meeting',1)")
                    cur.execute("INSERT INTO Meeting Values(9,'Other Private Meeting',2)")



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

        try:
            con.set_isolation_level(0)
        except:
            print("this is fine - local db doesnt support isolation level setting")

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





    def AddTeamNeedDB(abbr,need,needScore,needCount,draftId=2):

        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT 1 FROM TeamNeed WHERE Abbr='{}' AND need='{}' AND draftId={}".format(abbr,need,draftId))

            teamNeeds = cur.fetchall()


        if(len(teamNeeds)>0):
            sql="UPDATE TeamNeed SET needScore={}, needCount={} WHERE Abbr='{}' AND Need='{}' AND draftId={}".format(needScore,needCount,abbr,need,draftId)
        else:
            sql = "INSERT INTO TeamNeed VALUES('{}','{}',{},{},{})".format(abbr, need, needScore, needCount,draftId)

        DB.ExecuteSQL(sql)









    def CacheTeamNeedsForSession(sessionId,draftId):
        #SessionTeamNeed(SessionId varchar,Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer

        needs=Teams.Team.getNeedsForAllTeams2()

        for n in needs:
            DB.AddTeamNeedForSessionDB(sessionId,n['Abbr'],n['Need'],n['needScore'],1)








    def PopulateSessionProspects(sessionId,draftId=2):
        # SessionTeamNeed(SessionId varchar,Abbr varchar(50), Need varchar(50), NeedScore integer, NeedCount integer

        DB.DeleteAllProspectsForSessionDB(sessionId)

        sql = "INSERT INTO SessionProspect(SessionId,ProspectId) SELECT DISTINCT '{}',ProspectId FROM Prospect WHERE DraftId={}".format(sessionId,draftId)
        DB.ExecuteSQL(sql)




    def AddProspectDB(id,lname,fname,pos,height,weight,grade,rnd,pck,uMockMeGrade,sparqScore,College,DraftId):

        sql = "INSERT INTO Prospect(ProspectId,lastName,firstName,pos,height,weight,expertGrade,DraftProjectedRound,DraftProjectedPick,uMockMeGrade,sparqScore,school,draftId) VALUES({},'{}','{}','{}','{}','{}','{}',{},{},{},{},'{}',{})".format(id,lname,fname,pos,height,weight,grade,rnd,pck,uMockMeGrade,sparqScore,College,DraftId)
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
        sql = "UPDATE SessionTeamNeed SET needScore={}, needCount={} WHERE sessionId='{}' AND Abbr='{}' AND Need='{}'".format(needScore,needCount,sessionId,team,pos)
        # print(sql)
        DB.ExecuteSQL(sql)





    def DeleteTeamNeedsForSessionDB(sessionId):
        sql = "DELETE FROM SessionTeamNeed WHERE sessionId='{}'".format(sessionId)

        # print(sql)
        DB.ExecuteSQL(sql)







    def getNeedsForAllTeams(sessionId):
        con = DB.getConnection()

        cols = ["sessionId", "Abbr", "Need", "needScore", "needCount"]

        results = []

        with con:
            cur = con.cursor()
            cur.execute("SELECT sessionId,Abbr,Need,needScore,needCount FROM SessionTeamNeed WHERE sessionId='{}'".format(sessionId))


            cur.execute



            for m in cur.fetchall():
                results.append(dict(zip(cols, m)))


        if(len(results)==0):
            DB.CacheTeamNeedsForSession(sessionId,2)
            results = DB.getNeedsForAllTeams(sessionId)


        return results




    def getProspectById(PlayerId):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Prospect Where ProspectId='{}'".format(PlayerId))

            p = cur.fetchall()

            return p



    def getUserProspectById(UserId,PlayerId):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT up.prospectId,p.firstname,p.lastname,p.pos,p.height,p.weight,p.school,up.expertgrade,up.sparqscore FROM UserProspect up INNER JOIN Prospect p ON p.ProspectId=up.ProspectId Where up.ProspectId='{}' AND up.email='{}'".format(PlayerId,UserId))

            p = cur.fetchall()


            return p




    def PopulateUserProspects(UserId):

        sql = "INSERT INTO UserProspect(email,ProspectId,ExpertGrade,sparqScore,draftId) SELECT '{}',ProspectId,ExpertGrade,coalesce(sparqScore,50),2 FROM Prospect WHERE ProspectId Not In(SELECT ProspectId From UserProspect WHERE email='{}')".format(UserId,UserId)

        DB.ExecuteSQL(sql)



    def UpdateUserProspect(prospect,UserId):



        sql = "UPDATE UserProspect SET expertgrade={},sparqScore={} WHERE ProspectId='{}' AND email='{}'".format(prospect[7],prospect[8],prospect[0],UserId)



        DB.ExecuteSQL(sql)




    def getAllNeedsForSessionTeam(sessionId,abbr):
        con = DB.getConnection()

        cols = ["sessionId", "Abbr", "Need", "needScore", "needCount"]

        with con:
            cur = con.cursor()
            cur.execute("SELECT sessionId,Abbr,Need,needScore,needCount FROM SessionTeamNeed WHERE Abbr='{}' AND sessionId='{}'".format(abbr,sessionId))

            results = []

            for m in cur.fetchall():
                results.append(dict(zip(cols, m)))



        return results






    def getAllTeams():
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Team Order By conference,division")

            teams = cur.fetchall()

            return teams



    def getAllTeamsAsJSON():
        con = DB.getConnection()

        with con:
            cur = con.cursor()


            cur.execute("SELECT Abbr,City,Nickname FROM Team Order By City")

            columns = ('Abbr', 'City', 'Nickname')

            results = []

            for m in cur.fetchall():
                results.append(dict(zip(columns, m)))


        return results








    def getAllNeedsForTeam(abbr,draftId=2):
        con = DB.getConnection()

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM TeamNeed WHERE Abbr='{}' and draftId={} ORDER BY NeedScore DESC".format(abbr,draftId))

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
    def getAllProspects(year):
        con = DB.getConnection()

        if(year=="2017"):
            DraftId=1
        else:
            DraftId=2

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Prospect WHERE DraftId={} Order By Expertgrade desc".format(DraftId))

            prospects = cur.fetchall()

            return prospects





    def getAllProspectsForSession(sessionId):
        con = DB.getConnection()

        with con:
            cur = con.cursor()



            cur.execute("SELECT p.ProspectId,p.lastName,p.firstName,p.pos,p.height,p.weight,p.expertGrade,p.DraftProjectedRound,p.DraftProjectedPick,p.uMockMeGrade,p.sparqScore,p.school,p.draftId FROM SessionProspect as s INNER JOIN Prospect as p on p.ProspectId = s.ProspectId WHERE s.SessionId='{}' Order By expertGrade desc".format(sessionId))

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




    def getAllMeetings():
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT cast(meetingid as text),meetingname,cast(pointvalue as text) FROM Meeting")

            columns=('MeetingId','MeetingName','PointValue')

            results = []

            for m in  cur.fetchall():
                results.append(dict(zip(columns,m)))


            return results






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
        print(sql)
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






    def getAllSelectedPicksForUser(sessionId):
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT p.RoundId, p.RoundPickNum, p.OverallPickNum, p.TeamAbbr,t.ProspectId, t.firstName,t.lastName,t.pos, t.school FROM PICK AS p LEFT OUTER JOIN Prospect AS t on t.ProspectId = p.ProspectId WHERE p.SessionId='{}' and p.ProspectId is  not null ORDER BY p.OverallPickNum ASC".format(sessionId))

            p = cur.fetchall()

            return p


    def getAllPicksForUser(sessionId):
        con = DB.getConnection()
        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT p.RoundId, p.RoundPickNum, p.OverallPickNum, p.TeamAbbr,t.ProspectId, t.firstName,t.lastName,t.pos, t.school FROM PICK AS p LEFT OUTER JOIN Prospect AS t on t.ProspectId = p.ProspectId WHERE p.SessionId='{}' ORDER BY p.OverallPickNum ASC".format(sessionId))

            p = cur.fetchall()

            return p






    def UpdateSparqScores():

        #SOURCE: https://3sigmaathlete.com

        #Off LOS Linebackers

        sql="UPDATE Prospect SET sparqScore=96, UMockMeGrade=expertGrade+.46 Where LOWER(Lastname) = 'vander esch' AND LOWER(School) like 'boise%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=95.4, UMockMeGrade=expertGrade+.454 Where LOWER(Lastname) = 'Thomas' AND LOWER(School) like 'florida state%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=94.7, UMockMeGrade=expertGrade+.447 Where LOWER(Lastname) = 'burks' AND LOWER(School) like 'vanderbilt%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=86.8, UMockMeGrade=expertGrade+.368 Where LOWER(Lastname) = 'avery' AND LOWER(School) like 'memphis%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=75, UMockMeGrade=expertGrade+.25 Where LOWER(Lastname) = 'warner' AND LOWER(School) like 'byu%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=68, UMockMeGrade=expertGrade+.18 Where LOWER(Lastname) = 'kiser' AND LOWER(School) like 'virginia%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=38.6, UMockMeGrade=expertGrade-.114 Where LOWER(Lastname) = 'young' AND LOWER(School) like 'ucla%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=32, UMockMeGrade=expertGrade-.18 Where LOWER(Lastname) = 'sam' AND LOWER(School) like 'arizona state%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=30.3, UMockMeGrade=expertGrade-.197 Where LOWER(Lastname) = 'mccray' AND LOWER(School) like 'michigan%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=26.9, UMockMeGrade=expertGrade-.231 Where LOWER(Lastname) = 'jewell' AND LOWER(School) like 'iowa%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=17.9, UMockMeGrade=expertGrade-.321 Where LOWER(Lastname) = 'victor' AND LOWER(School) like 'washington%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=9.9, UMockMeGrade=expertGrade-.41 Where LOWER(Lastname) = 'bierria' AND LOWER(School) like 'washington%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=8.7, UMockMeGrade=expertGrade-.413 Where LOWER(Lastname) = 'deluca' AND LOWER(School) like 'north dakota state%' AND LOWER(POS) IN('ilb','olb','lb','edge') AND DraftId=2"
        DB.ExecuteSQL(sql)



        #SAFETY

        sql = "UPDATE Prospect SET sparqScore=99.4, UMockMeGrade=expertGrade+.496 Where LOWER(Lastname) = 'apke' AND LOWER(School) like 'penn state%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=96.2, UMockMeGrade=expertGrade+.462 Where LOWER(Lastname) = 'igwebuike' AND LOWER(School) like 'northwestern%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=95.5, UMockMeGrade=expertGrade+.445 Where LOWER(Lastname) = 'reid' AND LOWER(School) like 'stanford%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=67.1, UMockMeGrade=expertGrade+.171 Where LOWER(Lastname) = 'neal' AND LOWER(School) like 'jacksonville state%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=39.6, UMockMeGrade=expertGrade-.104 Where LOWER(Lastname) = 'elliott' AND LOWER(School) like 'texas%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=25.7, UMockMeGrade=expertGrade-.243 Where LOWER(Lastname) = 'walker' AND LOWER(School) like 'louisiana%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=1.2, UMockMeGrade=expertGrade-.482 Where LOWER(Lastname) = 'chandler' AND LOWER(School) like 'temple%' AND LOWER(POS) IN('s','fs','ss') AND DraftId=2"
        DB.ExecuteSQL(sql)



        #Edge

        sql = "UPDATE Prospect SET sparqScore=95.6, UMockMeGrade=expertGrade+.456 Where LOWER(Lastname) = 'sweat' AND LOWER(School) like 'florida state%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=87.1, UMockMeGrade=expertGrade+.371 Where LOWER(Lastname) = 'landry' AND LOWER(School) like 'boston college%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=85.0, UMockMeGrade=expertGrade+.35 Where LOWER(Lastname) = 'aruna' AND LOWER(School) like 'tulane%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=82.1, UMockMeGrade=expertGrade+.321 Where LOWER(Lastname) = 'fitts' AND LOWER(School) like 'utah%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=79.8, UMockMeGrade=expertGrade+.298 Where LOWER(Lastname) = 'jacobs' AND LOWER(School) like 'wisconsin%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=79.3, UMockMeGrade=expertGrade+.293 Where LOWER(Lastname) = 'davenport' AND LOWER(School) like 'texas%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=78.6, UMockMeGrade=expertGrade+.286 Where LOWER(Lastname) = 'chubb' AND LOWER(School) like 'north carolina%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=72.3, UMockMeGrade=expertGrade+.223 Where LOWER(Lastname) = 'kalambayi' AND LOWER(School) like 'stanford%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=62.6, UMockMeGrade=expertGrade+.126 Where LOWER(Lastname) = 'green' AND (LOWER(School) like 'southern cal%' OR Lower(School) like 'usc') AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=37.8, UMockMeGrade=expertGrade-.122 Where LOWER(Lastname) = 'haynes' AND LOWER(School) like 'mississippi%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=27.3, UMockMeGrade=expertGrade-.227 Where LOWER(firstname) = 'dorance' AND LOWER(School) like 'kansas%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=19.9, UMockMeGrade=expertGrade-.311 Where LOWER(firstname) = 'hercules' AND LOWER(School) like 'washington state%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=19.7, UMockMeGrade=expertGrade-.303 Where LOWER(Lastname) = 'adeniyi' AND LOWER(School) like 'toledo%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=.9, UMockMeGrade=expertGrade-.491 Where LOWER(Lastname) = 'jackson' AND LOWER(School) like 'jacksonville%' AND LOWER(POS) IN('edge','lb','olb','de') AND DraftId=2"
        DB.ExecuteSQL(sql)








        #Cornerbacks

        sql = "UPDATE Prospect SET sparqScore=97.9, UMockMeGrade=expertGrade+.479 Where LOWER(Lastname) = 'ward' AND LOWER(School) like 'ohio state%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=90.7, UMockMeGrade=expertGrade+.403 Where LOWER(Lastname) = 'maddox' AND LOWER(School) like 'pittsburgh%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=91.3, UMockMeGrade=expertGrade+.413 Where LOWER(Lastname) = 'alexander' AND LOWER(School) like 'louisville%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=89.3, UMockMeGrade=expertGrade+.393 Where LOWER(Lastname) = 'cruikshank' AND LOWER(School) like 'arizona%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=81.4, UMockMeGrade=expertGrade+.314 Where LOWER(Lastname) = 'chachere' AND LOWER(School) like 'san jose%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=76.2, UMockMeGrade=expertGrade+.262 Where LOWER(Lastname) = 'jackson' AND LOWER(School) like 'iowa%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=75.4, UMockMeGrade=expertGrade+.254 Where LOWER(Lastname) = 'brown' AND LOWER(School) like 'alabama%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=74.5, UMockMeGrade=expertGrade+.245 Where LOWER(Lastname) = 'thomas' AND LOWER(School) like 'oklahoma%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=73.3, UMockMeGrade=expertGrade+.233 Where LOWER(Lastname) = 'hughes' AND LOWER(School) like 'central florida%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=73.0, UMockMeGrade=expertGrade+.230 Where LOWER(Lastname) = 'haley' AND LOWER(School) like 'penn state%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=69.1, UMockMeGrade=expertGrade+.191 Where LOWER(firstname) = 'sullivan' AND LOWER(School) like 'georgia state%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=35.8, UMockMeGrade=expertGrade-.142 Where LOWER(firstname) = 'stewart' AND LOWER(School) like 'north carolina%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=34.1, UMockMeGrade=expertGrade-.159 Where LOWER(Lastname) = 'delaney' AND LOWER(School) like 'miami%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=33.7, UMockMeGrade=expertGrade-.163 Where LOWER(Lastname) = 'yiadom' AND LOWER(School) like 'boston college%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=31.2, UMockMeGrade=expertGrade-.198 Where LOWER(Lastname) = 'hill' AND LOWER(School) like 'texas%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=20.1, UMockMeGrade=expertGrade-.299 Where LOWER(Lastname) = 'wade' AND LOWER(School) like 'murray state%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=19.6, UMockMeGrade=expertGrade-.304 Where LOWER(Lastname) = 'johnson' AND LOWER(School) like 'weber state%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=17.5, UMockMeGrade=expertGrade-.122 Where LOWER(Lastname) = 'averett' AND LOWER(School) like 'alabama%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=13.2, UMockMeGrade=expertGrade-.227 Where LOWER(firstname) = 'kelly' AND LOWER(School) like 'san diego state%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=5.9, UMockMeGrade=expertGrade-.311 Where LOWER(firstname) = 'toliver' AND LOWER(School) like 'arkansas%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=2.7, UMockMeGrade=expertGrade-.303 Where LOWER(Lastname) = 'gaulden' AND LOWER(School) like 'tennessee%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=2.4, UMockMeGrade=expertGrade-.306 Where LOWER(Lastname) = 'stroman' AND LOWER(School) like 'virginia tech%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=96.5, UMockMeGrade=expertGrade+.465 Where LOWER(Lastname) = 'fitzpatrick' AND LOWER(School) like 'Alabama%' AND LOWER(POS) IN('cb','db') AND DraftId=2"
        DB.ExecuteSQL(sql)



        #Quarterbacks
        sql = "UPDATE Prospect SET sparqScore=82.1, UMockMeGrade=expertGrade+.721 Where LOWER(Lastname) = 'allen' AND LOWER(School) like 'wyoming%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=66.4, UMockMeGrade=expertGrade+.164 Where LOWER(Lastname) = 'lauletta' AND LOWER(School) like 'richmond%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=60.1, UMockMeGrade=expertGrade+.101 Where LOWER(Lastname) = 'flowers' AND LOWER(School) like 'south florida%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=40.3, UMockMeGrade=expertGrade-.907 Where LOWER(Lastname) = 'mayfield' AND LOWER(School) like 'oklahoma%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=39.3, UMockMeGrade=expertGrade-.107 Where LOWER(Lastname) = 'barrett' AND LOWER(School) like 'ohio state%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=39.2, UMockMeGrade=expertGrade-.108 Where LOWER(Lastname) = 'lee' AND LOWER(School) like 'nebraska%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=33.8, UMockMeGrade=expertGrade-.162 Where LOWER(Lastname) = 'benkert' AND LOWER(School) like 'virginia%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=31.4, UMockMeGrade=expertGrade-.186 Where LOWER(Lastname) = 'allen' AND LOWER(School) like 'arkansas%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=22.9, UMockMeGrade=expertGrade-.271 Where LOWER(Lastname) = 'darnold' AND (LOWER(School) like 'southern cal%' OR LOWER(School) like 'usc') AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=22.8, UMockMeGrade=expertGrade-.272 Where LOWER(Lastname) = 'ferguson' AND LOWER(School) like 'memphis%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=17.7, UMockMeGrade=expertGrade-.323 Where LOWER(Lastname) = 'litton' AND LOWER(School) like 'marshall%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=17.7, UMockMeGrade=expertGrade-.323 Where LOWER(Lastname) = 'shimonek' AND LOWER(School) like 'texas tech%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=4.8, UMockMeGrade=expertGrade-.452 Where LOWER(Lastname) = 'white' AND LOWER(School) like 'western kentucky%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=97.0, UMockMeGrade=expertGrade+.85 Where LOWER(Lastname) = 'rosen' AND LOWER(School) like 'ucla%' AND LOWER(POS) IN('qb') AND DraftId=2"
        DB.ExecuteSQL(sql)






        #Running Backs
        sql = "UPDATE Prospect SET sparqScore=98.5, UMockMeGrade=expertGrade+.485 Where LOWER(Lastname) = 'barkley' AND LOWER(School) like 'penn state%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=89.0, UMockMeGrade=expertGrade+.39 Where LOWER(Lastname) = 'chubb' AND LOWER(School) like 'georgia%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=83.5, UMockMeGrade=expertGrade+.335 Where LOWER(Lastname) = 'scarbrough' AND LOWER(School) like 'alabama%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=72.8, UMockMeGrade=expertGrade+.228 Where LOWER(Lastname) = 'jackson' AND LOWER(School) like 'northwestern%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=42.9, UMockMeGrade=expertGrade-.071 Where LOWER(Lastname) = 'hines' AND LOWER(School) like 'north carolina state%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=32.3, UMockMeGrade=expertGrade-.177 Where LOWER(Lastname) = 'ernsberger' AND LOWER(School) like 'western michigan%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=12.7, UMockMeGrade=expertGrade-.373 Where LOWER(Lastname) = 'franklin' AND LOWER(School) like 'western michigan%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=11.3, UMockMeGrade=expertGrade-.387 Where LOWER(Lastname) = 'williams' AND LOWER(School) like 'lsu%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=8.6, UMockMeGrade=expertGrade-.414 Where LOWER(Lastname) = 'flowers' AND LOWER(School) like 'oklahoma%' AND LOWER(POS) IN('rb') AND DraftId=2"
        DB.ExecuteSQL(sql)




        #Wide Receivers
        sql = "UPDATE Prospect SET sparqScore=97.2, UMockMeGrade=expertGrade+.472 Where LOWER(Lastname) = 'cantrell' AND LOWER(School) like 'texas tech%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=97.1, UMockMeGrade=expertGrade+.471 Where LOWER(Lastname) = 'moore' AND LOWER(School) like 'maryland%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=86.1, UMockMeGrade=expertGrade+.361 Where LOWER(Lastname) = 'sutton' AND LOWER(School) like 'smu%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=81.7, UMockMeGrade=expertGrade+.317 Where LOWER(Lastname) = 'moore' AND LOWER(School) like 'missouri%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=74.8, UMockMeGrade=expertGrade+.248 Where LOWER(Lastname) = 'weah' AND LOWER(School) like 'pittsburgh%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=64.7, UMockMeGrade=expertGrade+.147 Where LOWER(Lastname) = 'smith' AND LOWER(School) like 'central florida%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=38.9, UMockMeGrade=expertGrade-.111 Where LOWER(Lastname) = 'pringle' AND LOWER(School) like 'kansas state%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=36.7, UMockMeGrade=expertGrade-.133 Where LOWER(Lastname) = 'washington' AND LOWER(School) like 'oklahoma state%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=34.3, UMockMeGrade=expertGrade-.157 Where LOWER(Lastname) = 'cain' AND LOWER(School) like 'clemson%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=34, UMockMeGrade=expertGrade-.16 Where LOWER(Lastname) = 'ateman' AND LOWER(School) like 'oklahoma state%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=31.9, UMockMeGrade=expertGrade-.172 Where LOWER(Lastname) = 'quinn' AND LOWER(School) like 'smu%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=28.3, UMockMeGrade=expertGrade-.217 Where LOWER(Lastname) = 'wims' AND LOWER(School) like 'georgia%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=28.1, UMockMeGrade=expertGrade-.219 Where LOWER(Lastname) = 'foster' AND LOWER(School) like 'alabama%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=26.8, UMockMeGrade=expertGrade-.222 Where LOWER(Lastname) = 'kirk' AND LOWER(School) like 'texas %' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=26.1, UMockMeGrade=expertGrade-.229 Where LOWER(Lastname) = 'coutee' AND LOWER(School) like 'texas tech%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=26.0, UMockMeGrade=expertGrade-.23 Where LOWER(Lastname) = 'lasley' AND LOWER(School) like 'ucla%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=25.7, UMockMeGrade=expertGrade-.243 Where LOWER(Lastname) = 'henderson' AND LOWER(School) like 'pittsburgh%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=18.8, UMockMeGrade=expertGrade-.312 Where LOWER(Lastname) = 'mitchell' AND LOWER(School) like 'southern cal%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=17.4, UMockMeGrade=expertGrade-.326 Where LOWER(Lastname) = 'white' AND LOWER(School) like 'west virginia%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=11.3, UMockMeGrade=expertGrade-.383 Where LOWER(firstname) = 'simmie' AND LOWER(School) like 'indiana%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=8.5, UMockMeGrade=expertGrade-.415 Where LOWER(Lastname) = 'wieneke' AND LOWER(School) like 'south dakota state%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=7.3, UMockMeGrade=expertGrade-.427 Where LOWER(Lastname) = 'ridley' AND LOWER(School) like 'alabama%' AND LOWER(POS) IN('wr') AND DraftId=2"
        DB.ExecuteSQL(sql)








        #Tight Ends
        sql = "UPDATE Prospect SET sparqScore=99.3, UMockMeGrade=expertGrade+.493 Where LOWER(Lastname) = 'gesicki' AND LOWER(School) like 'penn state%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=81.9, UMockMeGrade=expertGrade+.319 Where LOWER(Lastname) = 'thomas' AND LOWER(School) like 'indiana%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=72.5, UMockMeGrade=expertGrade+.225 Where LOWER(Lastname) = 'samuels' AND LOWER(School) like 'north carolina state%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=70.98, UMockMeGrade=expertGrade+.209 Where LOWER(Lastname) = 'conklin' AND LOWER(School) like 'central michigan %' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=28.8, UMockMeGrade=expertGrade-.212 Where LOWER(Lastname) = 'andrews' AND LOWER(School) like 'oklahoma%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=20.2, UMockMeGrade=expertGrade-.298 Where LOWER(Lastname) = 'baugh' AND LOWER(School) like 'ohio state%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=20.0, UMockMeGrade=expertGrade-.30 Where LOWER(Lastname) = 'wells' AND LOWER(School) like 'san diego state%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=19.9, UMockMeGrade=expertGrade-.311 Where LOWER(Lastname) = 'smythe' AND LOWER(School) like 'notre dame%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=11.0, UMockMeGrade=expertGrade-.39 Where LOWER(Lastname) = 'izzo' AND LOWER(School) like 'florida state%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=9.8, UMockMeGrade=expertGrade-.402 Where LOWER(firstname) = 'dissly' AND LOWER(School) like 'washington%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=4.3, UMockMeGrade=expertGrade-.457 Where LOWER(Lastname) = 'thomas' AND LOWER(School) like 'mississippi state%' AND LOWER(POS) IN('te') AND DraftId=2"
        DB.ExecuteSQL(sql)






        #OLine
        sql = "UPDATE Prospect SET sparqScore=97.0, UMockMeGrade=expertGrade+.47 Where LOWER(Lastname) = 'miller' AND LOWER(School) like 'ucla%' AND LOWER(POS) IN('ot','g','c','og','oc','olt','olg','olc') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=89.1, UMockMeGrade=expertGrade+.391 Where LOWER(firstname) = 'brian' AND LOWER(School) like 'pittsburgh%' AND LOWER(POS) IN('ot','g','c','og','oc','olt','olg','olc') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=84.6, UMockMeGrade=expertGrade+.346 Where LOWER(Lastname) = 'quessenberry' AND LOWER(School) like 'ucla%' AND LOWER(POS) IN('ot','g','c','og','oc','olt','olg','olc') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=82.7, UMockMeGrade=expertGrade+.327 Where LOWER(Lastname) = 'smith' AND LOWER(School) like 'auburn%' AND LOWER(POS) IN('ot','g','c','og','oc','olt','olg','olc') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=75.4, UMockMeGrade=expertGrade+.754 Where LOWER(firstname) = 'teller' AND LOWER(School) like 'virginia%' AND LOWER(POS) IN('ot','g','c','og','oc','olt','olg','olc') AND DraftId=2"
        DB.ExecuteSQL(sql)


        #DLine
        sql = "UPDATE Prospect SET sparqScore=97.0, UMockMeGrade=expertGrade+.47 Where LOWER(Lastname) = 'vea' AND LOWER(School) like 'washington%' AND LOWER(POS) IN('de','dt','dg','dn','dlt','dlg','dln','n') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=97.1, UMockMeGrade=expertGrade+.471 Where LOWER(lastname) = 'bryan' AND LOWER(School) like 'florida%' AND LOWER(POS) IN('de','dt','dg','dn','dlt','dlg','dln','n') AND DraftId=2"
        DB.ExecuteSQL(sql)

        sql = "UPDATE Prospect SET sparqScore=93.1, UMockMeGrade=expertGrade+.931 Where LOWER(Lastname) = 'looney' AND LOWER(School) like 'california%' AND LOWER(POS) IN('de','dt','dg','dn','dlt','dlg','dln','n') AND DraftId=2"
        DB.ExecuteSQL(sql)



        return 0



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






    def PopulatePicks(sessionid,draftId=2):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("DELETE FROM PICK WHERE SessionId='{}'".format(sessionid))

            theTime = time.time()

            if(draftId==1):

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
            else:
                # 1 - 32 picks
                cur.execute("INSERT INTO PICK VALUES(1,1,1,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,2,2,'NYG',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,3,3,'NYJ',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,4,4,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,5,5,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,6,6,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,7,7,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,8,8,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,9,9,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,10,10,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,11,11,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,12,12,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,13,13,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,14,14,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,15,15,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,16,16,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,17,17,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,18,18,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,19,19,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,20,20,'DET',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,21,21,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,22,22,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,23,23,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,24,24,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,25,25,'TEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,26,26,'ATL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,27,27,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,28,28,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,29,29,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,30,30,'MIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,31,31,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(1,32,32,'PHI',null,'{}','{}')".format(sessionid, theTime))




                # 2 - 32 picks
                cur.execute("INSERT INTO PICK VALUES(2,1,33,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,2,34,'NYG',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,3,35,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,4,36,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,5,37,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,6,38,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,7,39,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,8,40,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,9,41,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,10,42,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,11,43,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,12,44,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,13,45,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,14,46,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,15,47,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,16,48,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,17,49,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,18,50,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,19,51,'DET',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,20,52,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,21,53,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,22,54,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,23,55,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,24,56,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,25,57,'TEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,26,58,'ATL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,27,59,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,28,60,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,29,61,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,30,62,'MIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,31,63,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(2,32,64,'CLE',null,'{}','{}')".format(sessionid, theTime))

                # 3
                # 43  'Compensatory Picks
                cur.execute("INSERT INTO PICK VALUES(3,1,65,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,2,66,'NYG',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,3,67,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,4,68,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,5,69,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,6,70,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,7,71,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,8,72,'NYJ',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,9,73,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,10,74,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,11,75,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,12,76,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,13,77,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,14,78,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,15,79,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,16,80,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,17,81,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,18,82,'DET',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,19,83,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,20,84,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,21,85,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,22,86,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,23,87,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,24,88,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,25,89,'TEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,26,90,'ATL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,27,91,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,28,92,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,29,93,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,30,94,'MIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,31,95,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,32,96,'BUF',null,'{}','{}')".format(sessionid, theTime))

                cur.execute("INSERT INTO PICK VALUES(3,33,97,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,34,98,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,35,99,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(3,36,100,'CIN',null,'{}','{}')".format(sessionid, theTime))


                # 4
                # 32
                cur.execute("INSERT INTO PICK VALUES(4,1,101,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,2,102,'NYG',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,3,103,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,4,104,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,5,105,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,6,106,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,7,107,'NYJ',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,8,108,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,9,109,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,10,110,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,11,111,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,12,112,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,13,113,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,14,114,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,15,115,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,16,116,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,17,117,'DET',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,18,118,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,19,119,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,20,120,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,21,121,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,22,122,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,23,123,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,24,124,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,25,125,'TEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,26,126,'ATL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,27,127,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,28,128,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,29,129,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,30,130,'PHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,31,131,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,32,132,'PHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,33,133,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,34,134,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,35,135,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,36,136,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(4,37,137,'DAL',null,'{}','{}')".format(sessionid, theTime))


                # 5
                # 32
                cur.execute("INSERT INTO PICK VALUES(5,1,138,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,2,139,'NYG',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,3,140,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,4,141,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,5,142,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,6,143,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,7,144,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,8,145,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,9,146,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,10,147,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,11,148,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,12,149,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,13,150,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,14,151,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,15,152,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,16,153,'DET',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,17,154,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,18,155,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,19,156,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,20,157,'NYJ',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,21,158,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,22,159,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,23,160,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,24,161,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,25,162,'TEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,26,163,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,27,164,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,28,165,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,29,166,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,30,167,'MIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,31,168,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,32,169,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,33,170,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,34,171,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,35,172,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,36,173,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(5,37,174,'GB',null,'{}','{}')".format(sessionid, theTime))


                # 6
                # 32
                cur.execute("INSERT INTO PICK VALUES(6,1,175,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,2,176,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,3,177,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,4,178,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,5,179,'NYJ',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,6,180,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,7,181,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,8,182,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,9,183,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,10,184,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,11,185,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,12,186,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,13,187,'BUF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,14,188,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,15,189,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,16,190,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,17,191,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,18,192,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,19,193,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,20,194,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,21,195,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,22,196,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,23,197,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,24,198,'LA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,25,199,'TEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,26,200,'ATL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,27,201,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,28,202,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,29,203,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,30,204,'MIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,31,205,'CLE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,32,206,'PHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,33,207,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,34,208,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,35,209,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,36,210,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,37,211,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,38,212,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,39,213,'MIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,40,214,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,41,215,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,42,216,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,43,217,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(6,44,218,'MIN',null,'{}','{}')".format(sessionid, theTime))




                # 7
                # 32
                cur.execute("INSERT INTO PICK VALUES(7,1,219,'NE',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,2,220,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,3,221,'IND',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,4,222,'HOU',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,5,223,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,6,224,'CHI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,7,225,'DEN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,8,226,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,9,227,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,10,228,'OAK',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,11,229,'MIA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,12,230,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,13,231,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,14,232,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,15,233,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,16,234,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,17,235,'NYJ',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,18,236,'DAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,19,237,'DET',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,20,238,'BAL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,21,239,'GB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,22,240,'SF',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,23,241,'WAS',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,24,242,'CAR',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,25,243,'KC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,26,244,'ATL',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,27,245,'NO',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,28,246,'PIT',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,29,247,'JAX',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,30,248,'SEA',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,31,249,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,32,250,'PHI',null,'{}','{}')".format(sessionid, theTime))

                cur.execute("INSERT INTO PICK VALUES(7,33,251,'LAC',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,34,252,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,35,253,'CIN',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,36,254,'ARI',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,37,255,'TB',null,'{}','{}')".format(sessionid, theTime))
                cur.execute("INSERT INTO PICK VALUES(7,38,256,'ATL',null,'{}','{}')".format(sessionid, theTime))



            theTimeEnd = time.time()




    def getUserByEmail(email):
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM UMMUser WHERE Email='{}'".format(email))

            u = cur.fetchall()

            print(u[0])

            return u


    def DeleteAllTeamNeeds():
        con = DB.getConnection()

        with con:
            cur = con.cursor()

            cur.execute("DELETE FROM TeamNeed")







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














