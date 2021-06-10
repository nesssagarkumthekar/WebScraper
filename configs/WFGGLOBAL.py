"""
The purpose of this module is to
    1.Create variables which can be used across the application
"""

#Member Details are captured into following Arrays
Name_A=[]
Phone_A=[]
Url_A=[]
Email_A=[]
Des_A=[]
Group_A=[]
Primary_A=[]
Link_A=[]

"""
Members for whom no details are found are added into following Arrays
"""
Name_not_found=[]
Fname_not_found =[]
Lname_not_found=[]
Zip_not_found =[]

"""
Data Dictionary which contains the group and Member details. 
This is used to avoid multiple hits for the same group
"""
Group_and_Member_Dict = {}
All_groups=[]
All_members =[]

"""
CSV Files 
"""
File_Input = ''
File_output1 = ''
File_output2 =''
Folder_loc =''


"""
Counters and Message Variables
"""
Counter_global = 0
Counter_max = 0
message = ''


Titles =[ 	'CHIEF FINANCIAL OFFICER'      ,
            'CHIEF INVESTMENT OFFICER'    ,
            'FOUNDER'     ,
            'CO FOUNDER'      ,
            'OWNER'       ,
            'PRESIDENT'       ,
            'PRINCIPAL'       ,
            'EXECUTIVE DIRECTOR'      ,
            'PARTNER'     ,
            'SENIOR VICE PRESIDENT'       ,
            'VICE PRESIDENT'      ,
            'FIRST VICE PRESIDENT'    ,
            'ASSOCIATE VICE PRESIDENT'    ,
            'ASSISTANT VICE PRESIDENT'    ,
            'REGIONAL DIRECTOR'       ,
            'MANAGING DIRECTOR'       ,
            'DIRECTOR'    ,
            'BRANCH OWNER'    ,
            'BRANCH DIRECTOR'     ,
            'BRANCH MANAGER'      ,
            'ASSISTANT BRANCH MANAGER'    ,
            'DISTRICT LEADER'     ,
            'BUSINESS MANAGER'    ,
            'PRACTICE MANAGER'    ,
            'REGION MANAGER'      ,
            'MANAGER'     ,
            'ASSOCIATE MANAGER'    ]

Wf_columns_of_input_file = ['mfo_per_first_name','mfo_per_last_name','mfo_ofl_postal_code','mfo_fir_name']
Wf_Filter = 'WELLS FARGO CLEARING SERVICES, LLC'


