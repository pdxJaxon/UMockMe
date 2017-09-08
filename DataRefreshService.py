import Prospects
import Teams
import DBLib
import Colleges
import Drafts
import Rounds
import Picks
import BigBoard
import uuid


class DataDude:


    def NukeDB():

        # tear down db to recreate from scratch (for testing only)
        DBLib.DB.TearDownDB()

        print("DB Torn Down")

        return True






    def BuildDB():
        # Create a New Cleaned Out DB
        DBLib.DB.createDB()

        print("DB CREATED FROM SCRATCH")

        return True



    def RefreshStaticProspects():
        # Go Get Raw Prospect Data From NFL.com
        rawData = Prospects.Prospect.getRawData()
        jsonData = Prospects.Prospect.stringToJson(rawData)

        print("Prospects Retrieved")
        # print(jsonData)

        # Pump all of our JSON records into the DB
        if (jsonData):
            Prospects.Prospect.AddBatch(jsonData)

        print("Prospects Updated")






    def RefreshStaticCollegeData():
        print("Teams Retrieved")
        # Get College Data
        rawCollegeData = Colleges.College.getCollegeData()
        jsonCollegeData = Colleges.College.stringToJson(rawCollegeData)

        print("Colleges Retrieved")
        # add teams to DB
        if (jsonCollegeData):
            Colleges.College.AddBatch(jsonCollegeData)

        print("Colleges Updated")






    def RefreshStaticTeamData():


        # Go Get Raw Team Data
        rawTeamData = Teams.Team.getRawTeamData()
        jsonTeamData = Teams.Team.stringToJson(rawTeamData)





        # add teams to DB
        if (jsonTeamData):
            Teams.Team.AddBatch(jsonTeamData)

        print("NFL Teams Updated")

        print("DB Refresh Complete")

        #Prospects.Prospect.CalculateUmockMeGrades()

