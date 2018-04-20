
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




    def __init__(self,sessionId,userId=0,draftId=2):

        self._sessionId = sessionId
        self._prospects = DBLib.DB.getAllProspectsForSession(sessionId)

        self._allTeamNeeds = DBLib.DB.getNeedsForAllTeams(sessionId)


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


        for n in needs:
            if(n['Need']==pos):
                picked=n['needScore']

            if(n['needScore']>highest):
                highest=n['needScore']


        if(picked>=highest):
            isHighestNeed=True


        return isHighestNeed





    def isSecondHighestNeed(self,pos,needs):
        retVal = False



        highest = 0
        secondHighest = 0
        picked = 0
        firstValue=0
        isFirst = True
        isSecond = True
        secondValue = 0


        for n in needs:
            if(isFirst):
                firstValue=n['needScore']
                isFirst = False
            elif(isSecond):
                if(n['needScore']<firstValue):
                    isSecond=False
                    secondValue = n['needScore']

            if (n['Need'] == pos):
                picked = n['needScore']


        if(picked==secondValue):
            retVal = True



        return retVal





    def isThirdHighestNeed(self,pos,needs):
        retVal = True

        highest = 0
        secondHighest = 0
        picked = 0
        firstValue = 0
        isFirst = True
        isSecond = True
        secondValue = 0
        thirdValue = 0
        isThird = True

        for n in needs:
            if (isFirst):
                firstValue = n['needScore']
                isFirst = False
            elif (isSecond):
                if (n['needScore'] < firstValue):
                    isSecond = False
                    secondValue = n['needScore']
            elif(isThird):
                if(n['needScore'] < secondValue):
                    isThird = False
                    thirdValue = n['needScore']

            if (n['Need'] == pos):
                picked = n['needScore']

        if (picked == thirdValue):
            retVal = True

        return retVal









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




        BetterProspect = None



        #lets look at the players we passed up in the ordered list of the "Best Available" and make sure we dont want one of them.

        for pup in passedUpPlayers:

            #for this passed up player, lets see how big of a need he would fill....
            thisProspectPosition = pup[2]

            thisProspectNeedValue = Draft.getNeedValueForPosition(thisProspectPosition,needs)

            randomizer = randint(1,100)

            #this is the priority of the need we just selected a person for....should be a SLAM DUNK Pick unless we passed up someone REALLY GOOD
            if(needPriority>=90):
                if ((pup[1] >= prospectPicked[9] + 1.50) and (thisProspectNeedValue >= 80)):
                    # Player too good to pass up.....80% chance they take him
                    if(randomizer>=20):
                        BetterProspect = pup
                        break
            elif(needPriority>=70):
                #how much stronger is alternate on UMockMeGrade

                if((pup[1] >= prospectPicked[9] + 1.00) and (thisProspectNeedValue >= 70)):
                    #Player too good to pass up.....80% chance they take him
                    if(randomizer>=25):
                        BetterProspect = pup
                        break
                elif ((pup[1] >= prospectPicked[9] + .75) and (thisProspectNeedValue >= 60)):
                    #if in needslist then 90% we take a look
                    if (self.isHighNeed(pup[2],needs) and randomizer>=10):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .50) or(thisProspectNeedValue >= 60)):
                    if (self.isHighNeed(pup[2],needs) and randomizer>=30):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .25) or (thisProspectNeedValue >= 60)):
                    if (self.isHighNeed(pup[2],needs) and randomizer>=30):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .10) or (thisProspectNeedValue >= 60)):
                    if (self.isHighNeed(pup[2],needs) and randomizer>=40):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9]) or (thisProspectNeedValue >= 60)):
                    if (self.isHighNeed(pup[2],needs) and randomizer>=50):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
            #The Selected Player fulfills a Need that is greater than Average.....Pretty good pick
            elif(needPriority>=50):
                # how much stronger is alternate on "NFL.COM Expert Grade:
                if ((pup[1] >= prospectPicked[9] + .5) or (thisProspectNeedValue >= 50)):
                    if (self.isHighNeed(pup[2], needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9] + .25) or (thisProspectNeedValue >= 50)):
                    if (self.isHighNeed(pup[2], needs)):
                        BetterProspect = pup
                        break
                    else:
                            BetterProspect = pup
                            break
                elif ((pup[1] >= prospectPicked[9]) or (thisProspectNeedValue >= 50)):
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





        return BetterProspect




    def getTeamNeedsForSession(sessionId,teamAbbr):
        needs = DBLib.DB.getAllNeedsForSessionTeam(sessionId,teamAbbr)
        return needs




    def getTeamNeeds(self,teamAbbr,sessionId):

        needs=[]


        if(self._allTeamNeeds):

            teamFound=False

            for t in self._allTeamNeeds:
                if(t['Abbr']==teamAbbr):
                    teamFound=True
                    needs.append(t)
        else:

            needs = Teams.Team.getNeedsByTeam2(teamAbbr)
            self._allTeamNeeds=[]
            for n in needs:
                self._allTeamNeeds.append(n)



        return needs







    def refreshCacheTeamNeeds(self,sessionId,draftId=2):
        self._allTeamNeeds = DBLib.DB.getNeedsForAllTeams(sessionId)



    def cacheTeamNeeds(self,sessionId,draftId=2):


        #theNeeds = DBLib.DB.getNeedsForAllTeams(sessionId)



        self._allTeamNeeds = Teams.Team.getNeedsForAllTeams2()









    def MarkNeedAsSelected(self,TeamAbbr,NeedPosition,sessionId):



        posAdded=False
        newNeed=[]



        for i in self._allTeamNeeds:

            if(i['Abbr']==TeamAbbr):


                if(i['Need']==NeedPosition):
                    i["needScore"]=0
                    DBLib.DB.UpdateTeamNeedForSessionDB(sessionId,TeamAbbr,NeedPosition,0,0)
                    posAdded=True

                    break







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
        elif(pPos == "DB"):
            pPos = "CB"

        return pPos



    def getDesperateneed(self,needs):
        retval=""
        for n in needs:
            if(int(n['needScore'])>int(90)):
                retval=n['Need']
                break

        return retval







    def MakePick(self,pck,sessionId,draftId=2):
        startTime = time.time()
        year=0

        if(draftId==1):
            year=2017
        else:
            year=2018

        round = pck[0]


        t = Teams.Team.getTeamByAbr(pck[3])

        city = t[0][2]
        abr = t[0][0]
        teamName = t[0][3]
        abbr = abr


        pickMade = False


        needs = self.getTeamNeeds(abbr,sessionId)




        passedUpPlayers = []
        potentialPicks = []


        isFirstPlayer = True
        iCount=0
        likelihood = randint(1, 100)
        pPos=""

        desperateNeed=self.getDesperateneed(needs)



        if(len(desperateNeed)>0):
            for p in self._prospects:
                if(p[3]==desperateNeed):
                    if(likelihood>=10):
                        Player = p[0]

                        pPos = p[3]  # Grab this Prospects position....(linebacker, wide receiver, quarterback, etc.)
                        if (pPos == "LB"):
                            pPos = "ILB"

                        if(pPos == "DB"):
                            pPos = "S"


                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)

                        pickMade = True
                        break
                    else:
                        pickMade = False
                        break

        if(pickMade==False):
            for p in self._prospects:

                iCount=iCount+1

                if(isFirstPlayer):
                    potentialPicks.append(p)
                    isFirstPlayer=False


                pPos = p[3]  # Grab this Prospects position....(linebacker, wide receiver, quarterback, etc.)
                if(pPos=="LB"):
                    pPos="ILB"

                if (pPos == "DB"):
                    pPos = "S"

                #if the current prospect is our highest need OR if we have already passed up 25 prospects, we need to make this pick.
                if (self.isHighestNeed(pPos, needs)):
                    if((round<2 and likelihood>=15) or (round<4 and likelihood>=20) or (likelihood>=30) or isFirstPlayer):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)

                        pickMade = True
                        break
                    else:
                        potentialPicks.append(p)
                elif(self.isSecondHighestNeed(pPos,needs)):
                    if((round<2 and likelihood>=40) or (round<4 and likelihood>=50) or (likelihood>=60)):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)
                        pickMade = True
                        break
                    elif((iCount>25 and  likelihood>=60) or likelihood>80 or iCount>35):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)
                        pickMade = True
                        break
                    else:
                        potentialPicks.append(p)
                elif(self.isThirdHighestNeed(pPos,needs)):
                    if((round<2 and likelihood>=80) or (round<4 and likelihood>=70) or (likelihood>=60)):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)
                        pickMade = True
                        break
                    elif ((iCount > 35 and likelihood>=70) or likelihood>85 or iCount>40):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)
                        pickMade = True
                        break
                    else:
                        potentialPicks.append(p)
                elif(self.isHighNeed(pPos,needs)):
                    if((round<2 and likelihood>=90) or (round<4 and likelihood>=80) or (likelihood>=70)):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)
                        pickMade = True
                        break
                    if ((iCount > 40 and likelihood>=70) or likelihood>80 or iCount>45):
                        Player = p[0]
                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                        self.removeProspectFromCache(sessionId, Player)
                        # needs.remove(n)
                        self.MarkNeedAsSelected(abr, pPos, sessionId)
                        pickMade = True
                        break
                    else:
                        potentialPicks.append(p)
                elif((round<4 and iCount>=40) or iCount>50):

                    BestPlayer = self.ChooseBestPotential(potentialPicks,needs)

                    Player = BestPlayer[0]

                    pPos = BestPlayer[2]

                    Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

                    self.removeProspectFromCache(sessionId, Player)
                    # needs.remove(n)
                    self.MarkNeedAsSelected(abr, pPos, sessionId)

                    pickMade = True
                    break
                else:
                    # This player was not a Match for the current Position we are looking for.....so we are passing them up for now....we will take another look later
                    passedUpPlayers.append([p[0], p[9], pPos])

        if(pickMade==False):
            if(len(potentialPicks)>0):
                BestPlayer = self.ChooseBestPotential(potentialPicks,needs)
                print("this was the best player available",BestPlayer)
            else:
                BestPlayer = self._prospects[0]

            Player = BestPlayer[0]

            pPos = BestPlayer[2]
            print("FUCK",abbr,pck[0])
            Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], abbr, Player, sessionId)

            self.removeProspectFromCache(sessionId, Player)
            # needs.remove(n)
            self.MarkNeedAsSelected(abr, pPos, sessionId)

            pickMade = True







        return True





    def ChooseBestPotential(self,lstPlayers,needsList):
        retval = []
        highestVal = 0
        playerPicked=False

        for p in lstPlayers:
            if(self.isHighestNeed(p,needsList)):
                retval=p
                playerPicked=True
        if(not playerPicked):
            for p in lstPlayers:

                if(self.isHighestNeed(p,needsList)):
                    retval = p
                    playerPicked = True

        if (not playerPicked):
            for p in lstPlayers:

                if(self.isHighestNeed(p,needsList)):
                    retval = p
                    playerPicked=True

        if (not playerPicked):
            for p in lstPlayers:

                if(self.isHighestNeed(p,needsList)):
                    retval = p
                    playerPicked=True

        if (not playerPicked):
            retval = lstPlayers[0]
            playerPicked = True




        return retval












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

        DBLib.DB.DeleteProspectForSessionDB(sessionId,ProspectId)

        self._prospects = DBLib.DB.getAllProspectsForSession(sessionId)
        #session['prospects'] = self._prospects






    def doDraft(self,sessionId,round=0,draftId=2):


        if(len(self._allTeamNeeds)==0):
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