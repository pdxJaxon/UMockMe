#!/usr/bin/env python



import Prospects
import Teams
import DBLib
import Colleges







#Run Unit Tests to Ensure this is all behaving as expected
def doTests():

    #Go Get Raw Prospect Data From NFL.com
    rawData = Prospects.Prospect.getRawData()
    jsonData = Prospects.Prospect.stringToJson(rawData)






    #Go Get Raw Team Data
    rawTeamData = Teams.Team.getRawTeamData()
    jsonTeamData = Teams.Team.stringToJson(rawTeamData)



    #Get College Data
    rawCollegeData = Colleges.College.getCollegeData()
    jsonCollegeData = Colleges.College.stringToJson(rawCollegeData)



    #Create a New Cleaned Out DB
    DBLib.DB.createDB()

    #Delete all records in DB if there are any
    #DBLib.DB.truncateDB()



    #Pump all of our JSON records into the DB
    Prospects.Prospect.AddBatch(jsonData)

    #Query the DB to see if all our prospects made it in there
    prospects = Prospects.Prospect.getAllProspects()

    #add teams to DB
    Teams.Team.AddBatch(jsonTeamData)

    #Query Teams to make sure they made it into Db
    teams = Teams.Team.getAllTeams()

    # add teams to DB
    Colleges.College.AddBatch(jsonCollegeData)

    # Query Teams to make sure they made it into Db
    colleges = Colleges.College.getAllColleges()


    assert rawData != ""                                #Make sure we got raw data back from NFL.com
    assert jsonData != None                             #Make sure JSON object got built


    #print(jsonData)

    assert jsonData["2558834"]["lastName"] != ""        #Make sure this specific player exists
    assert jsonData["2558834"]["firstName"] != ""
    assert prospects != None                            #Make sure our query from DB returned records as expected




    '''
    #Dump all DB Records for funsies
    for p in prospects:
        print(p)


    #dump nfl team info
    for t in teams:
        print(t)



    for c in colleges:
        print(c)

    '''

#Execute our Tests
doTests()







