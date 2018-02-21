
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class Meeting:



    # Will return all Teams from DB
    def getAllMeetings():
        meetings = DBLib.DB.getAllMeetings()
        return meetings

