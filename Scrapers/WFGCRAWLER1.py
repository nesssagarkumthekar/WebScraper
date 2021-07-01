from bs4 import BeautifulSoup
from mechanize import Browser
from configs import WFGGLOBAL as Wg
import requests
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from Lib import WFGFILEREAD1 as Wr1
import time
import os
import re

"""
The purpose of this Function is to
    1.This Function takes a member from the extracted Data
    2.The Postal code for this member is provided as an input to WellsFargo Web Site to search Advisor details
    3.The search returns links for the Advisors present in an around 25 Mile radius
    4.The links are passed to Search_page Function to check if the Advisor Exists into the link
    5.If the Advisor is present in the link, details are added into the Global Array of the found members
    6.If the Advisor is not present then Advisor Name and Postal Code is added into Not Found Array


"""


# member = [['Tyler', 'Naki'], '89410-5207']
# member = [['Matthew', 'Noble'], '43017-2950']
# member = [['Matthew','Lowe'],'75225-6330']
# member = [['Richard','Barry'],'95403-5738']
# member =[['Pearl','Maalouf'],22201-4611]


def process_members(member):
    foundflag=[]

    Fullname = member[0]
    # print(Fullname)
    Pcode = member[1]
    # print('called from crawler')
    # print(Pcode)

    br = Browser()  # Set Browser

    br.set_handle_robots(False)  # Ignore robots
    br.addheaders = [('User-agent', 'Firefox')]  # Set user Agent
    br.open('https://www.wellsfargo.com/locator/wellsfargoadvisors/search')
    ###
    br.form = list(br.forms())[0]
    # br.form['chkFNet'] = True
    # br.form['chkBIS'] = True

    br.form['zip5'] = str(Pcode).split('-')[0]
    search_zip = str(Pcode).split('-')[0]
    search_name = Fullname

    br.submit()
    soup = BeautifulSoup(br.response().read(), "lxml")

    found_flag = 'N'

    if soup.find('div', attrs={'id': 'alertBox'}) != None:
        pass
    else:
        table = soup.find_all('table', attrs={'class': 'generictext'})

        for td in table[0].find_all('td'):
            urlNotFound = 'N'
            try:
                url = td.find('div').find('strong').find('a', href=True).get('href')
                # print('this is the search url : ' + url)

            except AttributeError:
                urlNotFound = 'Y'
            except IndexError:
                urlNotFound = 'Y'

            if urlNotFound == 'N':
                # print('calling serch page for : '+ url)
                foundflag.append(search_page(url, search_name, Pcode))

                # print(found_flag)
        print(foundflag)
        print(' for ' + search_name[0] + ' ' + search_name[1])

    if 'Y' not in str(foundflag):
        url = 'EMPTY'
        found_flag = search_page(url, search_name, Pcode)
        print(found_flag)

        if found_flag != 'Y':
            Wg.Fname_not_found.append(search_name[0])
            Wg.Lname_not_found.append(search_name[1])
            Wg.Zip_not_found.append(Pcode)

    br.close()


"""
The purpose of this Function is to
    1.This Function takes a URL as an input from the Search results from the WellsFargo website search results
    2.The URL Data is scrapped to check if the member is present in the URL
    3.The Groups present in the URL and its members are captured and stored into an Array using search group function.
     This Array is used again if the Advisor from the same group is passed as an input.
     This saves additional Hits to the same URL
    3.If the mach on the Member name is found then the Search Member function is called to extract the Advisor details
"""


def search_page(url, search_name, Pcode):
    grp_found = 'N'
    gname1 = ''

    # print(Pcode)
    print(url)

    if url != 'EMPTY':
        group_exists = 'N'
        grp_found = []
        resp = requests.get(url)

        if resp.ok:
            pass
        else:
            print('error occurred')

        soup = BeautifulSoup(resp.text, "lxml")

        # group_exists ='Y'

        if soup.find('div', attrs={'id': 'ourTeams'}) != None:  # and group_exists != 'Y':

            for groups in soup.find('div', attrs={'id': 'ourTeams'}).find('ul').find_all('li'):
                grp_url = groups.find('a', href=True).get('href')
                Wg.All_groups.append(groups.find('a', href=True).text.strip())

                Wg.All_members = []

                gname = groups.find('a', href=True).text.strip()

                print("the group name is : " + gname)
                # print('group found  ' + grp_found)

                if 'of Wells Fargo Advisors' in gname:
                    grp_name = gname.split('of Wells Fargo Advisors')[0]
                else:
                    grp_name = gname

                # if grp_found == 'Y':
                #     gname1 = grp_name
                # if grp_name not in Wg.Group_and_Member_Dict.keys():
                grp_found.append(Search_for_Group(grp_url, search_name, grp_name))
                Wg.Group_and_Member_Dict[grp_name] = Wg.All_members

                # print(grp_name)
                # print(Wg.All_members)
            return grp_found
        elif soup.find('div', attrs={'id': 'ourFAs'}) != None:
            counter = 0
            try:
                for members in soup.find('div', attrs={'id': 'ourFAs'}).find('ul').find_all('li'):
                    Memurl = members.find('a', href=True).get('href')
                    names = members.find('a', href=True).text.strip()
                    names.capitalize()
                    counter = counter + 1

                    if (search_name[0].upper() in names and search_name[1].upper() in names) or \
                            (search_name[1].upper() in names and search_name[0][0:3].upper() in names): #and \
                            #Wg.Process_has_found_member == 'N':
                        # print('ai called multiple times . why?')
                        flag,element =search_member(Memurl,'')
                        Wg.Url_A.append(Memurl)
                        Wg.Group_A.append('')
                        Wg.Primary_A.append('')
                        #Wg.Process_has_found_member = 'Y'

                        return 'Y'
            except AttributeError:
                return 'N'
    else:
        Base_Url = 'https://home.wellsfargoadvisors.com/'
        Fin_Url = Base_Url + search_name[0] + '.' + search_name[1]
        # print('come inside this 1234 ')

        flag,element = search_member(Fin_Url,' ')
        print('this is found flag ' + flag + ' for ' + search_name[0] + ' ' + search_name[1])
        if flag != 'Y':
            mem_found = 'N'
        else:
            mem_found = 'Y'
            Wg.Url_A.append(Fin_Url)
            Wg.Group_A.append('')
            Wg.Primary_A.append('')

        return mem_found


"""
The purpose of this Function is to
    1.This Function takes a URL as an input from the Search results  group links
    2.The Group URL Data is scrapped and stored into an Array using search group function.
     This Array is used again if the Advisor from the same group is passed as an input.
     This saves additional Hits to the same URL
    3.This function also returns a flag if the Advisor is present in the group
"""


def Search_for_Group(Grpurl, search_name, gname):
    # print(Grpurl)
    resp1 = requests.get(Grpurl)

    if resp1.ok:
        pass
    else:
        print('bad search in group ' + Grpurl)

    soup1 = BeautifulSoup(resp1.text, 'lxml')
    found = 'N'

    for member1 in soup1.find('div', attrs={'id': 'groupFAs'}).find('ul').find_all('li'):
        try:
            names1 = member1.find('a', href=True).text.strip()
        except AttributeError:
            names1 = member1.find('span', attrs={'class': 'memberName'}).find('span', attrs={'class': 'nolink'}).text

        Wg.All_members.append(names1)

        if search_name[0].upper() in names1 and search_name[1].upper() in names1:
            found = 'Y'
            break

    if found == 'Y':
        flags = []
        for member1 in soup1.find('div', attrs={'id': 'groupFAs'}).find('ul').find_all('li'):
            try:
                url = member1.find('a', href=True).get('href')
                Wg.Url_A.append(url)
                Wg.Group_A.append(gname)
                flag, element =search_member(url,gname)
                print(element)
                flags.append(element)
            except AttributeError:
                names1 = member1.find('span', attrs={'class': 'memberName'}). \
                    find('span', attrs={'class': 'nolink'}).text.strip()
                Wg.Name_A.append(names1)
                Wg.Primary_A.append('')
                Wg.Email_A.append('')
                Wg.Link_A.append('')
                Wg.Phone_A.append(' ')
                Wg.Des_A.append('Financial Advisor')
                Wg.Url_A.append(Grpurl)
                Wg.Group_A.append(gname)

        resp1.close()
        requests.session().close()
        #valdiate_primary_member(flags)
        tempgroup = valdiate_primary_member(flags)

        for i in range(tempgroup.__len__()):
            Wg.Primary_A.append(tempgroup[i])

        return found


"""
The purpose of this Function is to
    1.If the Advisor is found in the Search result Link then his/her URL from the Search Result Link is passed
     as an input to this Function
    2.This function extracts the Advisor information and keeps into a Global Arrays

"""


# async def search_member(Memurl):
def search_member(Memurl,TeamName):
    resp = requests.get(Memurl)
    element=[]
    mem_exists='Y'
    if resp.ok:
        if resp.url != Memurl:
            mem_exists='N'
        else:
            soup = BeautifulSoup(resp.text, "lxml")

            try:
                name = soup.find('div', attrs := {'id': 'nameTitle'}).find('h1').text.strip()
            except AttributeError:
                name = \
                soup.find('div', attrs := {'id': 'nameTitle'}).find('script').contents[0].split('<h1>')[1].split('</h1>')[0]

            # print(name)
            if ',' in name:
                name = name.split(',')[0]

            Wg.Name_A.append(name)

            try:
                designation = soup.find('div', attrs := {'id': 'nameTitle'}).find_all('h2')[1].text.strip()
            except IndexError:
                try:
                    designation = soup.find('div', attrs := {'id': 'nameTitle'}).find_all('h2')[0].text.strip()
                except AttributeError:
                    designation = ' '

            if '-' in designation:
                designation = designation.split('-')[0]

            Wg.Des_A.append(designation)

            # if designation.strip().upper() in Wg.Titles:
            #     Wg.Primary_A.append('Y')
            # else:
            #     Wg.Primary_A.append('N')
            Name1=name.split(' ')
            if Name1[0] in TeamName or Name1[1] in TeamName:
                Fuzzy1 = 'Y'
            else:
                Fuzzy1 = 'N'

            if designation.strip().upper() in Wg.Titles:
                Fuzzy2 = 'Y'
            else:
                Fuzzy2 = 'N'
            try:
                rank = Wg.Titles.index(designation.strip().upper())
            except ValueError:
                rank = 100

            Wg.Link_A.append('')

            Address_tag = soup.find('div', attrs := {'id': 'address'})

            ph2 = ''
            for lines in Address_tag.select('strong'):

                if 'Phone' in lines.text:
                    ph = lines.nextSibling.strip()
                    ph1 = re.sub("(\n)|(\r)|(\t)|(\xa0)|(\n),", "", ph)
                    ph2 = ph1.replace('|', ',').replace('                                                ', '').replace(
                        '               ', '')

            if ph2 != '':
                Wg.Phone_A.append(ph2)
            else:
                Wg.Phone_A.append(' ')

            try:
                email = Address_tag.find('a', href=True).get('href').split(':')[1]
            except AttributeError:
                email = ''

            Wg.Email_A.append(email)
            element = (name, Fuzzy1, Fuzzy2, rank)

        # pass
    else:
        print('error from search member')

    return mem_exists,element


"""
The purpose of this module is to
    1.Create a GUI (Graphical User Interface) for Selection of Input and Output File
    2.To provide Error information if any Error is encountered
    3.Provide the status of the progress
"""


def create_UI():
    root = Tk()
    root.geometry('1000x600')
    root.resizable(0, 0)
    style = Style()
    style.configure('W.TButton', font=
    ('calibri', 10, 'bold', 'underline'),
                    foreground='red')

    root.title('WellsFargo Advisor Extractor')
    Label(root, text='Welcome to WellsFargo Advisor Extraction process', font='arial 20')
    display = Entry(root)

    Text = StringVar()
    Output_Folder_Loc = StringVar()
    private_key = StringVar()
    mode = StringVar()
    Result = StringVar()
    exc_var = StringVar()
    Complete_Msg_Part1 = StringVar()
    Complete_Msg_Part2 = StringVar()
    Ouptut_File_1 = StringVar()
    Output_file_2 = StringVar()
    Choose_Folder_msg = StringVar()
    location = ''
    display = Entry(root)
    File_success = StringVar()
    Notify = StringVar()
    # pb1= tkinter.ttk.Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
    # pb1.pack(expand=True)
    # pb1.place(x=290, y=500)
    current_system_pid = os.getpid()

    Notify.set("\n"
               "\nDefault location for Storing the results CSV File is D:/WebScraper/Logs        "
               "\n")
    Choose_Folder_msg.set("Optional: Select a Location to Store Output Files :")

    Output_Folder_Loc.set("Default as above")

    def Exit():
        # current_system_pid = os.getpid()
        # psutil.Process(current_system_pid).terminate()
        # ThisSystem = ThisSystem.terminate()
        root.destroy()

    def Reset():
        Text.set("")
        private_key.set("")
        mode.set("")
        Result.set("")
        File_success.set("")
        exc_var.set("")
        Complete_Msg_Part1.set("")
        Complete_Msg_Part2.set("")
        Ouptut_File_1.set("")
        Output_file_2.set("")
        Output_Folder_Loc.set("Default as above")

    def Browse():

        Wg.File_Input = filedialog.askopenfile(initialdir="C:/Users/P7165881/Desktop/Brodridge/")

        try:
            File_success.set(Wg.File_Input.name + ' File opened Successfully')
            Text.set(Wg.File_Input.name)
        except AttributeError:
            File_success.set('No File selected, Please select a File')
            Text.set(" ")

        Label(root, font='arial 12', textvariable=File_success).place(x=60, y=280)

    def Select_A_Folder():
        location = filedialog.askdirectory(initialdir="D:/WebScraper/Logs")
        print('this is the location ------> ' + location)
        Output_Folder_Loc.set(location)

    def Start():
        Base_loc = 'D:/WebScraper/Logs'
        start_time = time.strftime('%X %x %Z')
        print('Start Time time is : ' + start_time)

        print(location)

        if location != '':
            Wg.Folder_loc = location
        else:
            Output_Folder_Loc.set(location)
            Wg.Folder_loc = Base_loc

        try:
            input_file = Wg.File_Input.name
            try:
                Wr1.Start_Process(input_file)
                Complete_Msg_Part1.set('Completed the extraction process, Files :')
                Ouptut_File_1.set(Wg.File_output1)
                Output_file_2.set(Wg.File_output2)
                Complete_Msg_Part2.set(' are created successfully')
                Label(root, font='Calibri 12 ', textvariable=Complete_Msg_Part1).place(x=60, y=320)
                Label(root, font='Calibri 12 bold', textvariable=Ouptut_File_1).place(x=120, y=340)
                Label(root, font='Calibri 12 bold', textvariable=Output_file_2).place(x=120, y=360)
                Label(root, font='Calibri 12 ', textvariable=Complete_Msg_Part2).place(x=290, y=380)
                # vars = dir(Wg)
                # for var in vars:
                # del var
            except PermissionError:
                Wg.message = 'Permission to write into a file is denied. ' \
                             'Please check if the file is already open or ' \
                             'a folder is accessible to the application'
                print(Wg.message)
                exc_var.set(Wg.message)
                lable2 = tkinter.ttk.Label(root, font='Calibri 12 bold', textvariable=exc_var, background="red").place(
                    x=60,
                    y=500)
        except AttributeError:
            Wg.message = ' First Select a File!'
            exc_var.set(Wg.message)
            lable2 = tkinter.ttk.Label(root, font='Calibri 12 bold', textvariable=exc_var, background="red").place(
                x=60,
                y=500)

    Label(root, font='arial 12', text='Location of Input file containing Members').place(x=60, y=60)

    Entry(root, font='arial 10', textvariable=Text, width=50).place(x=390, y=60)

    btn1 = Button(root, text='Browse', command=Browse).place(x=790, y=60)
    btn_help = Button(root, text='HELP', command=Browse).place(x=880, y=60)
    lable1 = tkinter.ttk.Label(root, font='Calibri 12', textvariable=Notify, background="light green").place(x=60,
                                                                                                             y=100)

    tkinter.ttk.Label(select=lable1).pack(fill=tkinter.X, pady=10)

    lable2 = tkinter.ttk.Label(root, font='Calibri 12', textvariable=Choose_Folder_msg).place(x=60, y=200)
    Entry(root, font='arial 10', textvariable=Output_Folder_Loc, width=50).place(x=390, y=200)
    btn_help = Button(root, text='Folder', command=Select_A_Folder).place(x=880, y=200)
    btn2 = Button(root, text='RESET', command=Reset).place(x=80, y=450)
    btn3 = Button(root, text='EXIT', style='W.TButton', command=Exit).place(x=180, y=450)
    btn4 = Button(root, text='Start', command=Start).place(x=280, y=450)
    root.mainloop()


def valdiate_primary_member(flags):
    tempprimary = []

    def myFunc(e):
        return e[3]

    def setprimary(i):
        for j in range(tempprimary1.__len__()):
            if j == i:
                tempprimary.append('Y')
            else:
                tempprimary.append('N')

    tempprimary1=sorted(flags,key=myFunc)

    if tempprimary1[1][3] == tempprimary1[0][3]:
        multipleFlag= True
    else:
        multipleFlag = False

    newtemp = []
    if multipleFlag== True:
        for i in range(flags.__len__()):
            newtemp.append('N')
    else:
        for i in range(len(tempprimary1)):
            if tempprimary1[i][1] == 'Y' and tempprimary1[i][2] == 'Y':
                setprimary(i)
                break
            if tempprimary1[i][1] == 'N' and tempprimary1[i][2] == 'Y':
                setprimary(i)
                break
        for i in range(flags.__len__()):
            for j in range(tempprimary1.__len__()):
                if flags[i][0]==tempprimary1[j][0]:
                    newtemp.append(tempprimary[j])
                    break

    return newtemp
