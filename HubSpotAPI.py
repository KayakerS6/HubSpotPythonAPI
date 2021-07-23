# READ ME: The inline comments will contain notes, hints and instructions.  They will also note which sections of code to what.  It starts wih a CRM import using a .csv file.  Second (line 72), Adding contacts to a list using the same .csv file as the CRM import.  Third (line 110), Removing contacts from a list using a .csv file.  Fourth (line 144), Getting workflow information (I have this as a separate script, but included it here for completeness).  Fifth (152), Adding contacts to a workflow.  Sixth (line 166), Removing contacts from a workflow

import requests
import json
import os
import csv

#1:  CRM Import

# Items in all caps in URLs will need to be changed by you
url = "https://api.hubapi.com/crm/v3/imports?hapikey=YOUR API KEY"

data = {
    "name": "Import_Name",   #this should be named the same as the target import
    "files": [
        {
            "fileName": "File Name",   #Name of the file you want to import; I had the best luck when the file was in the same directory as the script
            "fileFormat": "CSV",
            "fileImportPage": {
                "hasHeader": True,
                "columnMappings": [
                    {
                        "ignored": False,           #'False' means the column WILL be imported
                        "columnName": "Last Name",  #This matches the file
                        "idColumnType": None,
                        "propertyName": "lastname",  #This matches the import field property name
                        "foreignKeyType": None,
                        "columnObjectType": "CONTACT",
                        "associationIdentifierColumn": False
                    },
                    {
                        "ignored": True,            #'True' means the column will NOT be imported, all of the items below "columnName" can be labled "None"
                        "columnName": "First Name",
                        "idColumnType": None,
                        "propertyName": "firstname",
                        "foreignKeyType": None,
                        "columnObjectType": "CONTACT",
                        "associationIdentifierColumn": False
                    },
                    {
                        "ignored": False,
                        "columnName": "Primary Email",
                        "idColumnType": "HUBSPOT_ALTERNATE_ID",     #This is the primary identifier for the import
                        "propertyName": "email",
                        "foreignKeyType": None,
                        "columnObjectType": "CONTACT",
                        "associationIdentifierColumn": False
                    },
                ]
            }
        }
    ]}

datastring = json.dumps(data)

payload = {"importRequest": datastring}

current_dir = os.path.dirname(__file__)
relative_path = "File Name"   #File name goes here too

absolute_file_path = os.path.join(current_dir, relative_path)

files = [
    ('files', open(absolute_file_path, 'r'))
]
print(files)


response = requests.request("POST", url, data=payload, files=files)

print(response.text.encode('utf8'))
print(response.status_code)

#2:  Adding contacts to a list using email addresses

#I changed the URL of the list and named the sections with numbers in them
#https://app.hubspot.com/contacts/HUB ID NUMBER/lists/LIST ID NUMBER

AddList = "https://api.hubapi.com/contacts/v1/lists/LIST ID NUMBER/add?hapikey=YOUR API KEY"

emailList = ""

with open("File Name") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:  #This will skip the header row
            line_count += 1
            pass
        else:
            emailList += "\""+row[2] + "\",\n"  #My emails happen to be in column c, you may need to change this.  If the csv file is open in excel column A=0, B=1, C=2, D=3...
            line_count += 1

mydata = """{
  "vids": [
  ],
  "emails": [
    """+emailList[:-2]+"""   #This will remove the extra spaces and characters at the end
  ]
}
"""

headers = {'content-type': 'application/json'}

response = requests.request("POST", AddList, headers=headers, data=mydata)

print(response.text.encode('utf8'))
print(response.status_code)

#3:  Remove contacts from a list using email addresses

RemList = "https://api.hubapi.com/contacts/v1/lists/LIST ID NUMBER/remove?hapikey=YOUR API KEY"

emailList = ""

with open("File Name") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            pass
        else:
            emailList += "\""+row[2] + "\",\n"
            line_count += 1

mydata = """{
  "vids": [
  ],
  "emails": [
    """+emailList[:-2]+"""
  ]
}
"""

headers = {'content-type': 'application/json'}

response = requests.request("POST", RemList, headers=headers, data=mydata)

print(response.text.encode('utf8'))
print(response.status_code)


#4:  To add contacts to workflows with the API, you will need the workflow ID; I have the following lines saved as their own python script.  It will return a lot of information.  There will be 2 workflow ID's, I copy the response into a text file and search by the workflow ID in the URL and use the  other ID.
import request

r = requests.get("https://api.hubapi.com/automation/v3/workflows/?hapikey=YOUR API KEY")

print(r.text.encode('utf8'))
print(r.status_code)

#5: Add contact to a workflow

with open("File Name.csv") as csv_file:     #My data gets exported as a csv, and it is easy for me to work with in python
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        response = requests.post( "https://api.hubapi.com/automation/v2/workflows/WORKFLOW ID/enrollments/contacts/" + row[2] + "Your API Key")            #the email addresses happen to be in column "C" you may need to change this.  Column "A" = row[0], "B" = row[1]...
        print(response.text.encode('utf8'))     #this line and the following line I use to monitor the progress
        print(response.status_code)

# the first result will most likely return a 404 as it tries to import the headers.  I have it that way just in case the headers get stripped out for some reason.  Successfull additions to the work flow will return 204



#6:  Remove contacts from a workflow

#Example DELETE URL: https://api.hubapi.com/automation/v2/workflows/WORKFLOW ID/enrollments/contacts/testingapis@hubspot.com?hapikey=demo Returns a 204 no content response on success. Returns a 404 error if there is no contact with the specified email address.



response = requests.delete( "https://api.hubapi.com/automation/v2/workflows/WORKFLOW ID/enrollments/contacts/EMAIL ADDRESS?hapikey=YOUR API KEY")      #the "add contact to workflow section" just needs the "response = request.post(URL)" changed to "response = request.delete(URL)".  I, personally, do not use this as the contacts will be move to "inactive" after the workflow finishes.

print(response.text.encode('utf8'))
print(response.status_code)