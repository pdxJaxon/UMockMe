
import sqlite3 as lite
import requests
from bs4 import BeautifulSoup
import re
import json
import DBLib
import Colleges




class Prospect:




    #Will return all prospects from DB sorted by Expert Grade in DESC Order (Best player at top)
    def getAllProspects(year=2018):

        prospects = DBLib.DB.getAllProspects(year)

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


    def getUserProspectById(UserId,ProspectId):


        DBLib.DB.PopulateUserProspects(UserId)


        p = DBLib.DB.getUserProspectById(UserId,ProspectId)

        return p




    def UpdateUserProspect(p,u):
        DBLib.DB.UpdateUserProspect(p,u)



    #pass in our JSON Data and pump em into the DB
    def AddBatch(jsonData,theYear):

           #print(jsonData)

            # attributes:
            # {'pos', 'weight', 'height', 'schoolYear', 'lastName', 'handSize', 'expertGrade', 'pick', 'video',
            #  'hasAnalysis', 'pickAnalysis', 'college', 'armLength', 'personId','firstName', 'fanPick'

            if(theYear=="2017"):
                DraftId=1
            else:
                DraftId=2

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

                if(collegeId==None):
                    collegeName = "Unlisted"

                else:
                    college = Colleges.College.getCollegeById(collegeId)

                    try:
                        collegeName = college[0][1].replace("'", "")
                    except:
                        collegeName = "TBD"
                        print("College Name Failure - " + str(collegeId) + " " + str(college))



                #todo: Add ProjectedDraftPick


                print(Id,lname,fname,pos,height,weight,grade,collegeName,DraftId)


                Prospect.AddProspect(Id,lname,fname,pos,height,weight,grade,0,0,0,0,collegeName,DraftId)


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



    def AddProspect(Id,Last,First,Pos,Height,Weight,Grade,rnd,pck,uMockMeGrde,sparq,college,DraftId):

        #Prospect(ProspectId integer, lastName varchar(50), firstName varchar(50), pos varchar(50), height varchar(50), weight varchar(50), expertGrade real,DraftProjectedRound integer, DraftProjectedPick integer,uMockMeGrade real,sparqScore real,school varchar(50),DraftId integer,
        DBLib.DB.AddProspectDB(Id,Last,First,Pos,Height,Weight,Grade,rnd,pck,uMockMeGrde,sparq,college,DraftId)
        print("prospect added " + Last)



    def GetProspectId(Name, POS, School,pickNum):
        prospectId = DBLib.DB.GetProspectId(Name,POS,School,pickNum)

        return prospectId