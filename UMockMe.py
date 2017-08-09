
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
import forms
import Users


import json

import logging
from logging.handlers import RotatingFileHandler


from flask import Flask, session, request,flash,redirect, url_for
from flask import render_template
from flask.json import jsonify




app = Flask(__name__, static_url_path='', static_folder="static")
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



@app.route("/NewAccount", methods= ['GET','POST'])
def NewAccount():
    frm = forms.NewAccount()

    teams = Teams.Team.getAllTeams()

    frm.FavoriteTeam.choices = [(row[0],row[2]) for row in teams]

    frm.FavoriteTeam.choices.sort()

    frm.FavoriteTeam.choices.insert(0,["0","please choose team"])

    if request.method == 'POST':
        if frm.validate() == False:
            flash("Please Validate Data Entry")
            return render_template('NewAccount.html', form = frm)
        else:

            email=frm.email.data
            fname=frm.Fname.data
            lname=frm.Lname.data
            userName=frm.userName.data
            Password=frm.Password.data
            abbr=frm.FavoriteTeam.data


            u = Users.User.AddUser(email,fname,lname,userName,Password,abbr)

            return render_template('index.html',form=frm,usr=u[0])
    else:
        return render_template('NewAccount.html', form=frm)







@app.route("/EditTeams")
def EditTeams():
    tms = Teams.Team.getAllTeams()

    return render_template('EditTeams.html',teams=tms)






@app.route("/getDraftData", methods= ['GET','POST'])
def getDraftData():
    try:
        sessionid = session['sessionid']
    except KeyError:
        session['sessionid'] = uuid.uuid1()
        sessionid = session['sessionid']


    myDraft = Drafts.Draft(sessionid)


    picks = myDraft.getNextPick(sessionid)




    '''
    myDraft.doDraft()

    picks = Picks.Pick.getAllPickDetailsForRound(2017, 1, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 2, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 3, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 4, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 5, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 6, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 7, sessionid)
    '''

    print(picks)

    return (jsonify(picks))








@app.route("/CustomDraft")
def CustomDraft():

    try:
        sessionid = session['sessionid']
    except KeyError:
        session['sessionid'] = uuid.uuid1()
        sessionid = session['sessionid']

    myDraft = Drafts.Draft(sessionid)

    myDraft.doDraft()
    usr = request.args.get('usr')
    '''
    picks = Picks.Pick.getAllPickDetailsForRound(2017, 1, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 2, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 3, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 4, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 5, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 6, sessionid)
    picks += Picks.Pick.getAllPickDetailsForRound(2017, 7, sessionid)
    '''
    picks=[]


    return render_template('CustomDraft.html',picks=picks,roundNumber=1,pickNumber=1,usr=usr)










@app.route("/DBRefresh0")
def refresh0():
    DataRefreshService.DataDude.NukeDB()



    return ("Database Scrubbed - <a href='/'>Return to Home Page</a>")






@app.route("/DBRefresh1")
def refresh1():
    DataRefreshService.DataDude.BuildDB()



    return ("Database Rebuilt - <a href='/'>Return to Home Page</a>")







@app.route("/DBRefresh2")
def refresh2():
    DataRefreshService.DataDude.RefreshStaticData()


    return ("Database Populated - <a href='/'>Return to Home Page</a>")









@app.route("/Login",  methods= ['GET','POST'])
def Login():
    frm = forms.Login()


    if request.method == 'POST':
        if frm.validate() == False:
            flash("Please Validate Data Entry")
            return render_template('index.html', form=frm)
        else:

            email = frm.email.data
            Password = frm.Password.data

            user = Users.User.ValidateLogin(email,Password)
            if(user):
                print("gotcha logged in")
                #return render_template('CustomDraft.html',usr=user)
                return redirect(url_for('CustomDraft',usr=user[0][1]))
            else:
                print("sorry...")
                return render_template('index.html',form=frm)
    else:
        return render_template('index.html', form=frm)







@app.route("/", methods= ['GET','POST'])
def index():
    frm = forms.Login()
    usr = request.args.get('usr')
    print("User=",usr)
    return render_template('index.html',form=frm, usr=usr)






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


