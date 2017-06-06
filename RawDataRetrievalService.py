#!/usr/bin/env python



import Prospects
import Teams
import DBLib
import Colleges
import Drafts
import Rounds
import Picks
import BigBoard








#Run Unit Tests to Ensure this is all behaving as expected
def doTests():



    # tear down db to recreate from scratch (for testing only)
    DBLib.DB.TearDownDB()

    # Create a New Cleaned Out DB
    DBLib.DB.createDB()





    #Go Get Raw Prospect Data From NFL.com
    rawData = Prospects.Prospect.getRawData()
    jsonData = Prospects.Prospect.stringToJson(rawData)






    #Go Get Raw Team Data
    rawTeamData = Teams.Team.getRawTeamData()
    jsonTeamData = Teams.Team.stringToJson(rawTeamData)



    #Get College Data
    rawCollegeData = Colleges.College.getCollegeData()
    jsonCollegeData = Colleges.College.stringToJson(rawCollegeData)





    #static data
    DBLib.DB.PopulatePicks()


    #Delete all records in DB if there are any
    #DBLib.DB.truncateDB()

    # add teams to DB
    Colleges.College.AddBatch(jsonCollegeData)

    # Query Teams to make sure they made it into Db
    colleges = Colleges.College.getAllColleges()



    #Pump all of our JSON records into the DB
    Prospects.Prospect.AddBatch(jsonData)

    #Query the DB to see if all our prospects made it in there
    prospects = Prospects.Prospect.getAllProspects()

    #add teams to DB
    Teams.Team.AddBatch(jsonTeamData)

    #Query Teams to make sure they made it into Db
    teams = Teams.Team.getAllTeams()




    #Drafts
    drafts = Drafts.Draft.getAllDraftByYear(2017)

    #print(drafts)


    #Rounds
    rounds = Rounds.Round.getAllRoundsForDraft(2017)

    #print(rounds)

    #Picks
    picks = Picks.Pick.getAllPicksForRound(2017,1)
    #print(picks)





    assert rawData != ""                                #Make sure we got raw data back from NFL.com
    assert jsonData != None                             #Make sure JSON object got built


    #print(jsonData)

    assert jsonData["2558834"]["lastName"] != ""        #Make sure this specific player exists
    assert jsonData["2558834"]["firstName"] != ""
    assert prospects != None                            #Make sure our query from DB returned records as expected

    bigBoardData = BigBoard.Board.getRawBigBoardDataForSource()  # Empty Parm = PFF
    BigBoard.Board.AddBoard(1, 1, None, 'PFF')
    BigBoard.Board.AddBatch(1,bigBoardData)

    WalterBoard = BigBoard.Board.getRawBigBoardDataForSource(1)
    BigBoard.Board.AddBoard(2,1,None,'WalterFootball')
    BigBoard.Board.AddBatch(2,WalterBoard)


    '''
    #Dump all DB Records for funsies
    for p in prospects:
        print(p)

    
    #dump nfl team info
    for t in teams:
        print(t)



    for c in colleges:
        print(c)

    
    


    for bb in lsBoard:
        print(bb)

    '''

    Prospects.Prospect.CalculateUmockMeGrades()

    Drafts.Draft.doDraft()


    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017,1)
    print(allPickDetailss)
    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017,2)
    print(allPickDetailss)
    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017,3)
    print(allPickDetailss)
    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017, 4)
    print(allPickDetailss)
    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017, 5)
    print(allPickDetailss)
    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017, 6)
    print(allPickDetailss)
    allPickDetailss = Picks.Pick.getAllPickDetailsForRound(2017, 7)
    print(allPickDetailss)


#Execute our Tests
doTests()







