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


    def RebuildDB():

        # tear down db to recreate from scratch (for testing only)
        DBLib.DB.TearDownDB()

        print("DB Torn Down")

        # Create a New Cleaned Out DB
        DBLib.DB.createDB()

        print("DB CREATED FROM SCRATCH")


        return True




    def RefreshStaticData():
        # Go Get Raw Prospect Data From NFL.com
        rawData = Prospects.Prospect.getRawData()
        jsonData = Prospects.Prospect.stringToJson(rawData)


        print("Prospects Retrieved")
        # print(jsonData)

        # Go Get Raw Team Data
        rawTeamData = Teams.Team.getRawTeamData()
        jsonTeamData = Teams.Team.stringToJson(rawTeamData)


        print("Teams Retrieved")
        # Get College Data
        rawCollegeData = Colleges.College.getCollegeData()
        jsonCollegeData = Colleges.College.stringToJson(rawCollegeData)


        print("Colleges Retrieved")

        # add teams to DB
        if (jsonCollegeData):
            Colleges.College.AddBatch(jsonCollegeData)

        print("Colleges Updated")

        # Pump all of our JSON records into the DB
        if (jsonData):
            Prospects.Prospect.AddBatch(jsonData)


        print("Prospects Updated")

            # add teams to DB
        if (jsonTeamData):
            Teams.Team.AddBatch(jsonTeamData)

        print("NFL Teams Updated")

        print("DB Refresh Complete")



        bigBoardData = BigBoard.Board.getRawBigBoardDataForSource()  # Empty Parm = PFF
        BigBoard.Board.AddBoard(1, 1, None, 'PFF')
        BigBoard.Board.AddBatch(1, bigBoardData)

        WalterBoard = BigBoard.Board.getRawBigBoardDataForSource(1)
        BigBoard.Board.AddBoard(2, 1, None, 'WalterFootball')
        BigBoard.Board.AddBatch(2, WalterBoard)




        Prospects.Prospect.CalculateUmockMeGrades()