
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






    def doDraft():

        #1 - get all rounds
        rounds = Draft.getAllRoundsByDraft(2017)



        
        #2 - Goto Round 1
        for rnd in rounds:

            picks = Picks.Pick.getAllPicksForRound(2017,rnd[1])
            #print(picks)

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



                for n in needs:
                    print("Team:{} Need:{}".format(teamName,n))
                    if(n != ""):
                        for p in Draft._prospects:
                            if(p[0]!=0):
                                pPos = p[3]
                                if(pPos=="C" or pPos=="OT" or pPos=="OG"):
                                    pPos="OL"
                                if(n==pPos):
                                    Team = abr
                                    Player = p[0]

                                    Draft._prospects.remove(p)
                                    needs.remove(n)

                                    Picks.Pick.UpdatePick(pck[0],pck[1],pck[2], Team, Player)
                                    break
                    break
            break


        #LOOP
        return True


























