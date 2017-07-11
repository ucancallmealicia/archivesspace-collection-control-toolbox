#!/usr/bin/python3

#Super-simple GUI to perform queries against the ArchivesSpace MySQL Database


#to-do -
#column headers, error handling, etc.

#--------------------------------------------------------------MODULES---------------------------------------------------------------

#IMPORT MODULES - not all of the tkinter stuff opened with * thus the multiple imports...
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import scrolledtext as tkst
import json, requests, csv, os, sys, subprocess, time, logging, re
import pymysql

#-----------------------------------------------------GUI FILE/ERROR HANDLING FUNCTIONS--------------------------------------------------

#select directory for output file
def prewritefile():
    directory = filedialog.askdirectory(parent=root)
    txt_name.set(str(directory))
    return directory

#create output file
def writefile(name):
    directoryname = txt_name.get()
    if txt_name.get() == '':
        nodirectory()
        return
    else:
        f = open(directoryname + '/' + name + '_output.csv', 'a', encoding='utf-8', newline='')
        txtfile = directoryname + '/' + name + '_output.csv'
        txt_file.set(str(txtfile))
        return f

#open output file - should work for Windows, OS, or Linux
def openoutput():
    filename = txt_file.get()
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

#opens program error log (update errors that don't stop the program are detailed in the output file)
def openerrorlog():
    filename = log_file.get()
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])

#message box confirming actions, that script is about run
#add start time?
def areyousure():
    result = messagebox.askyesno('Action Chosen', '             Are you sure? \n\n  Click Yes to run query \n\n        Click No to cancel')
    if result == True:
        script_status.set('...Query in progress...')
        script_status.get()
        results = messagebox.showinfo('Query Initialized', '  This may take a few moments \n\n         Press OK to continue')
    if result == False:
        false = messagebox.showinfo('Query Canceled', '       Query Canceled \n\n Press OK to return to menu')
    return result

#exits program
def client_exit():
    exit()

def nodirectory():
    messagebox.showerror('Error!', 'Please choose an output directory')
    script_status.set('Script stopped due to error')
    script_status.get()

def errors():
    messagebox.showerror('Error!', 'Something went wrong. Check error log for details')
    script_status.set('Script stopped due to error')
    script_status.get()
    error_log()

def login_error():
    messagebox.showerror('Error!', 'Please log in to the ArchivesSpace Database')
    script_status.set('Script stopped due to error')
    script_status.get()

def error_log():
    #make sure this works on all systems...add another temp folder for pre-Windows 10?
    if sys.platform == "win32":
        log_file.set('\\Windows\\Temp\\error_log.log')
    else:
        log_file.set('/tmp/error_log.log')
    logging.basicConfig(filename=log_file.get(), level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logging.exception('Error: ')

#script finished message
def script_finished():
#    box = messagebox.showinfo('Done!', 'Script finished. Check outfile for details')
    script_status.set('Query finished! Check outfile for details')
    script_status.get()

def clear_inputs():
    r = messagebox.askyesno('Warning!', '        Press Yes to clear all input values \n\n                   Press No to cancel')
    if r == True:
        login_confirmed.set('')
        txt_name.set('')
        txt_file.set('')
        update_attempts.set('')
        script_status.set('')
        sqlpassword.set('')
        sqlhostname.set('')
        sqlusername.set('')
        sqldbname.set('')
        sqlport.set('')
    else:
        return

def out(r, o):
    update_attempts.set(str(len(r)))
    for row in r:
        writer = csv.writer(o)
        writer.writerows([row])

#-------------------------------------------------------------AS SQL FUNCTIONS-----------------------------------------------------

#add headers to columns?? YESSSSS

def sql_login():
    try:
        connection = pymysql.connect(host=sqlhostname.get(),
                                 user=sqlusername.get(),
                                 password=sqlpassword.get(),
                                 port=int(sqlport.get()),
                                 db = sqldbname.get())
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        if results:
            login_confirmed.set('Login successful!')
            return connection
    except:
        login_confirmed.set('Login failed, try again')
        return None

#do something like, messagebox asking 
def get_archobj_instances():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            d = MyDialog(root, 'ead_id')
            root.wait_window(d.top)
            f = MyDialog(root, 'repo_id')
            root.wait_window(f.top)
            areyousure()
            output = writefile(eadid.get())
            cursor.execute("""
            SELECT resource.ead_id AS EAD_ID
                , resource.identifier AS Resource_ID
                , resource.title AS Collection_Title
                , ao.display_string AS Archival_Object_Title
                , ev2.value AS AO_Level
                , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
                , CONCAT('/repositories/', resource.repo_id, '/archival_objects/', ao.id) AS Archival_Object_URL
                , tc.barcode AS Barcode
                , cp.name AS Container_Type
                , tc.indicator AS Container_Number
                , ev3.value AS Sub_Container_Type
                , sc.indicator_2 AS Sub_Container_Indicator
            from sub_container sc
            left join enumeration_value on enumeration_value.id = sc.type_2_id
            left join top_container_link_rlshp tclr on tclr.sub_container_id = sc.id
            left join top_container tc on tclr.top_container_id = tc.id
            left join top_container_profile_rlshp tcpr on tcpr.top_container_id = tc.id
            left join container_profile cp on cp.id = tcpr.container_profile_id
            left join top_container_housed_at_rlshp tchar on tchar.top_container_id = tc.id
            left join location on location.barcode = tc.barcode
            left join instance on sc.instance_id = instance.id
            left join archival_object ao on instance.archival_object_id = ao.id
            left join resource on ao.root_record_id = resource.id
            left join repository on repository.id = resource.repo_id
            left join enumeration_value ev2 on ev2.id = ao.level_id
            left join enumeration_value ev3 on ev3.id = sc.type_2_id
            WHERE resource.repo_id = """ + repoid.get() + """
            AND resource.ead_id LIKE '%""" + eadid.get() + """%'
            ORDER BY Archival_Object_URL
            """)         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

def get_container_profiles():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            areyousure()
            output = writefile('container_profiles')
            cursor.execute("""
            SELECT cp.name
                , cp.extent_dimension
                , cp.height
                , cp.width
                , cp.depth
                , ev.value as dimension_units
                , CONCAT('/container_profiles/', cp.id) as container_profile_URI
            FROM container_profile cp
            LEFT JOIN enumeration_value ev on ev.id = cp.dimension_units_id""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

#specify repository?
def get_locations():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            areyousure()
            output = writefile('locations')
            cursor.execute("""
	    SELECT l.title
		, l.building
    		, l.floor
    		, l.room
    		, l.area
		, l.coordinate_1_label
    		, l.coordinate_1_indicator
		, l.coordinate_2_label
    		, l.coordinate_2_indicator
    		, l.coordinate_3_label
    		, l.coordinate_3_indicator
    		, CONCAT('/locations/', l.id) as location_URI
   		, CONCAT('/location_profiles', lp.id) as location_profile_URI
	    FROM location l
	    LEFT JOIN location_profile_rlshp lpr on lpr.location_id = l.id
	    LEFT JOIN location_profile lp on lp.id = lpr.location_profile_id""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

def get_top_containers():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            d = MyDialog(root, 'repo_id')
            root.wait_window(d.top)
            areyousure()
            output = writefile('top_containers')
            cursor.execute("""
            SELECT tc.barcode as barcode
                , cp.name as container_profile_name
                , tc.indicator as indicator
                , location.title as location_name
                , CONCAT('/locations/', location.id) as location_uri
                , CONCAT('/container_profiles/', tcpr.container_profile_id) as container_profile_uri
                , CONCAT('/repositories/', tc.repo_id, '/top_containers/', tc.id) as top_container_uri
            FROM top_container tc
            LEFT JOIN top_container_housed_at_rlshp tchr on tchr.top_container_id = tc.id
            LEFT JOIN location on tchr.location_id = location.id
            LEFT JOIN top_container_profile_rlshp tcpr on tcpr.top_container_id = tc.id
            LEFT JOIN container_profile cp on cp.id = tcpr.container_profile_id
            WHERE tc.repo_id = """ + repoid.get() + """
            ORDER BY top_container_uri""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

#added DISTINCT statement bc for some reason duplicates kept showing up in results...
def get_resource_restrictions():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            d = MyDialog(root, 'repo_id')
            root.wait_window(d.top)
            areyousure()
            output = writefile('resource_restrictions')
            cursor.execute("""
            SELECT DISTINCT resource.ead_id AS EAD_ID
        	, resource.identifier AS Identifier
        	, resource.title AS Resource_Title
        	, ev.value AS LEVEL
        	, rr.restriction_note_type AS Restriction_Type
        	, rr.begin AS BEGIN_DATE
        	, rr.end AS END_DATE
                , CAST(note.notes as CHAR (10000) CHARACTER SET UTF8) AS restriction_text
                , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
            FROM rights_restriction rr
            LEFT JOIN resource on resource.id = rr.resource_id
            LEFT JOIN enumeration_value ev on ev.id = resource.level_id
            LEFT JOIN note on resource.id = note.resource_id
            WHERE resource.repo_id = """ + repoid.get() + """
            AND rr.restriction_note_type LIKE '%accessrestrict%'
            AND note.notes LIKE '%accessrestrict%'""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

def get_ao_restrictions():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            d = MyDialog(root, 'repo_id')
            root.wait_window(d.top)
            areyousure()
            output = writefile('archival_object_restrictions')
            cursor.execute("""
            SELECT resource.ead_id AS EAD_ID
        	, resource.identifier AS Identifier
        	, resource.title AS Resource_Title
        	, ev.value AS LEVEL
                , ao.display_string AS Object_Title
        	, rr.restriction_note_type AS Restriction_Type
            	, rr.begin AS BEGIN_DATE
        	, rr.end AS END_DATE
                , CAST(note.notes as CHAR (10000) CHARACTER SET UTF8) AS restriction_text
                , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
                , CONCAT('/repositories/', resource.repo_id, '/archival_objects/', ao.id) AS Archival_Object_URL
            FROM rights_restriction rr
            LEFT JOIN archival_object ao on ao.id = rr.archival_object_id
            LEFT JOIN resource on ao.root_record_id = resource.id
            LEFT JOIN enumeration_value ev on ev.id = ao.level_id
            LEFT JOIN note on ao.id = note.archival_object_id
            WHERE resource.repo_id = """ + repoid.get() + """
            AND rr.restriction_note_type LIKE '%accessrestrict%'
            AND note.notes LIKE '%accessrestrict%'""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

def get_archival_objects():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            d = MyDialog(root, 'ead_id')
            root.wait_window(d.top)
            f = MyDialog(root, 'repo_id')
            root.wait_window(f.top)
            areyousure()
            output = writefile(eadid.get())
            cursor.execute("""
            SELECT resource.ead_id AS EAD_ID
        	, resource.identifier AS Resource_ID
        	, resource.title AS Collection_Title
                , aoj.display_string AS AO10
                , aoi.display_string AS AO09
                , aoh.display_string AS AO08
                , aog.display_string AS AO07
            	, aof.display_string AS AO06
        	, aoe.display_string AS AO05
        	, aod.display_string AS AO04
        	, aoc.display_string AS AO03
                , aob.display_string AS AO02
        	, aoa.display_string AS AO01
        	, ev.value AS AO_Level
        	, CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
        	, CONCAT('/repositories/', resource.repo_id, '/archival_objects/', aoa.id) AS Archival_Object_URL
     	    FROM archival_object aoa
            left join archival_object aob on aob.id = aoa.parent_id
	    left join archival_object aoc on aoc.id = aob.parent_id
	    left join archival_object aod on aod.id = aoc.parent_id
            left join archival_object aoe on aoe.id = aod.parent_id
            left join archival_object aof on aof.id = aoe.parent_id
            left join archival_object aog on aog.id = aof.parent_id
            left join archival_object aoh on aoh.id = aog.parent_id
            left join archival_object aoi on aoi.id = aoh.parent_id
            left join archival_object aoj on aoj.id = aoi.parent_id
            left join resource on aoa.root_record_id = resource.id
            left join enumeration_value ev on ev.id= aoa.level_id
            WHERE resource.repo_id = """ + repoid.get() + """
            AND resource.ead_id LIKE '%""" + eadid.get() + """%'
            Group by aoa.id""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()

def get_location_profiles():
    try:
        connect = sql_login()
        if connect == None:
            login_error()
            return
        else:
            cursor = connect.cursor()
            areyousure()
            output = writefile('location_profiles')
            cursor.execute("""
	    SELECT lp.name
		, lp.depth
	        , lp.width
	        , lp.height
		, ev.value AS dimension_units
		, CONCAT('/location_profiles/', lp.id) AS location_profile_URI
	    FROM location_profile lp
	    LEFT JOIN enumeration_value ev on ev.id = lp.dimension_units_id""")         
            columns = cursor.description
            results = cursor.fetchall()
            out(results, output)
            cursor.close()
            script_finished()
    except Exception:
        errors()
    
#----------------------------------------------------------------GUI SETUP--------------------------------------------------------

#---------------------------------------MAINFRAME, CANVAS, SCROLLBAR, INPUT MENUS-------------------------------------------#

#class to create scrollbar (filched from effbot)
class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

#message input dialogs - modified from stack overflow
class MyDialog():
    def __init__(self, parent, cmd):
        top = self.top = Toplevel(parent)
        if cmd == 'ead_id':
            Label(top, text='Please Enter EAD ID').pack()
            b = Button(top, text='OK', command=self.ead_id)
        elif cmd == 'repo_id':
            Label(top, text='Please Enter Repository ID').pack()
            b = Button(top, text='OK', command=self.repo_id)
        self.e = ttk.Entry(top)
        self.e.pack(padx=7)
        b.pack(pady=7)

    def ead_id(self):
        eadid.set(self.e.get())
        self.top.destroy()

    def repo_id(self):
        repoid.set(self.e.get())
        self.top.destroy()

#keeps the scrollbar even if window is resized
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

#mainframe and canvas, employing scrollbar class
root = Tk()
root.title('ArchivesSpace Collection Control Toolbox TEST GUI - SQL Version')
root.geometry('580x665')

vscrollbar = AutoScrollbar(root)
vscrollbar.grid(row=0, column=1, sticky=N+S)
hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=E+W)

canvas = Canvas(root, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, borderwidth=0)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

vscrollbar.config(command=canvas.yview)
hscrollbar.config(command=canvas.xview)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

mainframe = ttk.Frame(canvas)
#mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.rowconfigure(0, weight=1, minsize=20)
mainframe.columnconfigure(0, weight=1, minsize=20)


#-------------------------------------------------WIDGETS--------------------------------------------------#

#VARIABLE INPUTS
login_confirmed = StringVar()
txt_name = StringVar()
txt_file = StringVar()
update_attempts = StringVar()
log_file = StringVar()
error_dialog = StringVar()
script_status = StringVar()

eadid = StringVar()
repoid = StringVar()
sqlpassword = StringVar()
sqlhostname = StringVar()
sqlusername = StringVar()
sqldbname = StringVar()
sqlport = StringVar()

#------STEP 1A: LOG IN TO THE ARCHIVESSPACE API-------#

#LOGIN HEADER LABEL
ttk.Label(mainframe, text='Step 1: Log in to ArchivesSpace MySQL Database: ', font=('Arial', 13)).grid(column=2, row=1, columnspan=3, sticky=W+E)

#------STEP 1B: LOG IN TO ARCHIVESSPACE DATABASE-------#

#SQL Database Host Name
ttk.Label(mainframe, text='Database Host Name: ', font=('Arial', 11)).grid(column=2, row=3, sticky=W)
username_input = ttk.Entry(mainframe, width=40, textvariable=sqlhostname)
username_input.grid(column=2, row=4, sticky=W)
#SQL Database Name
ttk.Label(mainframe, text='Database Name: ', font=('Arial', 11)).grid(column=3, row=3, sticky=W)
username_input = ttk.Entry(mainframe, width=40, textvariable=sqldbname)
username_input.grid(column=3, row=4, sticky=W)

#SQL Database Username
ttk.Label(mainframe, text='Database Username: ', font=('Arial', 11)).grid(column=2, row=5, sticky=W)
password_input = ttk.Entry(mainframe, width=40, textvariable=sqlusername)
password_input.grid(column=2, row=6, sticky=W)

#SQL Port Name
ttk.Label(mainframe, text='Database Port: ', font=('Arial', 11)).grid(column=3, row=5, sticky=W)
username_input = ttk.Entry(mainframe, width=40, textvariable=sqlport)
username_input.grid(column=3, row=6, sticky=W)

#SQL Database Password
ttk.Label(mainframe, text='Database Password: ', font=('Arial', 11)).grid(column=2, row=7, sticky=W)
password_input = ttk.Entry(mainframe, width=40, textvariable=sqlpassword, show='*')
password_input.grid(column=2, row=8, sticky=W)



#CONNECT BUTTON, LOGIN CONFIRMATION/DENIAL
connectbutton = ttk.Button(mainframe, text='Connect!', command=sql_login).grid(column=3, row=9, sticky=E)
ttk.Label(mainframe, textvariable=login_confirmed, font=('Arial', 11)).grid(column=3, row=8, sticky=E)

#OUTPUT TXT BUTTON AND LABEL INDICATING WHICH DIRECTORY IS OPEN
ttk.Label(mainframe, text='Step 2: Select output directory: ', font=('Arial', 13)).grid(column=2, row=18, sticky=W)
selectfilebutton = ttk.Button(mainframe, text='Select Output Directory', command=prewritefile).grid(column=3, row=18, sticky=E)
ttk.Label(mainframe, text='Directory selected: ', font=('Arial', 11)).grid(column=2, row=19, sticky=W)
ttk.Label(mainframe, textvariable=txt_name, width=50, font=('Arial', 10)).grid(column=2, row=20, columnspan=3, sticky=W)

#-------STEP 4: CHOOSE AN ACTION------#

#CHOOSE AN ACTION HEADER
ttk.Label(mainframe, text='Step 3: Choose a query: \n', font=('Arial', 13)).grid(column=2, row=21, sticky=W)

#ACTIONS TO CHOOSE FROM BUTTONS - columns 22-26

#SQL Actions

getaos = ttk.Button(mainframe, text='Get archival objects', width=40, command=get_archival_objects).grid(column=2, row=22, sticky=W)
getlocations = ttk.Button(mainframe, text='Get locations', width=40, command=get_locations).grid(column=3, row=22, sticky=W)
gettcs = ttk.Button(mainframe, text='Get top containers', width=40, command=get_top_containers).grid(column=2, row=23, sticky=W)
getcps = ttk.Button(mainframe, text='Get container profiles', width=40, command=get_container_profiles).grid(column=3, row=23, sticky=W)
getresourcerestricts = ttk.Button(mainframe, text='Get resource-level restrictions', width=40, command=get_resource_restrictions).grid(column=2, row=24, sticky=W)
getaorestricts = ttk.Button(mainframe, text='Get archival object-level restrictions', width=40, command=get_ao_restrictions).grid(column=3, row=24, sticky=W)
getaos = ttk.Button(mainframe, text='Get container list', width=40, command=get_archobj_instances).grid(column=2, row=25, sticky=W)
getlps = ttk.Button(mainframe, text='Get location profiles', width=40, command=get_location_profiles).grid(column=3, row=25, sticky=W)
#-------STEP 5: REVIEW OUTPUT------#

#REVIEW OUTPUT HEADER
ttk.Label(mainframe, text='\nStep 4: Review output: ', font=('Arial', 13)).grid(column=2, row=27, sticky=W)
ttk.Label(mainframe, textvariable=script_status, font=('Arial', 11)).grid(column=3, row=27, sticky=E)

#VIEW OUTPUT FILE BUTTON AND LABEL INDICATING WHICH FILE IS OPEN
selectfilebutton = ttk.Button(mainframe, text='View Output File', command=openoutput).grid(column=3, row=28, sticky=E)
ttk.Label(mainframe, text='File selected: ', font=('Arial', 11)).grid(column=2, row=28, sticky=W)
ttk.Label(mainframe, textvariable=txt_file, width=70, font=('Arial', 10)).grid(column=2, row=29, columnspan=3, sticky=W)

#VIEW ERROR LOG BUTTON
errorlogbutton = ttk.Button(mainframe, text='View Error Log', command=openerrorlog).grid(column=3, row=30, sticky=E)
clearinputs = ttk.Button(mainframe, text='Clear All Inputs', command=clear_inputs).grid(column=3, row=31, sticky=S+E)

#RECORD UPDATE SUMMARY LABELS
ttk.Label(mainframe, text='Rows returned: ', width=20, font=('Arial', 11)).grid(column=2, row=30, sticky=W)
ttk.Label(mainframe, textvariable=update_attempts, width=20, font=('Arial', 10)).grid(column=3, row=30, sticky=W)

#----------------------------------------MORE MAINFRAME AND CANVAS STUFF-------------------------------------#

#FINISH CREATING CANVAS
canvas.create_window(0, 0, anchor=NW, window=mainframe)
mainframe.update_idletasks()
canvas.config(scrollregion=canvas.bbox('all'))

#SET SPACING BETWEEN WIDGETS
for child in mainframe.winfo_children():
    child.grid_configure(padx=3, pady=3)

#CREATE EXIT MENU AT TOP OF WINDOW  
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Exit', command=client_exit)
menubar.add_cascade(label='File', menu=filemenu)
root.config(menu=menubar)

#EXECUTE RESIZING FUNCTION UPON RESIZING
mainframe.bind('<Configure>', lambda event, canvas=canvas: onFrameConfigure(canvas))

#EXECUTE ARCHIVESSPACE LOGIN SCRIPT UPON PRESSING ENTER
root.bind('<Return>', sql_login)

#LAST BIT OF GUI INITIALIZATION
root.mainloop()

#TO-DO, QUESTIONS:

#disable user entry into text box? Not sure if this matters
#additional error handling if necessary
#general script cleanup
#add comments as necessary
#Write README - create troubleshooting doc (to consult when the something went wrong message comes up - common errors)
#color?
#bind trackpad, allow for selection of text (selection works on windows)

#add OPEN README button?

#redo styling for Windows

#check what happens when spreadsheet is missing data....and when a crappy barcode is entered...
#change value of update successes to O if script does not run all the way through...

#restructure GUI setup into classes

#Package this as a standalone application with a setup file so that the IDLE window doesn't open when it's run
    #can do for MacOS and Windows

#TEST TEST TEST TEST......
#most testing done on PC so far - need more Mac testing
#Display is different on Macs and PCs, make sure it looks right on both

#need to indicate that requests needs to be installed for this to work...or that Anaconda should be installed; could just do a setup.py file also to install requests

#future possibilities:
#add query for getting top container and archobj info using pymysql? But would need to add DB login stuff too then...and add pymysql to setup.py
#could use this GUI for reporting too...or a different one, like a DB GUI?
#instead of a grid could I place in specific locations? Grid is a little rigid
#why can't you just do uploads like this in AS?
