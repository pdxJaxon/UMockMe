
import Prospects
import Teams
import DBLib
import Colleges
import Drafts
import Rounds
import Picks
import BigBoard

import logging
from logging.handlers import RotatingFileHandler


from flask import Flask
from flask import render_template

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
app.logger.disabled=False




@app.before_first_request
def initSite():

    app.logger.info("HERE")
    # tear down db to recreate from scratch (for testing only)
    DBLib.DB.TearDownDB()

    # Create a New Cleaned Out DB
    DBLib.DB.createDB()

    # Go Get Raw Prospect Data From NFL.com
    rawData = Prospects.Prospect.getRawData()
    jsonData = Prospects.Prospect.stringToJson(rawData)

    #print(jsonData)

    # Go Get Raw Team Data
    rawTeamData = Teams.Team.getRawTeamData()
    jsonTeamData = Teams.Team.stringToJson(rawTeamData)

    # Get College Data
    rawCollegeData = Colleges.College.getCollegeData()
    jsonCollegeData = Colleges.College.stringToJson(rawCollegeData)

    # static data
    DBLib.DB.PopulatePicks()

    app.logger.info("HERE 2")


    # add teams to DB
    Colleges.College.AddBatch(jsonCollegeData)

    # Query Teams to make sure they made it into Db
    colleges = Colleges.College.getAllColleges()

    # Pump all of our JSON records into the DB
    Prospects.Prospect.AddBatch(jsonData)

    app.logger.info("HERE 3")

    # Query the DB to see if all our prospects made it in there
    prospects = Prospects.Prospect.getAllProspects()

    # add teams to DB
    Teams.Team.AddBatch(jsonTeamData)

    # Query Teams to make sure they made it into Db
    teams = Teams.Team.getAllTeams()

    # Drafts
    drafts = Drafts.Draft.getAllDraftByYear(2017)


    # Rounds
    rounds = Rounds.Round.getAllRoundsForDraft(2017)



    # Picks
    picks = Picks.Pick.getAllPicksForRound(2017, 1)

    app.logger.info("HERE 4")

    bigBoardData = BigBoard.Board.getRawBigBoardDataForSource()  # Empty Parm = PFF
    BigBoard.Board.AddBoard(1, 1, None, 'PFF')
    BigBoard.Board.AddBatch(1, bigBoardData)

    WalterBoard = BigBoard.Board.getRawBigBoardDataForSource(1)
    BigBoard.Board.AddBoard(2, 1, None, 'WalterFootball')
    BigBoard.Board.AddBatch(2, WalterBoard)


    Prospects.Prospect.CalculateUmockMeGrades()



    app.logger.info("HERE 88")




@app.route("/")
def hello():
    return render_template('index.html')



@app.route("/ComingSoon")
def ComingSoon():
    return render_template('ComingSoon.html')







@app.route("/QuickDraft")
def QuickDraft():

    '''
    picks = [
        {"picknum": 1, "team": "CLE", "player": "Myles Garrett", "position": "DE", "school": "Texas A&M"},
        {"picknum": 2, "team": "MIA", "player": "Bob Griese", "position": "QB", "school": "BYU"},
        {"picknum": 3, "team": "PIT", "player": "Lynn Swann", "position": "WR", "school": "Alabama"}
    ]
    
    SELECT p.RoundId,p.RoundPickNum,p.OverallPickNum,p.TeamAbbr,p.ProspectId, x.firstName,x.LastName,x.pos,x.expertGrade
    '''

    Drafts.Draft.doDraft()


    picks = Picks.Pick.getAllPickDetailsForRound(2017, 1)


    return render_template('QuickDraft.html',picks=picks)






if __name__ == "__main__":
    app.run()

