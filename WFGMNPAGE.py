import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from configs import WFGGLOBAL as Wg
from Lib import WFGFILEREAD1 as Wr1
import time
import os


"""
The purpose of this module is to
    1.Create a GUI (Graphical User Interface) for Selection of Input and Output File
    2.To provide Error information if any Error is encountered
    3.Provide the status of the progress
"""

root = Tk()
root.geometry('1000x600')
root.resizable(0,0)
style=Style()
style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'red')

root.title('WellsFargo Advisor Extractor')
Label(root, text ='Welcome to WellsFargo Advisor Extraction process', font = 'arial 20')
display = Entry(root)


Text = StringVar()
Output_Folder_Loc = StringVar()
private_key = StringVar()
mode = StringVar()
Result = StringVar()
exc_var = StringVar()
Complete_Msg_Part1 = StringVar()
Complete_Msg_Part2 = StringVar()
Ouptut_File_1=StringVar()
Output_file_2=StringVar()
Choose_Folder_msg =StringVar()
location = ''
display = Entry(root)
File_success = StringVar()
Notify = StringVar()
#pb1= tkinter.ttk.Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
#pb1.pack(expand=True)
#pb1.place(x=290, y=500)
current_system_pid = os.getpid()


Notify.set("\n"
           "\nDefault location for Storing the results CSV File is C:/Users/P7165881/Desktop/Brodridge/        "
           "\n")
Choose_Folder_msg.set("Optional: Select a Location to Store Output Files :")

Output_Folder_Loc.set("Default as above")

def Exit():
    #current_system_pid = os.getpid()
    #psutil.Process(current_system_pid).terminate()
    #ThisSystem = ThisSystem.terminate()
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
        File_success.set( Wg.File_Input.name + ' File opened Successfully')
        Text.set(Wg.File_Input.name)
    except AttributeError:
        File_success.set('No File selected, Please select a File')
        Text.set(" ")

    Label(root, font='arial 12', textvariable=File_success).place(x=60, y=280)


def Select_A_Folder():
    location = filedialog.askdirectory(initialdir="C:/Users/P7165881/Desktop/Brodridge/")
    print('this is the location ------> ' + location)
    Output_Folder_Loc.set(location)

def Start():
    Base_loc = 'C:/Users/P7165881/Desktop/Brodridge/bkp'
    start_time = time.strftime('%X %x %Z')
    print('Start Time time is : ' + start_time)

    print(location)

    if location!='':
       Wg.Folder_loc=location
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
            Label(root, font='Calibri 12 bold', textvariable= Ouptut_File_1).place(x=120, y=340)
            Label(root, font='Calibri 12 bold', textvariable= Output_file_2 ).place(x=120, y=360)
            Label(root, font='Calibri 12 ', textvariable=Complete_Msg_Part2).place(x=290, y=380)
            #vars = dir(Wg)
            #for var in vars:
                #del var
        except PermissionError:
            Wg.message='Permission to write into a file is denied. ' \
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
"""
def step():
    #print(range1)
    print('started step')
    for i in range(5):
        root.update_idletasks()
        pb1['value'] += 20

        time.sleep(1)
"""





Label(root, font= 'arial 12', text='Location of Input file containing Members').place(x= 60,y=60)

Entry(root, font = 'arial 10', textvariable = Text,width =50).place(x=390, y = 60)

btn1= Button(root,text ='Browse' ,command = Browse).place(x=790, y = 60)
btn_help= Button(root,text ='HELP' ,command = Browse).place(x=880, y = 60)
lable1 = tkinter.ttk.Label(root, font = 'Calibri 12', textvariable =Notify,background="light green" ).place(x=60, y = 100)

tkinter.ttk.Label(select=lable1).pack(fill= tkinter.X, pady=10)

lable2 = tkinter.ttk.Label(root, font = 'Calibri 12', textvariable =Choose_Folder_msg).place(x=60, y = 200)
Entry(root, font = 'arial 10', textvariable = Output_Folder_Loc,width =50).place(x=390, y = 200)
btn_help= Button(root,text ='Folder' ,command = Select_A_Folder).place(x=880, y = 200)


btn2 = Button(root,text ='RESET' ,command = Reset).place(x=80, y = 450)
btn3 = Button(root,text ='EXIT' ,style = 'W.TButton',command = Exit).place(x=180, y = 450)
btn4 = Button(root,text ='Start' ,command = Start).place(x=280, y = 450)


#root.mainloop()

#filedialog.askdirectory('/')