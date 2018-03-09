
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib
import Drafts
import Teams
import Prospects
import Rounds
import Picks
from random import *
import uuid
import ast
import time,datetime

from flask import Flask, session


class Draft:




    def __init__(self,sessionId,userId=0):

        self._sessionId = sessionId
        self._prospects = DBLib.DB.getAllProspectsForSession(sessionId)
        self._allTeamNeeds=[]
        self._rounds=[]




    def __del__(self):
        pass




    #Draft(DraftID int, Year int)")
    def AddDraft(id,Year):
        DBLib.DB.AddDraftDB(id,Year)






    # Will return all Teams from DB
    def getAllDraftByYear(Year):
        Draft = DBLib.DB.getDraftByYear(Year)
        return Draft






    def isHighestNeed(self,pos,needs):
        isHighestNeed=False

        highest=0
        picked=0

        #print("DISECT:",needs,type(needs))

        for n in needs:
            if(n['Need']==pos):
                picked=n['needScore']

            if(n['needScore']>highest):
                highest=n['needScore']


        if(picked>=highest):
            isHighestNeed=True


        return isHighestNeed





    def isHighNeed(self,pos,needs):
        HighNeed = False
        for n in needs:
            if(pos==needs[1]):
                if(needs[2]>=80):
                    HighNeed=True
                else:
                    HighNeed=False

        return HighNeed




    def getAllRoundsByDraft(Year):
        rounds = DBLib.DB.getAllRoundsByDraft(Year)
        return rounds

    def getNeedValueForPosition(pos,needs):
        retVal=50
        return retVal




    def BetterPlayerPassedUp(self,needs,needPickedFor,prospectPicked,passedUpPlayers):

        needPriority = Draft.getNeedValueForPosition(needPickedFor,needs)

        startTime = time.time()


        BetterProspect = None



        #lets look at the players we passed up in the ordered list of the "Best Available" and make sure we dont want one of them.

        for pup in passedUpPlayers:

            #for this passed up player, lets see how big of a need he would fill....
            thisProspectPosition = pup[2]

            thisProspectNeedValue = Draft.getNeedValueForPosition(thisProspectPosition,needs)



            #this is the priority of the need we just selected a person for....should be a SLAM DUNK Pick unless we passed up someone REALLY GOOD
            if(needPriority>=90):
                if ((pup[1] >= prospectPicked[9] + 1.50) and (thisProspectNeedValue >= needPriority - 10)):
                    # Player too good to pass up.....80% chance they take him

                    BetterProspect = pup
                    break
            elif(needPriority>=70):
                #how much stronger is alternate on UMockMeGrade

                if((pup[1] >= prospectPicked[9] + 1.00) or (thisProspectNeedValue >= needPriority-20)):
                    #Player too good to pass up.....80% chance they take him

                        BetterProspect = pup
                        break
                elif ((pup[1] >= prospectPicked[9] + .75) or (thisProspectNeedValue >= needPriority-20)):
                    #if in needslist then 90% we take a look
                    if (self.isHighNeed(pup[2],needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .50) or(thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2],needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .25) or (thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2],needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .10) or (thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2],needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9]) or (thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2],needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
            #The Selected Player fulfills a Need that is greater than Average.....Pretty good pick
            elif(needPriority>=50):
                # how much stronger is alternate on "NFL.COM Expert Grade:
                if ((pup[1] >= prospectPicked[9] + .5) or (thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2], needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .25) or (thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2], needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9]) or (thisProspectNeedValue >= needPriority-20)):
                    if (self.isHighNeed(pup[2], needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
            else:
                if (self.isHighNeed(pup[2],needs)):
                    BetterProspect = pup
                    break
                else:
                        BetterProspect = pup
                        break

        endtime = time.time()

        print("BetterProspect Time Elapsed:",str(endtime-startTime))

        return BetterProspect




    def getTeamNeedsForSession(sessionId,teamAbbr):
        needs = DBLib.DB.getAllNeedsForSessionTeam(sessionId,teamAbbr)
        return needs




    def getTeamNeeds(self,teamAbbr):

        needs=[]


        if(self._allTeamNeeds):

            teamFound=False

            for t in self._allTeamNeeds:
                if(t['Abbr']==teamAbbr):
                    teamFound=True
                    needs.append(t)
                    print("NEEDS From Get() {}".format(needs))

            if(teamFound==False):
                needs = json.dumps(Teams.Team.getStoredNeedsByTeam(teamAbbr))
                for n in needs:
                    self._allTeamNeeds.append(n)
        else:
            needs = json.loads(Teams.Team.getStoredNeedsByTeam(teamAbbr))
            self._allTeamNeeds=[]
            for n in needs:
                self._allTeamNeeds.append(n)

        return needs









    def cacheTeamNeeds(self,sessionId,draftId=2):


        theNeeds = DBLib.DB.getNeedsForAllTeams(sessionId)


        self._allTeamNeeds = theNeeds









    def MarkNeedAsSelected(self,TeamAbbr,NeedPosition,sessionId):


        posAdded=False
        newNeed=[]



        for i in self._allTeamNeeds:

            if(i['Abbr']==TeamAbbr):

                #print("FML",i)


                if(i['Need']==NeedPosition):
                    i["needScore"]=0

                    posAdded=True

                    DBLib.DB.UpdateTeamNeedForSessionDB(i["sessionId"],i["Abbr"],i["Need"],i["needScore"],0)










    def picksPopulated(self,sessionid):
        p=DBLib.DB.getPicksForUser(sessionid)
        if(len(p)>0):
            return True
        else:
            return False


    def ClearAllPicksForUser(self,sessionId):
        DBLib.DB.DeletePicksForSession(sessionId)








    def getNextPick(self,sessionId):


        if(len(self._allTeamNeeds)==0):
            print("CACHEING SHIT")
            self.cacheTeamNeeds(sessionId)

        # 1 - get all rounds
        if(len(self._rounds)==0):

            rounds = Draft.getAllRoundsByDraft(2018)
            self._rounds = rounds


        # static data
        if(not self.picksPopulated(sessionId)):
            DBLib.DB.PopulatePicks(sessionId)  # this is only gonna work for current  year......


        p=DBLib.DB.getNextPickForUser(sessionId)



        if(len(p)>0):
            self.MakePick(p[0],sessionId)

            pu=DBLib.DB.getAllPicksForUser(sessionId)
        else:
            pu=None

        return pu




    def SelectPlayer(self,round,PickNum,OverallPickNum,Team,Player,pos,sessionid):

        Picks.Pick.UpdatePick(round, PickNum, OverallPickNum, Team, Player, sessionid)

        self.removeProspectFromCache(sessionid, Player)
        # needs.remove(n)
        self.MarkNeedAsSelected(Team, pos, sessionid)





    def NormalizePosition(pPos):
        if(pPos=="C"):
            pPos="OLC"
        elif(pPos=="OT"):
            pPos="OLT"
        elif (pPos == "OG"):
            pPos = "OLG"
        elif (pPos == "G"):
            pPos = "OLG"
        elif (pPos == "DT"):
            pPos = "DLT"
        elif (pPos == "DE"):
            pPos = "DLE"
        elif (pPos == "NT"):
            pPos = "DLN"
        elif (pPos == "LB"):
            pPos = "ILB"
        elif (pPos == "FS"):
            pPos = "S"
        elif (pPos == "SS"):
            pPos = "S"

        return pPos




    def MakePick(self,pck,sessionId,draftId=2):
        startTime = time.time()
        year=0

        if(draftId==1):
            year=2017
        else:
            year=2018



        t = Teams.Team.getTeamByAbr(pck[3])

        city = t[0][2]
        abr = t[0][0]
        teamName = t[0][3]
        abbr = abr


        pickMade = False


        needs = self.getTeamNeeds(abr)


        if(not needs):
            Teams.Team.AddNeedsForTeam(abr,city,teamName,year,draftId)
            needs=self.getTeamNeeds(abr)



        if(len(self._prospects)==0):


            DBLib.DB.PopulateSessionProspects(sessionId,draftId)


            self._prospects = DBLib.DB.getAllProspectsForSession(sessionId)



        if (needs):
            passedUpPlayers = []



            for p in self._prospects:

                #make sure we have a valid prospect by checking their ID p[0]
                if (p[0] != 0):
                    pPos = p[3]  # Grab this Prospects position....(linebacker, wide receiver, quarterback, etc.)

                    pPos= Draft.NormalizePosition(pPos)


                    #if the current prospect is our highest need OR if we have already passed up 25 prospects, we need to make this pick.
                    if (self.isHighestNeed(pPos, needs) or len(passedUpPlayers)>25):

                        if(self.isHighestNeed(pPos, needs)):
                            Player = p[0]
                            Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)
                            # print("Pick Normal - {}".format(pck))
                            self.removeProspectFromCache(sessionId, Player)
                            # needs.remove(n)
                            self.MarkNeedAsSelected(abr, pPos, sessionId)
                            pickMade = True
                            break
                        else:
                            # Were There  higher ranked players that were NOT in our need list....are we sure we want to pass em up?
                            AlternatePicks = self.BetterPlayerPassedUp(needs, pPos, p, passedUpPlayers)

                            #Account for SOME degree of Randomness in the pick. Teams do some weird shit sometimes.....
                            PickLikelihood = randint(1, 100)

                            if (not AlternatePicks):
                                # There were no higher ranked players....so this pick is basically a slam dunk
                                if (PickLikelihood >= 10):  # 90% chance that we pick this dude......
                                    Player = p[0]
                                    Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)
                                    # print("Pick Normal - {}".format(pck))
                                    self.removeProspectFromCache(sessionId,Player)
                                    # needs.remove(n)
                                    self.MarkNeedAsSelected(abr, pPos,sessionId)
                                    pickMade = True
                                    break
                                else:
                                    # OK, we did the weird thing and passed up our slam dunk player so add them to the "Passed Up List" we may come back around and reconsider them in a minute....
                                    passedUpPlayers.append([p[0], p[9], pPos])



                    else:
                        # This player was not a Match for the current Position we are looking for.....so we are passing them up for now....we will take another look later
                        passedUpPlayers.append([p[0], p[9], pPos])
                        # print("Team: {} Need:{} Pos:{}".format(abr,n,pPos))

        else:  # No Needs left for Team, so pick next best player available......GAJ
            #todo: add needs
            abbr = abr
            Player = self._prospects[0][0]
            position = self._prospects[0][3]

            # print(self._prospects[0])

            # print("Pick no need {}".format(pck))
            Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)
            pickMade = True
            # print("Blind Pick Team{} Prospect:{}".format(Team,Player))
            self.removeProspectFromCache(sessionId,Player)
            self.MarkNeedAsSelected(abbr, position,sessionId)

        step4StopTime = time.time()


        endtime = time.time()
        elapsedTime = endtime-startTime


        return True















    def getPickedPlayers(self):
        return True

    def getPickedPlayersByPos(self,pos):
        return True

    def getPickedPlayersByTeam(self,TeamAbbr):
        return True


    def getPlayersAvailable(self):
        return self._prospects

    def getPlayersAvailableByPos(self,pos):
        return True




    def removeProspectFromCache(self,sessionId,ProspectId):
        print("Player to remove",ProspectId)

        DBLib.DB.DeleteProspectForSessionDB(sessionId,ProspectId)

        self._prospects = DBLib.DB.getAllProspectsForSession(sessionId)
        #session['prospects'] = self._prospects






    def doDraft(self,sessionId,round=0,draftId=2):



        #todo: Wire DraftId
        self.cacheTeamNeeds(sessionId,draftId)


        #1 - get all rounds
        #Todo: Fix This DraftId - its curerntly year
        rounds = Draft.getAllRoundsByDraft(draftId)




        if(int(round)<=1):
            # static data
            DBLib.DB.PopulatePicks(sessionId,draftId)  # this is only gonna work for current  year......


        picks = Picks.Pick.getAllPicksForRound(draftId,round,sessionId)

        for pck in picks:
            self.MakePick(pck,sessionId)