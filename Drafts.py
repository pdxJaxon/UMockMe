
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



class Draft:


    _prospects = Prospects.Prospect.getAllProspects()

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

        for pup in passedUpPlayers:
            #print("Alternate - {}".format(pup))
            if(pup[1] >= prospectPicked[6] + .5):
                BetterProspect = pup
                break


        return BetterProspect




    def doDraft():

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

        #1 - get all rounds
        rounds = Draft.getAllRoundsByDraft(2017)

        
        #2 - Goto Round 1
        for rnd in rounds:

            picks = Picks.Pick.getAllPicksForRound(2017,rnd[1])
            #print("Picks for round {} - {}".format(rnd[1],picks))

            #3 goto next pick
            for pck in picks:
                #print("Pick:",pck)

                #Get Needs For Team
                t=Teams.Team.getTeamByAbr(pck[3])


                city = t[0][2]
                abr = t[0][0]
                teamName = t[0][3]

                needs = Teams.Team.getNeedsByTeam(city,abr,teamName).split(":")
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
                            pPos = p[3]
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

                                if(not AlternatePick):
                                    Player = p[0]



                                    Draft._prospects.remove(p)
                                    needs.remove(n)


                                else:
                                    #BetterPlayerPassedUp(needs,n,p,passedUpPlayers)
                                    Player = AlternatePick[0]

                                    for dp in Draft._prospects:
                                        if(dp[0] == AlternatePick[0]):
                                            Draft._prospects.remove(dp)
                                            needs.remove(n)

                                Team = abr

                                Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player)

                                break
                            else:
                                passedUpPlayers.append([p[0],p[6]])
                                #print("Team: {} Need:{} Pos:{}".format(abr,n,pPos))

                else:
                    Team = abr
                    Player = Draft._prospects[0][0]
                    #print("Blind Pick Team{} Prospect:{}".format(Team,Player))
                    Draft._prospects.remove(Draft._prospects[0])

                    Picks.Pick.UpdatePick(pck[0], pck[1], pck[2], Team, Player)





        #LOOP
        return True


























