import sqlite3 as lite


class DB:

    #Build our database if its not already created
    def createDB():
        con = lite.connect('UMockMe.db')

        try:
            with con:
                cur = con.cursor()

                cur.execute("DROP TABLE Prospect")
                cur.execute("DROP TABLE Team")
                cur.execute("DROP TABLE College")

                cur.execute("CREATE TABLE Prospect(Id Int, lastName Text, firstName Text, pos Text, height Text, weight Text, expertGrade float)")
                cur.execute("CREATE TABLE Team(Abbr Text,URL Text,City Text,Nickname Text,Conference Text,Division Text, Needs Text)")
                cur.execute("CREATE TABLE College(Id Int, Name Text, Conference Text)")
        except:
            print("Error - db already exists")          #This error just means the DB already exists......no biggy







    #Whack the DB records to start clean with each test run
    def truncateDB():
        con = lite.connect('UMockMe.db')
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM Prospect")
            cur.execute("DELETE FROM Team")
            cur.execute("DELETE FROM College")



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

        sql = "INSERT INTO Prospect VALUES({},'{}','{}','{}','{}','{}','{}')".format(id, lname, fname, pos, height, weight,
                                                                                 grade)
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
