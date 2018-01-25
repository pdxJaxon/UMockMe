
import sqlite3 as lite
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib
import Colleges




class Prospect:




    #Will return all prospects from DB sorted by Expert Grade in DESC Order (Best player at top)
    def getAllProspects():

        prospects = DBLib.DB.getAllProspects()

        return prospects






    def stringToJson(rawString):

        iFoundStart = rawString.find("\"prospects\"")
        iFoundEnd = rawString.find("\"draft\"")


        jsonString = rawString[iFoundStart+12:iFoundEnd-1]

        #print("data:\n" + jsonString)



        #print(jsonString)
        obj = json.loads(jsonString)



        return obj








    def getRawData(theYear):
        url=""
        page=""
        soup=""
        script=""
        m=""

        if(theYear=="2017"):
            url = "http://www.nfl.com/draft/2017/tracker#dt-tabs:dt-by-grade"


            page = requests.get(url)


            soup = BeautifulSoup(page.content, 'html.parser')

            script = soup.find('script', text=re.compile('nfl\.global\.dt\.data'))

            #print(soup)

            m = re.search("^\s+nfl.global.dt.data\s+=\s+{\"picks\".+",script.string,flags=re.IGNORECASE | re.MULTILINE)



            if(m):
                return m.group(0)
            else:
                return ""
        else:
            url = "http://www.nfl.com/draft/2018/tracker#dt-tabs:dt-by-grade"

            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            script = soup.find('script', text=re.compile('nfl\.global\.dt\.data'))

            # print(soup)

            m = re.search("^\s+nfl.global.dt.data\s+=\s+{\"picks\".+", script.string,
                          flags=re.IGNORECASE | re.MULTILINE)

            if (m):
                return m.group(0)
            else:
                return ""




    def getProspectById(ProspectId):
        p = DBLib.DB.getProspectById(ProspectId)

        return p



    #pass in our JSON Data and pump em into the DB
    def AddBatch(jsonData):



            # attributes:
            # {'pos', 'weight', 'height', 'schoolYear', 'lastName', 'handSize', 'expertGrade', 'pick', 'video',
            #  'hasAnalysis', 'pickAnalysis', 'college', 'armLength', 'personId','firstName', 'fanPick'



            for dude in jsonData:
                Id = jsonData[dude]["personId"]
                lname = jsonData[dude]["lastName"].replace("'","")                #parse any single quotes out of names.....it will blow up our SQL below
                fname = jsonData[dude]["firstName"].replace("'","")               #parse any single quotes out of names.....it will blow up our SQL below
                pos = jsonData[dude]["pos"]
                height = jsonData[dude]["height"]

                if(height != None):
                    height = height.replace("'"," ")                                #parse any single quotes out of names.....it will blow up our SQL below
                    height = height.replace('"','')

                weight = jsonData[dude]["weight"]
                grade = jsonData[dude]["expertGrade"]
                if(grade==None or grade==""):                                        #if expert grade not provided, just sort to bottom of list.....assume a Zero Grade.
                    grade=0
                collegeId = jsonData[dude]["college"]
                college = Colleges.College.getCollegeById(collegeId)
                collegeName = college[0][1].replace("'","")
                #todo: Add ProjectedDraftPick


                #print(Id,lname,fname,pos,height,weight,grade,collegeName)

                Prospect.AddProspect(Id,lname,fname,pos,height,weight,grade,0,collegeName)


    def CalculateUmockMeGrades():
        '''
        This SHOULD Differ for each team, but we can ceate a baseline for the UMockMeGrade
        expertGrade * 5
        PFF Grade * 3
        WalterFootball Grade
        Deragatory
        Sparq
        MeetingScore
        NeedScore
        
         
        '''
        return 0






    def AddProspect(Id,Last,First,Pos,Height,Weight,Grade,uMockMeGrde,college):
        DBLib.DB.AddProspectDB(Id,Last,First,Pos,Height,Weight,Grade,uMockMeGrde,college)




    def GetProspectId(Name, POS, School,pickNum):
        prospectId = DBLib.DB.GetProspectId(Name,POS,School,pickNum)

        return prospectId