import sqlite3 as lite
import sys


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

        except:
            print("")




    #Build our database if its not already created
    def createDB():
        con = lite.connect('UMockMe.db')



        try:
            with con:

                cur = con.cursor()

                cur.execute("CREATE TABLE if not exists Prospect(Id Int, lastName Text, firstName Text, pos Text, height Text, weight Text, expertGrade float,DraftProjectedRound int, DraftProjectedPick int)")
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


                cur.execute("CREATE TABLE if not exists Pick(RoundId int, RoundPickNum int, OverallPickNum int, TeamAbbr Text, ProspectId int)")




                cur.execute("CREATE TABLE if not exists DeragatoryRemark(RemarkId int, Name Text, PointValue int)")
                cur.execute("CREATE TABLE if not exists ProspectDeragatoryRemark(RemarkId int, ProspectId Int")


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
            cur.execute("DELETE FROM MeetingType")

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









    def AddProspectDB(id,lname,fname,pos,height,weight,grade):

        sql = "INSERT INTO Prospect VALUES({},'{}','{}','{}','{}','{}','{}',{},{})".format(id, lname, fname, pos, height, weight,
                                                                                 grade,0,0)
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
            # 5
            # 41
            # 6
            # 35
            # 7
            # 35





