
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

from flask import Flask, session


class Draft:




    def __init__(self,sessionId):
        self._sessionId = sessionId
        self._prospects = Prospects.Prospect.getAllProspects()

        self._allTeamNeeds = []





    def __del__(self):
        self._prospects=""
        self._allTeamNeeds=""




    #Draft(DraftID int, Year int)")
    def AddDraft(id,Year):
        DBLib.DB.AddDraftDB(id,Year)






    # Will return all Teams from DB
    def getAllDraftByYear(Year):
        Draft = DBLib.DB.getDraftByYear(Year)
        return Draft






    def isHighestNeed(pos,needs):
        isHighestNeed=False

        highest=0
        picked=0

        for n in needs:
            if(n[1]==pos):
                picked=n[2]

            if(n[2]>highest):
                highest=n[2]


        if(picked>=highest):
            isHighestNeed=True


        return isHighestNeed





    def isHighNeed(pos,needs):
        HighNeed = False
        for n in needs:
            if(pos==needs[1]):
                if(needs[2]>=75):
                    HighNeed=True
                else:
                    HighNeed=False

        return HighNeed




    def getAllRoundsByDraft(Year):
        rounds = DBLib.DB.getAllRoundsByDraft(Year)
        return rounds



    def BetterPlayerPassedUp(needs,needPickedFor,prospectPicked,passedUpPlayers):
        BetterProspect = None


        #print("Pick:{}".format(prospectPicked))
        rn=randint(1,100)

        #try to find needPriority in NeedsList else just default to "Average" Priority value
        needPriority=50
        #print("Need:",needs)


        for n in needs:
            if(n[1]==needPickedFor):
                needPriority=n[2]



        #lets look at the players we passed up in the ordered list of the "Best Available" and make sure we dont want one of them.

        for pup in passedUpPlayers:
            #this is the priority of the need we just selected a person for....should be a SLAM DUNK Pick unless we passed up someone REALLY GOOD
            if(needPriority>=75):
                #how much stronger is alternate on "NFL.COM Expert Grade:
                #print("picked {} \nalt {}".format(prospectPicked,pup))
                if(pup[1] >= prospectPicked[6] + 1.00):
                    #Player too good to pass up.....80% chance they take him
                    if(rn>=10):
                        BetterProspect = pup
                        break
                elif (pup[1] >= prospectPicked[6] + .75):
                    #if in needslist then 90% we take a look
                    if (Draft.isHighNeed(pup[2],needs) and rn >= 10):
                        BetterProspect = pup
                        break
                    elif (rn >= 60):
                            BetterProspect = pup
                            break
                elif (pup[1] >= prospectPicked[6] + .50):
                    if (Draft.isHighNeed(pup[2],needs) and rn >= 20):
                        BetterProspect = pup
                        break
                    elif (rn >= 60):
                            BetterProspect = pup
                            break
                elif (pup[1] >= prospectPicked[6] + .25):
                    if (Draft.isHighNeed(pup[2],needs) and rn >= 30):
                        BetterProspect = pup
                        break
                    elif (rn >= 60):
                            BetterProspect = pup
                            break
                elif (pup[1] >= prospectPicked[6] + .10):
                    if (Draft.isHighNeed(pup[2],needs) and rn >= 70):
                        BetterProspect = pup
                        break
                    elif (rn >= 75):
                            BetterProspect = pup
                            break
                elif (pup[1] >= prospectPicked[6]):
                    if (Draft.isHighNeed(pup[2],needs) and rn >= 90):
                        BetterProspect = pup
                        break
                    elif (rn >= 95):
                            BetterProspect = pup
                            break
            #The Selected Player fulfills a Need that is greater than Average.....Pretty good pick
            elif(needPriority>=50):
                # how much stronger is alternate on "NFL.COM Expert Grade:
                if (pup[1] >= prospectPicked[6] + .5):
                    if (Draft.isHighNeed(pup[2], needs) and rn >= 25):
                        BetterProspect = pup
                        break
                    elif (rn >= 60):
                            BetterProspect = pup
                            break
                elif (pup[1] >= prospectPicked[6] + .25):
                    if (Draft.isHighNeed(pup[2], needs) and rn >= 50):
                        BetterProspect = pup
                        break
                    elif (rn >= 75):
                            BetterProspect = pup
                            break
                elif (pup[1] >= prospectPicked[6]):
                    if (Draft.isHighNeed(pup[2], needs) and rn >= 80):
                        BetterProspect = pup
                        break
                    elif (rn >= 95):
                            BetterProspect = pup
                            break
            else:
                if (Draft.isHighNeed(pup[2],needs) and rn >= 90):
                    BetterProspect = pup
                    break
                elif (rn >= 95):
                        BetterProspect = pup
                        break

        return BetterProspect






    def getTeamNeeds(self,teamAbbr):

        needs=[]


        if(self._allTeamNeeds):

            teamFound=False

            for t in self._allTeamNeeds:
                if(t[0][0]==teamAbbr):
                    teamFound=True
                    needs=t
                    #print("NEEDS From Get() {}".format(needs))

            if(teamFound==False):
                needs = Teams.Team.getStoredNeedsByTeam(teamAbbr)
                for n in needs:
                    self._allTeamNeeds.append(n)



        else:
            needs = Teams.Team.getStoredNeedsByTeam(teamAbbr)
            self._allTeamNeeds=[]
            for n in needs:
                self._allTeamNeeds.append(n)

        return needs









    def cacheTeamNeeds(self):

        #We need to account for position translations for OL, DL, etc.
        self._allTeamNeeds=[]

        theTeams = Teams.Team.getAllTeams()
        for t in theTeams:
            city = t[2]
            abr = t[0]
            teamName = t[3]

            #[('CHI', 'CB', 90, 1), ('CHI', 'OL', 85, 1), ('CHI', 'TE', 80, 1), ('CHI', 'LB', 75, 1),('CHI', 'S', 70, 1), ('CHI', 'QB', 65, 1)]
            needs = Teams.Team.getTeamNeeds(abr)

            for n in needs:
                if (n[1] == "C" or n[1] == "OT" or n[1] == "OG"):
                    n[1] = "OL"
                if (n[1] == "DT" or n[1] == "NT"):
                    n[1] = "DL"
                if (n[1] == "OLB" or n[1] == "ILB" or n[1] == "DE"):
                    n[1] = "LB"
                if (n[1] == "SS" or n[1] == "FS"):
                    n[1] = "S"

            self._allTeamNeeds.append(needs)









    def MarkNeedAsSelected(self,TeamAbbr,NeedPosition):

        posAdded=False
        newPosition = []

        for i in self._allTeamNeeds:
            if(i[0][0]==TeamAbbr):

                # [('CLE', 'QB', 90, 1), ('CLE', 'DL', 85, 1), ('CLE', 'LB', 80, 1), ('CLE', 'CB', 75, 1), ('CLE', 'S', 70, 1)]
                #print("Is this json - {}".format(i[0]))
                for n in i:
                    if(n[1]==NeedPosition):
                        team=n[0]
                        pos=n[1]
                        score=5
                        count=1
                        newNeed=(team,pos,score,count)

                        posAdded=True
                        i.remove(n)
                        i.append(newNeed)
                        break

                if(not posAdded):
                    newNeed=(i[0][0],NeedPosition,5,1)
                    i.append(newNeed)

                break










    def removeProspectFromCache(self,ProspectId):
        for p in self._prospects:
            if(p[0]==ProspectId):
                self._prospects.remove(p)
                break






    def doDraft(self):



        self.cacheTeamNeeds()



        #1 - get all rounds
        rounds = Draft.getAllRoundsByDraft(2017)

        # static data
        DBLib.DB.PopulatePicks(self._sessionId)   #this is only gonna work for current  year......
        
        #2 - Goto Round 1
        for rnd in rounds:

            picks = Picks.Pick.getAllPicksForRound(2017,rnd[1],self._sessionId)
            #print("Picks for round {} - {}".format(rnd[1],picks))



            #3 goto next pick
            for pck in picks:
                #print("Pick:",pck)

                #Get Needs For Team
                t=Teams.Team.getTeamByAbr(pck[3])


                city = t[0][2]
                abr = t[0][0]
                teamName = t[0][3]
                Team = abr

                pickMade=False

                needs = self.getTeamNeeds(abr)


                #print("Pick {} Team {} Needs {}".format(pck[0],abr,needs))

                needsList = needs


                if(needsList):
                    passedUpPlayers = []
                    for p in self._prospects:
                        if(p[0]!=0):
                            pPos = p[3]     #Grab this Prospects position....(linebacker, wide receiver, quarterback, etc.)


                            #Normalize the Positions
                            if(pPos=="C" or pPos=="OT" or pPos=="OG"):
                                pPos="OL"
                            if(pPos=="DT" or pPos=="NT"):
                                pPos="DL"
                            if(pPos=="OLB" or pPos=="ILB" or pPos=="DE"):
                                pPos="LB"
                            if(pPos=="SS" or pPos=="FS"):
                                pPos="S"



                            if(Draft.isHighestNeed(pPos,needs)):

                                #Were There  higher ranked players that were NOT in our need list....are we sure we want to pass em up?
                                AlternatePicks = Drafts.Draft.BetterPlayerPassedUp(needs,pPos,p,passedUpPlayers)


                                PickLikelihood = randint(1,100)


                                if(not AlternatePicks):
                                    #There were no higher ranked players....so this pick is basically a slam dunk
                                    if(PickLikelihood>=10): #90% chance that we pick this dude......
                                        Player = p[0]
                                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player, self._sessionId)
                                        #print("Pick Normal - {}".format(pck))
                                        self.removeProspectFromCache(Player)
                                        #needs.remove(n)
                                        self.MarkNeedAsSelected(abr, pPos)
                                        pickMade=True
                                        break
                                    else:
                                        #OK, we did the weird thing and passed up our slam dunk player
                                        passedUpPlayers.append([p[0],p[6],pPos])
                                        #print("A MISS ON PICK # {}".format(pck))

                                else:
                                    #BetterPlayerPassedUp(needs,n,p,passedUpPlayers)
                                    Player = AlternatePicks[0]

                                    for dp in self._prospects:
                                        if(dp[0] == AlternatePicks[0]):
                                            pickMade=True
                                            Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player, self._sessionId)
                                            self.removeProspectFromCache(dp[0])

                                            #find position in needs list that matches dp[pos]
                                            # for i in needs:
                                            #     if(i[0] ==dp[3]):
                                            #         needs.remove(i)

                                            self.MarkNeedAsSelected(abr, pPos)
                                            break

                                    break

                            else:
                                #This player was not a Match for the current Position we are looking for.....so we are passing them up for now....we will take another look later
                                passedUpPlayers.append([p[0],p[6],pPos])
                                #print("Team: {} Need:{} Pos:{}".format(abr,n,pPos))

                else: #No Needs left for Team, so pick next best player available......GAJ
                    Team = abr
                    Player = self._prospects[0][0]
                    position = self._prospects[0][3]

                    #print(self._prospects[0])

                    #print("Pick no need {}".format(pck))
                    Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player, self._sessionId)
                    pickMade=True
                    #print("Blind Pick Team{} Prospect:{}".format(Team,Player))
                    self.removeProspectFromCache(Player)
                    self.MarkNeedAsSelected(Team,position)
                    break







        #LOOP



























