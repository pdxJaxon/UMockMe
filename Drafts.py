
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


    _prospects = Prospects.Prospect.getAllProspects()
    _allTeamNeeds = []


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



    def getTeamNeeds(teamAbbr):

        needs=[]

        if(Draft._allTeamNeeds):

            teamFound=False

            for t in Draft._allTeamNeeds:
                if(t[0]==teamAbbr):
                    teamFound=True
                    needs=t[1]


            if(teamFound==False):
                needs = Teams.Team.getStoredNeedsByTeam(teamAbbr)
                Draft._allTeamNeeds.append([teamAbbr, needs])



        else:
            needs = Teams.Team.getStoredNeedsByTeam(teamAbbr)
            Draft._allTeamNeeds.append([teamAbbr,needs])

        return needs.split(':')



    def cacheTeamNeeds():

        theTeams = Teams.Team.getAllTeams()
        for t in theTeams:
            city = t[2]
            abr = t[0]
            teamName = t[3]

            needs = Teams.Team.getNeedsByTeam(city,abr,teamName)

            Draft._allTeamNeeds.append([abr,needs])



    def removeTeamNeedFromCache(TeamAbbr,NeedPosition):
        for i in Draft._allTeamNeeds:
            if(i[0]==TeamAbbr and (NeedPosition in i[1])):
                oldNeeds = i[1]
                StartPos=str(oldNeeds).find(NeedPosition)
                LenPos = len(NeedPosition)

                newNeeds=str(oldNeeds).replace(NeedPosition,"")
                newNeeds=newNeeds.replace("::",":")

                i[1]=newNeeds
                break




    def doDraft():

        try:
            sessionid=session['sessionid']
        except KeyError:
            session['sessionid'] = uuid.uuid1()
            sessionid=session['sessionid']

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

        Draft.cacheTeamNeeds()



        #1 - get all rounds
        rounds = Draft.getAllRoundsByDraft(2017)

        # static data
        DBLib.DB.PopulatePicks(sessionid)
        
        #2 - Goto Round 1
        for rnd in rounds:

            picks = Picks.Pick.getAllPicksForRound(2017,rnd[1],sessionid)
            #print("Picks for round {} - {}".format(rnd[1],picks))



            #3 goto next pick
            for pck in picks:
                #print("Pick:",pck)

                #Get Needs For Team
                t=Teams.Team.getTeamByAbr(pck[3])


                city = t[0][2]
                abr = t[0][0]
                teamName = t[0][3]



                needs = Draft.getTeamNeeds(abr)


                #print("Needs-->",needs)


                if(len(needs) > rnd[1]-1):
                    n=needs[rnd[1]-1]
                else:
                    n=""

                #print("Team:{} Need:{}".format(teamName,n))
                if(n != ""):
                    passedUpPlayers = []
                    for p in Draft._prospects:
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

                                        Draft._prospects.remove(p)
                                        #needs.remove(n)
                                        Draft.removeTeamNeedFromCache(abr, n)
                                    else:
                                        passedUpPlayers.append([p[0],p[6],pPos])


                                else:
                                    #BetterPlayerPassedUp(needs,n,p,passedUpPlayers)
                                    Player = AlternatePick[0]

                                    for dp in Draft._prospects:
                                        if(dp[0] == AlternatePick[0]):
                                            Draft._prospects.remove(dp)

                                            #find position in needs list that matches dp[pos]
                                            # for i in needs:
                                            #     if(i[0] ==dp[3]):
                                            #         needs.remove(i)

                                            Draft.removeTeamNeedFromCache(abr, dp[3])

                                Team = abr

                                Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player,sessionid)

                                break
                            else:
                                #This player was a Match for the current Position we are looking for.....so we are passing them up for now....we will take another look later
                                passedUpPlayers.append([p[0],p[6],pPos])
                                #print("Team: {} Need:{} Pos:{}".format(abr,n,pPos))

                else: #No Needs left for Team, so pick next best player available......GAJ
                    Team = abr
                    Player = Draft._prospects[0][0]
                    #print("Blind Pick Team{} Prospect:{}".format(Team,Player))
                    Draft._prospects.remove(Draft._prospects[0])

                    Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player,sessionid)
                   





        #LOOP
        return True


























