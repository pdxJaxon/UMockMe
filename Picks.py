
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class Pick:





    # Will return all Teams from DB
    def getAllPicksForRound(year,round,sessionid):
        picks = DBLib.DB.GetAllPicksForRoundDB(year,round,sessionid)
        return picks


    def getAllPickDetailsForYear(year,sessionId):
        pickDetails - DBLib.DB.GetAllPickDetailsForRoundDB(year,sessionId)
        return pickdetails

    def getAllPickDetailsForRound(year,round,sessionid):
        pickdetails = DBLib.DB.GetAllPickDetailsForRoundDB(year,round,sessionid)
        return pickdetails



    def DeletePicksForSession(session):
        DBLib.DB.DeletePicksForSession(session)



    def UpdatePick(rnd,PickNum,OverallPickNum,Team,Player,sessionid):
        #print("UpdatePick: {} {} {} {} {}".format(rnd,PickNum,OverallPickNum,Team,Player,sessionid))
        DBLib.DB.UpdatePick(rnd,PickNum,OverallPickNum,Team,Player,sessionid)