
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class Round:





    def AddRound(id,name, conference):
        DBLib.DB.AddCollegeDB(id,name, conference)






    # Will return all Teams from DB
    def getAllRoundsForDraft(Year):
        rounds = DBLib.DB.getAllRoundsByDraft(Year)
        return rounds

