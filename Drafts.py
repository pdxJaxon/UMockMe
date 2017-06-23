
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







    def getAllRoundsByDraft(Year):
        rounds = DBLib.DB.getAllRoundsByDraft(Year)
        return rounds



    def BetterPlayerPassedUp(needs,needPickedFor,prospectPicked,passedUpPlayers):
        BetterProspect = None

        #print("Pick:{}".format(prospectPicked))
        rn=randint(1,100)

        for pup in passedUpPlayers:
            #print("Alternate - {}".format(pup))
            if(pup[1] >= prospectPicked[6] + 1.50):
                if(pup[2] in needs and rn>=5):
                    BetterProspect = pup
                    break
                else:
                    if(rn>=20):
                        BetterProspect = pup
                        break
            elif(pup[1] >= prospectPicked[6] + 1.25):
                if (pup[2] in needs and rn >= 20):
                    BetterProspect = pup
                    break
                else:
                    if (rn >= 35):
                        BetterProspect = pup
                        break
            elif(pup[1] >= prospectPicked[6] + 1.00):
                if (pup[2] in needs and rn >= 30):
                    BetterProspect = pup
                    break
                else:
                    if (rn >= 50):
                        BetterProspect = pup
                        break
            elif(pup[1] >= prospectPicked[6] + .80):
                if (pup[2] in needs and rn >= 50):
                    BetterProspect = pup
                    break
                else:
                    if (rn >= 75):
                        BetterProspect = pup
                        break
            elif(pup[1] >= prospectPicked[6] + .65):
                if (pup[2] in needs and rn >= 70):
                    BetterProspect = pup
                    break
                else:
                    if (rn >= 80):
                        BetterProspect = pup
                        break
            elif (pup[1] >= prospectPicked[6] + .50):
                if (pup[2] in needs and rn >= 80):
                    BetterProspect = pup
                    break
                else:
                    if (rn >= 90):
                        BetterProspect = pup
                        break
            elif (pup[1] >= prospectPicked[6]):
                if (pup[2] in needs and rn >= 90):
                    BetterProspect = pup
                    break
                else:
                    if (rn >= 95):
                        BetterProspect = pup
                        break

        return BetterProspect



    def getTeamNeeds(self,teamAbbr):

        needs=[]


        if(self._allTeamNeeds):

            teamFound=False

            for t in self._allTeamNeeds:
                if(t[0]==teamAbbr):
                    teamFound=True
                    needs=t[1]


            if(teamFound==False):
                needs = Teams.Team.getStoredNeedsByTeam(teamAbbr)
                self._allTeamNeeds.append([teamAbbr, needs])



        else:
            needs = Teams.Team.getStoredNeedsByTeam(teamAbbr)
            self._allTeamNeeds=[]
            self._allTeamNeeds.append([teamAbbr,needs])

        return needs.split(':')



    def cacheTeamNeeds(self):

        #We need to account for position translations for OL, DL, etc.
        self._allTeamNeeds=[]

        theTeams = Teams.Team.getAllTeams()
        for t in theTeams:
            city = t[2]
            abr = t[0]
            teamName = t[3]

            needs = t[6]

            self._allTeamNeeds.append([abr,needs])



    def removeTeamNeedFromCache(self,TeamAbbr,NeedPosition):

        #Need to account for pos translations

        for i in self._allTeamNeeds:
            if(i[0]==TeamAbbr and (NeedPosition in i[1])):
                oldNeeds = i[1]
                StartPos=str(oldNeeds).find(NeedPosition)
                LenPos = len(NeedPosition)

                newNeeds=str(oldNeeds).replace(NeedPosition,"")
                newNeeds=newNeeds.replace("::",":")

                i[1]=newNeeds
                break



    def removeProspectFromCache(self,ProspectId):
        for p in self._prospects:
            if(p[0]==ProspectId):
                self._prospects.remove(p)
                break






    def doDraft(self):


        ''' 
        Todo:
            For Prospects 
                get their PFF Big Board Ranking (PFF)   - DONE
                get thier Walter Football Big Board Ranking
                Get their Injury Status and history
                Get Deragatory Info
                Get SPARQ
                Link Player to College Table
                Calculate UMockeMe Grade
            For Teams
                Get Defense Base (4-3 or 3-4)
                    Update Code to classify DE as OLB or as DL depending on the base picked
                Get Their team specific Big Boards
                Get Need Details
                    Need Score for Each Position 0-100
                    Count of Players @ Each Position of Need
                Get Draft Behavior\Tendencies
                    Schools they target
                    Division and Conferences they Target
                    stats targeted at each position
                    Taking Players with Character Issues
                    Trading up and Trading Down
                get list of player Visits
            For Draft
                Build in Trade Considerations\Transactions
                
            Clean up my Tuples so I can use column names\attributes - use JSON
            
        '''

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


                needs = self.getTeamNeeds(abr)


                #print("Needs-->",needs)


                if(len(needs) > rnd[1]-1):
                    n=needs[rnd[1]-1]
                else:
                    n=""

                #print("Team:{} Need:{}".format(teamName,n))
                if(n != ""):
                    passedUpPlayers = []
                    for p in self._prospects:
                        if(p[0]!=0):
                            pPos = p[3]     #Grab this Prospects position....(linebacker, wide receiver, quarterback, etc.)
                            if(pPos=="C" or pPos=="OT" or pPos=="OG"):
                                pPos="OL"
                            if(pPos=="DT" or pPos=="NT"):
                                pPos="DL"
                            if(pPos=="OLB" or pPos=="ILB" or pPos=="DE"):
                                pPos="LB"
                            if(pPos=="SS" or pPos=="FS"):
                                pPos="S"
                            if(n==pPos):


                                AlternatePick = Drafts.Draft.BetterPlayerPassedUp(needs,n,p,passedUpPlayers)

                                PickLikelihood = randint(1,100)


                                if(not AlternatePick):
                                    if(PickLikelihood>=10): #90% chance that we pick this dude......
                                        Player = p[0]
                                        Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player, self._sessionId)
                                        self.removeProspectFromCache(Player)
                                        #needs.remove(n)
                                        self.removeTeamNeedFromCache(abr, n)
                                    else:
                                        passedUpPlayers.append([p[0],p[6],pPos])


                                else:
                                    #BetterPlayerPassedUp(needs,n,p,passedUpPlayers)
                                    Player = AlternatePick[0]

                                    for dp in self._prospects:
                                        if(dp[0] == AlternatePick[0]):
                                            Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player, self._sessionId)
                                            self.removeProspectFromCache(dp[0])

                                            #find position in needs list that matches dp[pos]
                                            # for i in needs:
                                            #     if(i[0] ==dp[3]):
                                            #         needs.remove(i)

                                            self.removeTeamNeedFromCache(abr, dp[3])





                                break
                            else:
                                #This player was a Match for the current Position we are looking for.....so we are passing them up for now....we will take another look later
                                passedUpPlayers.append([p[0],p[6],pPos])
                                #print("Team: {} Need:{} Pos:{}".format(abr,n,pPos))

                else: #No Needs left for Team, so pick next best player available......GAJ
                    Team = abr
                    Player = self._prospects[0][0]

                    Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player, self._sessionId)

                    #print("Blind Pick Team{} Prospect:{}".format(Team,Player))
                    self.removeProspectFromCache(Player)








        #LOOP



























