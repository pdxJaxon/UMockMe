
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib


class MeetingType:













    # Will return all Teams from DB
    def getAllColleges():
        colleges = DBLib.DB.getAllColleges()
        return colleges

