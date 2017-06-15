import sqlite3 as lite
import sys
from random import *


class DB:



    def TearDownDB():
        con = lite.connect('UMockMe.db')

        try:
            with con:
                cur = con.cursor()


                cur.execute("DROP TABLE if exists Prospect")
                cur.execute("DROP TABLE if exists Team")
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

        except:
            print("")




    #Build our database if its not already created
    def createDB():
        con = lite.connect('UMockMe.db')



        try:
            with con:

                cur = con.cursor()

                cur.execute("CREATE TABLE if not exists Prospect(Id Int, lastName Text, firstName Text, pos Text, height Text, weight Text, expertGrade float,DraftProjectedRound int, DraftProjectedPick int,uMockMeGrade float,school Text)")
                cur.execute("CREATE TABLE if not exists Team(Abbr Text,URL Text,City Text,Nickname Text,Conference Text,Division Text, Needs Text)")
                cur.execute("CREATE TABLE if not exists College(Id Int, Name Text, Conference Text)")


                cur.execute("CREATE TABLE if not exists Meeting(MeetingId Int, MeetingName Text, PointValue int)")
                cur.execute("CREATE TABLE if not exists TeamPlayerMeeting(MeetingID,TeamId,ProspectId)")
                cur.execute("CREATE TABLE if not exists Draft(DraftID int, Year int)")


                #populate static data for 2017 - we dont import draft info yet as this version is just an MVP
                cur.execute("INSERT INTO DRAFT VALUES(1,2017)")


                cur.execute("CREATE TABLE if not exists Round(DraftID int,RoundId int,Round int)")
                cur.execute("INSERT INTO ROUND VALUES(1,1,1)")
                cur.execute("INSERT INTO ROUND VALUES(1,2,2)")
                cur.execute("INSERT INTO ROUND VALUES(1,3,3)")
                cur.execute("INSERT INTO ROUND VALUES(1,4,4)")
                cur.execute("INSERT INTO ROUND VALUES(1,5,5)")
                cur.execute("INSERT INTO ROUND VALUES(1,6,6)")
                cur.execute("INSERT INTO ROUND VALUES(1,7,7)")


                cur.execute("CREATE TABLE if not exists Pick(RoundId int, RoundPickNum int, OverallPickNum int, TeamAbbr Text, ProspectId int)")




                cur.execute("CREATE TABLE if not exists DeragatoryRemark(RemarkId int, Name Text, PointValue int)")
                cur.execute("CREATE TABLE if not exists ProspectDeragatoryRemark(RemarkId int, ProspectId Int)")

                cur.execute("CREATE TABLE if not exists BigBoard(BigBoardId int, DraftId int, TeamId Int, sourceId text)")
                cur.execute("CREATE TABLE if not exists BigBoardProspect(BigBoardId int, ProspectId int, Rank int)")


        except:
            print("Error - db already exists")          #This error just means the DB already exists......no biggy
            print("Error: ", sys.exc_info()[0])






    #Whack the DB records to start clean with each test run
    def truncateDB():
        con = lite.connect('UMockMe.db')
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Prospect")
            cur.execute("DELETE FROM Team")
            cur.execute("DELETE FROM College")
            cur.execute("DELETE FROM Meeting")
            cur.execute("DELETE FROM TeamPlayerMeeting")

            cur.execute("DELETE FROM DeragatoryRemark")
            cur.execute("DELETE FROM ProspectDeragatoryRemark")




    def ExecuteSQL(sql):
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()
            cur.execute(sql)











    def AddCollegeDB(Id,Name,Conference):
        sql = "INSERT INTO College VALUES({},'{}','{}')".format(Id, Name, Conference)
        #print(sql)
        DB.ExecuteSQL(sql)











    def AddTeamDB(abbr,url,city,nickname,conference,division,needs):
        sql = "INSERT INTO Team VALUES('{}','{}','{}','{}','{}','{}','{}')".format(abbr,url,city,nickname,conference,division,needs)
        #print(sql)
        DB.ExecuteSQL(sql)









    def AddProspectDB(id,lname,fname,pos,height,weight,grade,uMockMeGrade,College):

        sql = "INSERT INTO Prospect VALUES({},'{}','{}','{}','{}','{}','{}',{},{},{},'{}')".format(id, lname, fname, pos, height, weight,grade,0,0,uMockMeGrade,College)
        print(sql)
        DB.ExecuteSQL(sql)








    def getAllTeams():
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Team Order By conference,division")

            teams = cur.fetchall()

            return teams





    def getAllColleges():
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM College Order By conference")

            colleges = cur.fetchall()

            return colleges




    #Will return all prospects from DB sorted by Expert Grade in DESC Order (Best player at top)
    def getAllProspects():
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Prospect Order By Expertgrade desc")

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
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Draft WHERE Year={}".format(Year))

            TheDraft = cur.fetchall()

            return TheDraft






    def getAllRoundsByDraft(Year):
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            'lookup draft id by year'


            cur.execute("SELECT r.* FROM Round as r inner join Draft as d on d.draftid = r.draftid WHERE d.year={}".format(Year))

            TheDraft = cur.fetchall()

            return TheDraft




    def GetAllPicksForRoundDB(year,round):
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            cur.execute("SELECT p.* From Pick as p where roundId={} ".format(round))

            Picks = cur.fetchall()

            return Picks






    def GetAllPickDetailsForRoundDB(year, round):

        #Prospect(Id Int, lastName Text, firstName Text, pos Text, height Text, weight Text, expertGrade float,DraftProjectedRound int, DraftProjectedPick int)")
        #Pick(RoundId int, RoundPickNum int, OverallPickNum int, TeamAbbr Text, ProspectId int)")


        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            cur.execute("SELECT p.RoundId,p.RoundPickNum,p.OverallPickNum,p.TeamAbbr,p.ProspectId, x.firstName,x.LastName,x.pos,x.expertGrade, x.school From Pick as p inner join Prospect x on x.Id = p.ProspectId where p.roundId={} ".format(round))

            PickDetails = cur.fetchall()

        return PickDetails




    def GetCollegeById(id=-1):
        con = lite.connect('UMockMe.db')
        sql = "SELECT * FROM College WHERE id={}".format(id)

        with con:
            cur = con.cursor()
            cur.execute(sql)

            data = cur.fetchall()

        return data









    def GetProspectId(Name, POS, School,pickNum):
        con = lite.connect('UMockMe.db')

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

        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            sql = "SELECT * FROM BigBoardProspect ORDER BY Rank ASC"
            #print(sql)
            cur.execute(sql)

            t = cur.fetchall()

        return t






    def getBigBoardForTeam(teamId):

        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM BigBoard WHERE TeamId='{}'".format(teamId))

            t = cur.fetchall()

        return t






    def getBigBoardForSource(Source=1):

        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM BigBoard WHERE SourceId={}".format(Source))

            t = cur.fetchall()

        return t






    def getTeamByAbr(abr):
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM Team WHERE Abbr='{}'".format(abr))

            t=cur.fetchall()

            return t







    def UpdatePick(rnd,PickNum,OverallPickNum,Team,Player):

        #Pick(RoundId int, RoundPickNum int, OverallPickNum int, TeamAbbr Text, ProspectId int)

        sql = "Update Pick SET TeamAbbr = '{}', ProspectId={} WHERE RoundId={} AND RoundPickNum={} AND OverallPickNum={}".format(Team,Player,rnd,PickNum,OverallPickNum)
        #print(sql)
        DB.ExecuteSQL(sql)







    def PopulatePicks():
        con = lite.connect('UMockMe.db')

        with con:
            cur = con.cursor()




            # 1 - 32 picks
            cur.execute("INSERT INTO PICK VALUES(1,1,1,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(1,2,2,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(1,3,3,'CHI',null)")
            cur.execute("INSERT INTO PICK VALUES(1,4,4,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(1,5,5,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(1,6,6,'NYJ',null)")
            cur.execute("INSERT INTO PICK VALUES(1,7,7,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(1,8,8,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(1,9,9,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(1,10,10,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(1,11,11,'NO',null)")
            cur.execute("INSERT INTO PICK VALUES(1,12,12,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(1,13,13,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(1,14,14,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(1,15,15,'IND',null)")
            cur.execute("INSERT INTO PICK VALUES(1,16,16,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(1,17,17,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(1,18,18,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(1,19,19,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(1,20,20,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(1,21,21,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(1,22,22,'MIA',null)")
            cur.execute("INSERT INTO PICK VALUES(1,23,23,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(1,24,24,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(1,25,25,'HOU',null)")
            cur.execute("INSERT INTO PICK VALUES(1,26,26,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(1,27,27,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(1,28,28,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(1,29,29,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(1,30,30,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(1,31,31,'ATL',null)")
            cur.execute("INSERT INTO PICK VALUES(1,32,32,'NO',null)")










            # 2 - 32 picks
            cur.execute("INSERT INTO PICK VALUES(2,1,33,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(2,2,34,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(2,3,35,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(2,4,36,'CHI',null)")
            cur.execute("INSERT INTO PICK VALUES(2,5,37,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(2,6,38,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(2,7,39,'NYJ',null)")
            cur.execute("INSERT INTO PICK VALUES(2,8,40,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(2,9,41,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(2,10,42,'NO',null)")
            cur.execute("INSERT INTO PICK VALUES(2,11,43,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(2,12,44,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(2,13,45,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(2,14,46,'IND',null)")
            cur.execute("INSERT INTO PICK VALUES(2,15,47,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(2,16,48,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(2,17,49,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(2,18,50,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(2,19,51,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(2,20,52,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(2,21,53,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(2,22,54,'MIA',null)")
            cur.execute("INSERT INTO PICK VALUES(2,23,55,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(2,24,56,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(2,25,57,'HOU',null)")
            cur.execute("INSERT INTO PICK VALUES(2,26,58,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(2,27,59,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(2,28,60,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(2,29,61,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(2,30,62,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(2,31,63,'ATL',null)")
            cur.execute("INSERT INTO PICK VALUES(2,32,64,'CAR',null)")







            # 3
            # 43  'Compensatory Picks
            cur.execute("INSERT INTO PICK VALUES(3,1,65,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(3,2,66,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(3,3,67,'CHI',null)")
            cur.execute("INSERT INTO PICK VALUES(3,4,68,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(3,5,69,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(3,6,70,'NYJ',null)")
            cur.execute("INSERT INTO PICK VALUES(3,7,71,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(3,8,72,'NE',null)")
            cur.execute("INSERT INTO PICK VALUES(3,9,73,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,10,74,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(3,11,75,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(3,12,76,'NO',null)")
            cur.execute("INSERT INTO PICK VALUES(3,13,77,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(3,14,78,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(3,15,79,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,16,80,'IND',null)")
            cur.execute("INSERT INTO PICK VALUES(3,17,81,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(3,18,82,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,19,83,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,20,84,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(3,21,85,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(3,22,86,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,23,87,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(3,24,88,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(3,25,89,'HOU',null)")
            cur.execute("INSERT INTO PICK VALUES(3,26,90,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(3,27,91,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(3,28,92,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(3,29,93,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(3,30,94,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(3,31,95,'ATL',null)")
            cur.execute("INSERT INTO PICK VALUES(3,32,96,'NE',null)")
            cur.execute("INSERT INTO PICK VALUES(3,33,97,'MIA',null)")
            cur.execute("INSERT INTO PICK VALUES(3,34,98,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(3,35,99,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(3,36,100,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,37,101,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(3,38,102,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(3,39,103,'NO',null)")
            cur.execute("INSERT INTO PICK VALUES(3,40,104,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(3,41,105,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(3,42,106,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(3,43,107,'NYJ',null)")




            # 4
            # 38
            cur.execute("INSERT INTO PICK VALUES(4,1,108,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(4,2,109,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(4,3,110,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(4,4,111,'CHI',null)")
            cur.execute("INSERT INTO PICK VALUES(4,5,112,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(4,6,113,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(4,7,114,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(4,8,115,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(4,9,116,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(4,10,117,'CHI',null)")
            #cur.execute("INSERT INTO PICK VALUES(4,11,75,'NE',null)") - NE LOST PICK
            cur.execute("INSERT INTO PICK VALUES(4,12,118,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(4,13,119,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(4,14,120,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(4,15,121,'IND',null)")
            cur.execute("INSERT INTO PICK VALUES(4,16,122,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(4,17,123,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(4,18,124,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(4,19,125,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(4,20,126,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(4,21,127,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(4,22,128,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(4,23,129,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(4,24,130,'HOU',null)")
            cur.execute("INSERT INTO PICK VALUES(4,25,131,'NE',null)")
            cur.execute("INSERT INTO PICK VALUES(4,26,132,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(4,27,133,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(4,28,134,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(4,29,135,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(4,30,136,'ATL',null)")
            cur.execute("INSERT INTO PICK VALUES(4,31,137,'IND',null)")
            cur.execute("INSERT INTO PICK VALUES(4,32,138,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(4,33,139,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(4,34,140,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(4,35,141,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(4,36,142,'HOU',null)")
            cur.execute("INSERT INTO PICK VALUES(4,37,143,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(4,38,144,'IND',null)")




            # 5
            # 41
            cur.execute("INSERT INTO PICK VALUES(5,1,145,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(5,2,146,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(5,3,147,'CHI',null)")
            cur.execute("INSERT INTO PICK VALUES(5,4,148,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(5,5,149,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(5,6,150,'NYJ',null)")
            cur.execute("INSERT INTO PICK VALUES(5,7,151,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(5,8,152,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(5,9,153,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(5,10,154,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(5,11,155,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(5,12,156,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(5,13,157,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(5,14,158,'IND',null)")
            cur.execute("INSERT INTO PICK VALUES(5,15,159,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(5,16,160,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(5,17,161,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(5,18,162,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(5,19,163,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(5,20,164,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(5,21,165,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(5,22,166,'MIA',null)")
            cur.execute("INSERT INTO PICK VALUES(5,23,167,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(5,24,168,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(5,25,169,'HOU',null)")
            #cur.execute("INSERT INTO PICK VALUES(5,26,90,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(5,27,170,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(5,28,171,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(5,29,172,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(5,30,173,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(5,31,174,'ATL',null)")
            cur.execute("INSERT INTO PICK VALUES(5,32,175,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(5,33,176,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(5,34,177,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(5,35,178,'MIA',null)")
            cur.execute("INSERT INTO PICK VALUES(5,36,179,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(5,37,180,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(5,38,181,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(5,39,182,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(5,40,183,'NE',null)")
            cur.execute("INSERT INTO PICK VALUES(5,41,184,'MIA',null)")


            # 6
            # 35
            cur.execute("INSERT INTO PICK VALUES(6,1,185,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(6,2,186,'BAL',null)")
            cur.execute("INSERT INTO PICK VALUES(6,3,187,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(6,4,188,'CLE',null)")
            cur.execute("INSERT INTO PICK VALUES(6,5,189,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(6,6,190,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(6,7,191,'NYJ',null)")
            cur.execute("INSERT INTO PICK VALUES(6,8,192,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(6,9,193,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(6,10,194,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(6,11,195,'BUF',null)")
            cur.execute("INSERT INTO PICK VALUES(6,12,196,'NO',null)")
            cur.execute("INSERT INTO PICK VALUES(6,13,197,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(6,14,198,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(6,15,199,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(6,16,200,'NE',null)")
            cur.execute("INSERT INTO PICK VALUES(6,17,201,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(6,18,202,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(6,19,203,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(6,20,204,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(6,21,205,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(6,22,206,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(6,23,207,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(6,24,208,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(6,25,209,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(6,26,210,'SEA',null)")
            #cur.execute("INSERT INTO PICK VALUES(6,27,91,'KC',null)") PICK YANKED
            cur.execute("INSERT INTO PICK VALUES(6,28,211,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(6,29,212,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(6,30,213,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(6,31,214,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(6,32,215,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(6,33,216,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(6,34,217,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(6,35,218,'KC',null)")




            # 7
            # 35
            cur.execute("INSERT INTO PICK VALUES(7,1,219,'SF',null)")
            cur.execute("INSERT INTO PICK VALUES(7,2,220,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(7,3,221,'CHI',null)")
            cur.execute("INSERT INTO PICK VALUES(7,4,222,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(7,5,223,'MIA',null)")
            cur.execute("INSERT INTO PICK VALUES(7,6,224,'NYJ',null)")
            cur.execute("INSERT INTO PICK VALUES(7,7,225,'LAC',null)")
            cur.execute("INSERT INTO PICK VALUES(7,8,226,'SEA',null)")
            cur.execute("INSERT INTO PICK VALUES(7,9,227,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(7,10,228,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(7,11,229,'NO',null)")
            cur.execute("INSERT INTO PICK VALUES(7,12,230,'PHI',null)")
            cur.execute("INSERT INTO PICK VALUES(7,13,231,'ARI',null)")
            cur.execute("INSERT INTO PICK VALUES(7,14,232,'MIN',null)")
            cur.execute("INSERT INTO PICK VALUES(7,15,233,'CAR',null)")
            cur.execute("INSERT INTO PICK VALUES(7,16,234,'LA',null)")
            cur.execute("INSERT INTO PICK VALUES(7,17,235,'WAS',null)")
            cur.execute("INSERT INTO PICK VALUES(7,18,236,'TEN',null)")
            cur.execute("INSERT INTO PICK VALUES(7,19,237,'TB',null)")
            cur.execute("INSERT INTO PICK VALUES(7,20,238,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(7,21,239,'NE',null)")
            cur.execute("INSERT INTO PICK VALUES(7,22,240,'JAX',null)")
            cur.execute("INSERT INTO PICK VALUES(7,23,241,'NYG',null)")
            cur.execute("INSERT INTO PICK VALUES(7,24,242,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(7,25,243,'HOU',null)")
            cur.execute("INSERT INTO PICK VALUES(7,26,244,'OAK',null)")
            cur.execute("INSERT INTO PICK VALUES(7,27,245,'KC',null)")
            cur.execute("INSERT INTO PICK VALUES(7,28,246,'DAL',null)")
            cur.execute("INSERT INTO PICK VALUES(7,29,247,'GB',null)")
            cur.execute("INSERT INTO PICK VALUES(7,30,248,'PIT',null)")
            cur.execute("INSERT INTO PICK VALUES(7,31,249,'ATL',null)")
            cur.execute("INSERT INTO PICK VALUES(7,32,250,'DET',null)")
            cur.execute("INSERT INTO PICK VALUES(7,33,251,'CIN',null)")
            cur.execute("INSERT INTO PICK VALUES(7,34,252,'DEN',null)")
            cur.execute("INSERT INTO PICK VALUES(7,35,253,'DEN',null)")





