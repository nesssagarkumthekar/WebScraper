import re
from bs4 import BeautifulSoup
from mechanize import Browser
import WFGSRCHPG as Ws
from configs import WFGGLOBAL as Wg

#import WFGALTSRCH as Wa


"""
The purpose of this Function is to
    1.This Function takes a member from the extracted Data
    2.The Postal code for this member is provided as an input to WellsFargo Web Site to search Advisor details
    3.The search returns links for the Advisors present in an around 25 Mile radius
    4.The links are passed to Search_page Function to check if the Advisor Exists into the link
    5.If the Advisor is present in the link, details are added into the Global Array of the found members
    6.If the Advisor is not present then Advisor Name and Postal Code is added into Not Found Array
     

"""

#member = [['Tyler', 'Naki'], '89410-5207']
#member = [['Matthew', 'Noble'], '43017-2950']
#member = [['Matthew','Lowe'],'75225-6330']
#member = [['Richard','Barry'],'95403-5738']
#member =[['Pearl','Maalouf'],22201-4611]
def process_members(member):

    Fullname = member[0]
    #print(Fullname)
    Pcode = member[1]

    #print(Pcode)


    br = Browser()  # Set Browser


    br.set_handle_robots(False)  # Ignore robots
    br.addheaders = [('User-agent', 'Firefox')]  # Set user Agent
    br.open('https://www.wellsfargo.com/locator/wellsfargoadvisors/search')
###
    br.form = list(br.forms())[0]
    #br.form['chkFNet'] = False
    #br.form['chkBIS'] = False

    br.form['zip5'] = str(Pcode).split('-')[0]
    search_zip = str(Pcode).split('-')[0]
    search_name = Fullname



    br.submit()
    soup = BeautifulSoup(br.response().read(), "lxml")

    found_flag = 'N'

    if soup.find('div',attrs={'id':'alertBox'}) != None:
        pass
    else:
        table = soup.find_all('table', attrs={'class': 'generictext'})
        for td in table[0].find_all('td'):
            try:
                url = td.find('div').find('strong').find('a', href=True).get('href')
                for links in td.find_all('br'):
                    zip = re.sub("(\n)|(\r)|(\t)|(\xa0)|(\n),", "", links.nextSibling)

                    if search_zip in zip:
                        found_flag = Ws.search_page(url, search_name, Pcode)


            except AttributeError:
                pass
            except IndexError:
                pass

            finally:

                if found_flag == 'Y':
                    break


    if found_flag != 'Y':
        url = 'EMPTY'
        found_flag = Ws.search_page(url, search_name, Pcode)
        #print(found_flag)

        if found_flag != 'Y':
            Wg.Fname_not_found.append(search_name[0])
            Wg.Lname_not_found.append(search_name[1])
            Wg.Zip_not_found.append(Pcode)


    br.close()




"""

process_members(member)

print('--------------------')
print(Wg.Group_A)
print(Wg.Name_A)
print(Wg.Link_A)
print(Wg.Url_A)

"""