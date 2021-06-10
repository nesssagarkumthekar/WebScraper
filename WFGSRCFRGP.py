import requests
from bs4 import BeautifulSoup
from configs import WFGGLOBAL as Wg

"""
The purpose of this Function is to
    1.This Function takes a URL as an input from the Search results  group links
    2.The Group URL Data is scrapped and stored into an Array using search group function.
     This Array is used again if the Advisor from the same group is passed as an input.
     This saves additional Hits to the same URL
    3.This function also returns a flag if the Advisor is present in the group
"""

def Search_for_Group(Grpurl,search_name):

    resp1 = requests.get(Grpurl)

    if resp1.ok:
        pass
    else:
        print('bad search in group '+ Grpurl)

    soup1 = BeautifulSoup(resp1.text,'lxml')
    found = 'N'

    for member1 in soup1.find('div',attrs={'id':'groupFAs'}).find('ul').find_all('li'):
        names1 = member1.find('a', href=True).text.strip()

        Wg.All_members.append(names1)

        if search_name[0].upper() in names1 and search_name[1].upper() in names1:

            found = 'Y'

        resp1.close()
        requests.session().close()

    return found










