import requests
from bs4 import BeautifulSoup
import re
from configs import WFGGLOBAL as Wg

"""
The purpose of this Function is to
    1.If the Advisor is found in the Search result Link then his/her URL from the Search Result Link is passed
     as an input to this Function
    2.This function extracts the Advisor information and keeps into a Global Arrays

"""

#async def search_member(Memurl):
def search_member(Memurl):
    resp = requests.get(Memurl)

    #print('member found in member search ' + Memurl)

    if resp.ok:
        if resp.url != Memurl:
           return 'N'
        #pass
    else:
        print('error from search member')

    soup = BeautifulSoup(resp.text,"lxml")

    try:
        name = soup.find('div',attrs:={'id':'nameTitle'}).find('h1').text.strip()
    except AttributeError:
        name = soup.find('div', attrs := {'id': 'nameTitle'}).find('script').contents[0].split('<h1>')[1].split('</h1>')[0]

    print(name)
    if ',' in name:
        name = name.split(',')[0]

    Wg.Name_A.append(name)


    try:
        designation = soup.find('div',attrs:={'id':'nameTitle'}).find_all('h2')[1].text.strip()
    except IndexError:
        try:
            designation = soup.find('div', attrs := {'id': 'nameTitle'}).find_all('h2')[0].text.strip()
        except AttributeError:
            designation = ' '

    if '-' in designation:
        designation = designation.split('-')[0]

    Wg.Des_A.append(designation)

    if designation.strip().upper() in Wg.Titles:
        Wg.Primary_A.append('Y')
    else:
        Wg.Primary_A.append('N')

    Wg.Link_A.append('')

    Address_tag = soup.find('div',attrs:={'id': 'address'})

    ph2=''
    for lines in Address_tag.select('strong'):

        if 'Phone' in lines.text:
            ph=lines.nextSibling.strip()
            ph1 = re.sub("(\n)|(\r)|(\t)|(\xa0)|(\n),", "", ph)
            ph2 = ph1.replace('|', ',').replace('                                                ', '').replace(
                '               ', '')


    if ph2 != '':
        Wg.Phone_A.append(ph2)
    else:
        Wg.Phone_A.append(' ')

    try:
        email = Address_tag.find('a',href=True).get('href').split(':')[1]
    except AttributeError:
        email = ''

    Wg.Email_A.append(email)

    return 'Y'




