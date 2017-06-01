
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class Pick:





    # Will return all Teams from DB
    def getAllPicksForRound(year,round):
        picks = DBLib.DB.GetAllPicksForRoundDB(year,round)
        return picks




    def UpdatePick(rnd,PickNum,OverallPickNum,Team,Player):
        print("UpdatePick: {} {} {} {} {}".format(rnd,PickNum,OverallPickNum,Team,Player))
        DBLib.DB.UpdatePick(rnd,PickNum,OverallPickNum,Team,Player)