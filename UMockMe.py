
import Prospects
import Teams
import DBLib
import Colleges
import Drafts
import Rounds
import Picks
import BigBoard
import uuid
import DataRefreshService




import logging
from logging.handlers import RotatingFileHandler


from flask import Flask, session
from flask import render_template

app = Flask(__name__)
app.secret_key = "I Like Turtles"
app.config['SESSION_TYPE'] = 'filesystem'



app.logger.setLevel(logging.INFO)
app.logger.disabled=False


@app.before_first_request
def initSite():
    return True

@app.route("/EditProspects")
def EditProspects():
    return render_template('EditProspects.html')






@app.route("/EditTeams")
def EditTeams():
    tms = Teams.Team.getAllTeams()

    return render_template('EditTeams.html',teams=tms)








@app.route("/CustomDraft")
def CustomDraft():
    return render_template('CustomDraft.html')




@app.route("/DBRefresh")
def refresh():
    DataRefreshService.DataDude.RebuildDB()
    DataRefreshService.DataDude.RefreshStaticData()


    return ("Database Refreshed")







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

    try:
        sessionid = session['sessionid']
    except KeyError:
        session['sessionid'] = uuid.uuid1()
        sessionid = session['sessionid']

    myDraft = Drafts.Draft(sessionid)

    myDraft.doDraft()

    picks = Picks.Pick.getAllPickDetailsForRound(2017, 1,sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 2,sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 3,sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 4,sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 5,sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 6,sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 7,sessionid)


    return render_template('QuickDraft.html',picks=picks)






if __name__ == "__main__":

    app.run(host='0.0.0.0')


