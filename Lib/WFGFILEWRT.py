from configs import WFGGLOBAL as Wg
import pandas as pd
import time
import datetime


"""
The purpose of this function is to
    1.Create a Panda Data Frame for all the extracted details
    2.Write the Advisors into an Output file for whom the details are found
    3.Write the Advisors into an Error Output file for whom the details are not found
"""
def Write_To_Csv():

    try:
        df = pd.DataFrame({'Name': Wg.Name_A, 'Designation': Wg.Des_A, 'Phone': Wg.Phone_A, 'Email': Wg.Email_A,
                           'Primary Person': Wg.Primary_A, 'Group': Wg.Group_A, 'Url': Wg.Url_A,
                           'Linked In Url': Wg.Link_A})

        print('Folder Location is :  '+ Wg.Folder_loc)
        df=df.drop_duplicates()
        #df.to_csv('/Users/P7165881/Desktop/Brodridge/WellsFargo/WFARG_Found_012.csv', index=False, encoding='utf-8')

        Wg.File_output1 = 'WFARG_Found_' + str(datetime.datetime.now()).replace(':','.') + '.csv'
        df.to_csv(Wg.Folder_loc + '/' + Wg.File_output1, index=False, encoding='utf-8')
        df = pd.DataFrame({'First Name': Wg.Fname_not_found, 'Last Name': Wg.Lname_not_found, 'Zip': Wg.Zip_not_found})


        #df.to_csv('/Users/P7165881/Desktop/Brodridge/WellsFargo/WFARG_Error_012.csv', index=False, encoding='utf-8')
        Wg.File_output2 = 'WFARG_Error_' + str(datetime.datetime.now()).replace(':','.') + '.csv'
        df.to_csv(Wg.Folder_loc + '/' + Wg.File_output2, index=False, encoding='utf-8')


    except ValueError:
        print('Name :')
        print(Wg.Name_A.__len__())
        print('Designation :')
        print(Wg.Des_A.__len__())
        print('Phone :')
        print(Wg.Phone_A.__len__())
        print('Email :')
        print(Wg.Email_A.__len__())
        print('Primary_Sw :')
        print(Wg.Primary_A.__len__())
        print('Group :')
        print(Wg.Group_A.__len__())
        print('Url :')
        print(Wg.Url_A.__len__())
        print(Wg.Name_A)
        print(Wg.Group_A)
        df = pd.DataFrame({'Url': Wg.Url_A, 'Name': Wg.Name_A})
        df.to_csv('D:/WebScraper/Logs/WFGERR0011.csv', index=False, encoding='utf-8')


    finally:
        print('Process Completed Successfully')
        End_time = time.strftime('%X %x %Z')
        print('Final End time is : ' + End_time)