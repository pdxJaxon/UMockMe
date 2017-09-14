
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
import time,datetime
import os
import re



import json

import logging
from logging.handlers import RotatingFileHandler


from flask import Flask, session, request,flash,redirect, url_for
from flask import render_template
from flask.json import jsonify




app = Flask(__name__, static_url_path='', static_folder="static")
app.secret_key = "I Like Turtles"
#app.config['SESSION_TYPE'] = 'memcached'



app.logger.setLevel(logging.INFO)
app.logger.disabled=False




@app.before_first_request
def initSite():
    if ("DATABASE_URL" in os.environ):
        if request.url.lower().startswith('http:'):
            url = request.url.lower().replace('http:', 'https:', 1)
            code = 301
            return redirect(url, code=code)



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

            return render_template('index.html',form=frm,usr=u[0][0])
    else:
        return render_template('NewAccount.html', form=frm)







@app.route("/EditTeams")
def EditTeams():
    tms = Teams.Team.getAllTeams()

    return render_template('EditTeams.html',teams=tms)





@app.route("/getQuickDraftData", methods= ['GET','POST'])
def getQuickDraftData():

    start = time.time()


    sessionid = request.args.get('sessionid')






    usr = request.args.get('usr')
    round = str(request.data)

    lengthOfString = len(round)
    colPos = round.find(":")

    round=round[colPos+1:lengthOfString-2]

    print("ROUND:{} for Session:{}".format(round,sessionid))

    startPre = time.time()
    myDraft = Drafts.Draft(sessionid)

    # When user first navigates to this page, they should have no picks yet if it's round 1
    if(int(round)<=1):
        myDraft.ClearAllPicksForUser(sessionid)

        DBLib.DB.DeleteTeamNeedsForSessionDB(sessionid)
        DBLib.DB.DeleteAllProspectsForSessionDB(sessionid)


    stopPre=time.time()

    preProcessing = stopPre-startPre
    print("PreProcessing-",str(preProcessing))


    myDraft.doDraft(sessionid,round)


    picks = DBLib.DB.getAllPicksForUser(sessionid)



    endtime = time.time()

    diff = endtime - start

    print("Elapsed overall:", str(diff))

    return (jsonify(picks))











@app.route("/getDraftData", methods= ['GET','POST'])
def getDraftData():
    sessionid = request.args.get('sessionid')

    usr = request.args.get('usr')
    print("session:",sessionid)
    myDraft = Drafts.Draft(sessionid)

    round = str(request.data)
    print("the round is:", str(round))



    lengthOfString = len(round)
    colPos = round.find(":")

    round = round[colPos + 1:lengthOfString - 2]


    # When user first navigates to this page, they should have no picks yet if it's round 1
    if (int(round) <= 1):
        myDraft.ClearAllPicksForUser(sessionid)

        DBLib.DB.DeleteTeamNeedsForSessionDB(sessionid)
        DBLib.DB.DeleteAllProspectsForSessionDB(sessionid)



    picks = myDraft.getNextPick(sessionid)





    return (jsonify(picks))




@app.route("/makePick", methods = ['GET','POST'])
def makePick():



    j = request.get_json()
    round = j.get('round')
    usr = j.get('usr')
    sessionid = j.get('sessionid')

    print("TheRound=", round)

    if (round):
        if (int(round) <= 1):
            DBLib.DB.PopulateSessionProspects(sessionid)
    else:
        DBLib.DB.PopulateSessionProspects(sessionid)

    myProspects = DBLib.DB.getAllProspectsForSession(sessionid)

    print(myProspects)
    return (jsonify(myProspects))







@app.route("/getAvailableProspects", methods = ['GET','POST'])
def getAvailableProspects():
    sessionid = request.args.get('sessionid')



    usr = request.args.get('usr')
    round = request.args.get('round')

    print("TheRound=",round)

    if(round):
        if(int(round)<=1):
            DBLib.DB.PopulateSessionProspects(sessionid)
    else:
        DBLib.DB.PopulateSessionProspects(sessionid)



    myProspects = DBLib.DB.getAllProspectsForSession(sessionid)

    print(myProspects)
    return (jsonify(myProspects))




@app.route("/CustomDraft")
def CustomDraft():
    sessionid = request.args.get('sessionid')

    usr = request.args.get('usr')

    myDraft = Drafts.Draft(sessionid)

    #When user first navigates to this page, they should have no picks yet
    myDraft.ClearAllPicksForUser(sessionid)

    DBLib.DB.DeleteTeamNeedsForSessionDB(sessionid)

    usr = request.args.get('usr')



    #return render_template('CustomDraft.html',usr=usr, sessionid=sessionid)

    return render_template('ManualDraft.html',usr=usr, sessionid=sessionid,round=0)













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
                return redirect(url_for('index',login=1,usr=user[0][1]))
            else:
                print("sorry...")
                return render_template('index.html',form=frm,login=0)
    else:
        return render_template('index.html', form=frm)







@app.route("/", methods= ['GET','POST'])
def index():
    if ("DATABASE_URL" in os.environ):
        url = r"https://www.umockme.com"

        matchObj = re.match(r'^http://',request.url,re.I)
        if(matchObj):
            print("REDIRECT {} -->{}".format(request.url, url))
            return redirect(url)

    frm = forms.Login()
    usr = request.args.get('usr')
    print("User=",usr)
    return render_template('index.html',form=frm, usr=usr)






@app.route("/ComingSoon")
def ComingSoon():
    return render_template('ComingSoon.html')







@app.route("/QuickDraft")
def QuickDraft():
    usr = request.args.get('usr')
    sessionid = request.args.get('sessionid')
    return render_template('QuickDraft.html',usr=usr,sessionid=sessionid)





@app.route("/Admin")
def Admin():
    usr = request.args.get('usr')
    sessionid = request.args.get('sessionid')
    return render_template('Admin.html', usr=usr)






@app.route("/DBNukeDB")
def NukeDB():
    DataRefreshService.DataDude.NukeDB()



    return ("Database Scrubbed - <a href='/Admin'>Return to Admin Page</a>")






@app.route("/DBRebuildDB")
def rebuildDB():
    DataRefreshService.DataDude.BuildDB()



    return ("Database Rebuilt - <a href='/Admin'>Return to Admin Page</a>")







@app.route("/DBRefreshProspects")
def refreshProspects():
    DataRefreshService.DataDude.RefreshStaticProspects()


    return ("Prospects Refreshed - <a href='/Admin'>Return to Admin Page</a>")





@app.route("/DBRefreshColleges")
def refreshColleges():
    DataRefreshService.DataDude.RefreshStaticCollegeData()


    return ("Colleges Refreshed - <a href='/Admin'>Return to Admin Page</a>")





@app.route("/DBRefreshNFLTeams")
def refreshNFLTeams():
    DataRefreshService.DataDude.RefreshStaticTeamData()


    return ("NFL Teams Refreshed - <a href='/Admin'>Return to Admin Page</a>")











if __name__ == "__main__":

    app.run(host='0.0.0.0')


