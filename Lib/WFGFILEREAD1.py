########### Import all the packages needed for the processing ##############
import pandas as pd
#import WFGPRCMEM as Wp
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from configs import WFGGLOBAL as Wg
import traceback
import sys
from Lib import WFGFILEWRT as Ww
import WFGCRAWLER as Wc

"""
The purpose of this Function is 
    1.Read financial advisors from CSV File 
    2.Call the submodules to extract the advisor information
    3.Once all the Data is extracted, Write the details into a CSV output File
"""


def Start_Process(input_file):
    #File = '/Users/P7165881/Desktop/Brodridge/input_file_extracts.xlsx'
    #File = '/Users/P7165881/Desktop/Brodridge/Reps for Web Research Input3.xlsx'
    members=[]

    File = input_file


    try:
        #Open a CSV File and read the Advisor Name and Postal Code
        Excl = pd.read_excel(File)
        df = pd.DataFrame(Excl,columns=Wg.Wf_columns_of_input_file)
        print('Total # records in Excel : ' + str(df.__len__()))

        #Filer the excel data only for Wells Fargo Advisors
        df1 = df[df['mfo_fir_name'].str.contains(Wg.Wf_Filter)]

        line_count = 0

        print( '#of records in Filtered from Excel : -------------> '+ str(df1.__len__()))

        """
        Load all the Advisors as a Members into an Array
        """
        for index, row in df1.iterrows():
            Fname = row['mfo_per_first_name']
            Lname = row['mfo_per_last_name']

            Pcode = row['mfo_ofl_postal_code']
            Fullname=[Fname,Lname]

            #Wg.sleep(Wg.np.random.randint(1, 10))
            #Wg.sleep(Wg.np.random.randint(1, 3))
            #main.process_file(Fullname,Pcode)
            member=[Fullname,Pcode]
            members.append(member)
            line_count = line_count + 1

        """
        Handle if any exception is encountered
        """
    except FileNotFoundError:
        print('Invalid or Empty Input File')
        message = 'Invalid or Empty Input File'

    except UnicodeDecodeError:
        print('File is corrupted or incorrect, Please check the file contents')
        message = 'File is corrupted Or Incorrect,Please check the file contents'

        """
        Print the count of the number of members present in the array
        """
    except ValueError:
        print('One of the column is blank for the row')

    finally:
        End_time = time.strftime('%X %x %Z')
        Wg.Counter_max = members.__len__()




    with ThreadPoolExecutor(max_workers=10) as executor:
        start = time.time()
        #futures = {executor.submit(Wp.process_members,member): member for member in members}
        futures = {executor.submit(Wc.process_members, member): member for member in members}
        for future in as_completed(futures):
            Wg.Counter_global = Wg.Counter_global + 1
            #print(str(counter1))
            url = futures[future]
            #print(url)
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                print(''.join(tb.format_exception_only()))

        end = time.time()
        print("Time Taken: {:.6f}s".format(end - start))
        print('End time of url process is xz : ' + End_time)

    """
    Once the Extracted data is processed, Write the details into a CSV Output file
    """
    Ww.Write_To_Csv()



