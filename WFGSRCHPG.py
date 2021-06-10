import  WFGSRCHMB as Wb
import requests
from bs4 import BeautifulSoup
from configs import WFGGLOBAL as Wg
import WFGSRCFRGP as Wf

"""
The purpose of this Function is to
    1.This Function takes a URL as an input from the Search results from the WellsFargo website search results
    2.The URL Data is scrapped to check if the member is present in the URL
    3.The Groups present in the URL and its members are captured and stored into an Array using search group function.
     This Array is used again if the Advisor from the same group is passed as an input.
     This saves additional Hits to the same URL
    3.If the mach on the Member name is found then the Search Member function is called to extract the Advisor details
"""

grp_found = 'N'
gname1= ''

def search_page(url,search_name,Pcode):

    #print(Pcode)

    if url != 'EMPTY':
        group_exists = 'N'
        grp_found ='N'
        resp = requests.get(url)


        if resp.ok:
            pass
        else:
            print('error occurred')

        soup = BeautifulSoup(resp.text, "lxml")

        grp_name = ' '

        if Wg.Group_and_Member_Dict.__len__() > 0:

            for x,y in Wg.Group_and_Member_Dict.items():

                mem_name = search_name[0].upper() +' ' + search_name[1].upper()


                if y.count(mem_name) > 0:

                    if y.count(mem_name)==1 :
                        grp_name = x
                    else:
                        grp_name = x + ',' + grp_name

                    group_exists ='Y'

        if soup.find('div', attrs={'id': 'ourTeams'}) != None and group_exists != 'Y':

            for groups in soup.find('div', attrs={'id': 'ourTeams'}).find('ul').find_all('li'):
                grp_url = groups.find('a', href=True).get('href')
                Wg.All_groups.append(groups.find('a', href=True).text.strip())

                Wg.All_members = []
                grp_found = Wf.Search_for_Group(grp_url, search_name)
                gname = groups.find('a', href=True).text.strip()
                #print('group found  ' + grp_found)


                if 'of Wells Fargo Advisors' in gname:
                    grp_name = gname.split('of Wells Fargo Advisors')[0]
                else:
                    grp_name = gname

                if grp_found == 'Y':
                    gname1 = grp_name

                Wg.Group_and_Member_Dict[grp_name] = Wg.All_members
                #print(grp_name)
                #print(Wg.All_members)



        counter = 0
        for members in soup.find('div',attrs={'id':'ourFAs'}).find('ul').find_all('li'):
            Memurl = members.find('a',href=True).get('href')
            names  = members.find('a',href=True).text.strip()
            names.capitalize()
            counter = counter + 1


            if (search_name[0].upper() in names and search_name[1].upper() in names) or \
                    (search_name[1].upper() in names and search_name[0][0:3].upper() in names) :

                Wb.search_member(Memurl)
                Wg.Url_A.append(Memurl)
                if grp_found =='Y':
                    Wg.Group_A.append(gname1)
                elif group_exists =='Y':
                    Wg.Group_A.append(grp_name)
                else:
                    Wg.Group_A.append('')

                return 'Y'

    else:
        Base_Url = 'https://home.wellsfargoadvisors.com/'
        Fin_Url = Base_Url + search_name[0] + '.' + search_name[1]
        #print('come inside this ')

        flag=Wb.search_member(Fin_Url)

        if flag != 'Y':
            mem_found ='N'
        else:
            mem_found = 'Y'
            Wg.Url_A.append(Fin_Url)
            Wg.Group_A.append('')

        return mem_found






