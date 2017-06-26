#!/usr/bin/python3

#Super-simple GUI to perform collection control functions via the ArchivesSpace API

#--------------------------------------------------------------------------------------------------------------------------------------------
#TO-DO, QUESTIONS:

#disable user entry into text box? Not sure if this matters
#additional error handling if necessary
#general script cleanup
#add comments as necessary
#add timer - would really like a '...script running...' message but it doesn't work how I want it to - shows up after it finishes...
#Write README - create troubleshooting doc (to consult when the something went wrong message comes up - common errors)
#color?
#bind trackpad, allow for selection of text

#error handling for when wrong spreadsheet is chosen/wrong update button pressed

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


#--------------------------------------------------------------MODULES---------------------------------------------------------------

#IMPORT MODULES - not all of the tkinter stuff opened with * thus the multiple imports...
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import scrolledtext as tkst
import json, requests, csv, os, sys, subprocess, time, logging, re

#-----------------------------------------------------GUI FILE/ERROR HANDLING FUNCTIONS--------------------------------------------------

#select directory for output file
def prewritefile():
    directory = filedialog.askdirectory(parent=root)
    txt_name.set(str(directory))
    return directory

#create output file
def writefile():
    directoryname = txt_name.get()
    if txt_name.get() == '':
        error_dialog.set('No directory chosen')
        messagebox.showinfo('Error!', error_dialog.get())
        return
    else:
        f = open(directoryname + '/output.txt', 'a')
        txtfile = directoryname + '/output.txt'
        txt_file.set(str(txtfile))
        return f

#read output file
def readfile():
    filename = txt_file.get()
    file = open(filename, 'r', encoding='UTF8')
    return file.read()

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

#enables writing log into text box
def writetolog():
    text = readfile()
    return text

#gets CSV file from window
def opencsv():
    filename = filedialog.askopenfilename(parent=root)
    filename_input.set(str(filename))
    return filename

#opens CSV
def csvopen():
    filename = filename_input.get()
    file = open(filename, 'r', encoding='UTF8')
    csvin = csv.reader(file)
    next(csvin, None)
    return csvin    

#message box confirming actions, that script is about run
def areyousure():
    result = messagebox.askyesno('Action Chosen', '             Are you sure? \n\n  Click Yes to make updates \n        Click No to cancel')
    if result == True:
        results = messagebox.showinfo('Updates Initialized', 'This may take a few moments \n\n     Press OK to continue')
    if result == False:
        false = messagebox.showinfo('Updates Canceled', '       Updates Canceled \n\n Press OK to return to menu')
    return result

def csverror():
    error_dialog.set('Invalid CSV')
    messagebox.showinfo('Error!', error_dialog.get())               

#message box if an error happens with the update, logs error to file
def errors():
    errormessage = messagebox.showerror('Error!', 'Something went wrong. Check error log for details')
    #make sure this works on all systems...add another temp folder for pre-Windows 10?
    if sys.platform == "win32":
        log_file.set('\\Windows\\Temp\\error_log.log')
    else:
        log_file.set('/tmp/error_log.log')
    logging.basicConfig(filename=log_file.get(), level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logging.exception('Error: ')

def script_finished():
    box = messagebox.showinfo('Done!', 'Script finished. Check outfile for details')

#exits program
def client_exit():
    exit()

def outfileprocess(txtfile, jsonname):
    for key, value in jsonname.items():
        if key == 'status':
            txtfile.write('%s:%s\n' % (key, value))
            #Allows for modification of the counters in the AS API functions; globvar not ideal but works for now
            global x
            x += 1
        if key == 'uri':
            txtfile.write('%s:%s\n' % (key, value) + '\n')
        if key == 'error':
            txtfile.write('%s:%s\n' % (key, value) + '\n')
    updates_success.set(x)

def timer(start):
    elapsedTime = time.time() - start
    m, s = divmod(elapsedTime, 60)
    h, m = divmod(m, 60)
    elapsed_time.set('%d:%02d:%02d' % (h, m, s))

def wrongcsv():
    error_dialog.set('Invalid CSV')
    messagebox.showinfo('Error!', error_dialog.get())

def spreadsheet_error():
    error_dialog.set('Something went wrong. Please check spreadsheet for errors')
    messagebox.showinfo('Error!', error_dialog.get())

#--------------------------------------------------------AS API FUNCTIONS---------------------------------------------------------

#something to think about - do I want a class APIUpdates, with members being these functions?

#logs in to ArchivesSpace API
def asloginprocess(event=None):
    try:
        #basic/imperfect check for improperly formatted URLs
        urlcheck = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        #if URL field is empty; missing field error checks may be obsolete now but I'm leaving it in because the URL checks may not be perfect
        if api_address.get() == '':
            login_confirmed.set('Missing value, try again')
        #empty username field
        if username_entry.get() == '':
            login_confirmed.set('Missing value, try again')
        #empty password field
        if password_entry.get() == '':
            login_confirmed.set('Missing value, try again')
        #uses reg ex above to check formulation of URL; may not be perfect but anything it misses gets caught later 
        if not re.match(urlcheck, api_address.get()):
            login_confirmed.set('Improperly formatted URL, try again')
        else:
            api_url = api_address.get()
            username = username_entry.get()
            password = password_entry.get()
            auth = requests.post(api_url+'/users/'+username+'/login?password='+password).json()
            if 'error' in auth.keys():
                login_confirmed.set('Login failed, try again')
            elif 'session' in auth.keys():
                session = auth["session"]
                headers = {'X-ArchivesSpace-Session':session}
                login_confirmed.set('Login successful!')
                authenticate.set(headers)
                return headers
    #this captures a URL that is valid but not correct, plus any other errors
    except Exception:
        login_confirmed.set('Error, check login info and try again')

#gets headers without logging in to API again - a bit of a hack but it works for now
def head():
    h = authenticate.get()
    accept_json = h.replace("'", "\"")
    heads = json.loads(accept_json)
    return heads

#add container profiles to AS
def containerprofiles():
    try:
        go = areyousure()
        if go == True:
            starttime = time.time()
            heady = head()
            csvin = csvopen()
            txtfile = writefile()
            #variable to hold count of update attempts
            i = 0
            #variable to hold count of objects successfully updated
            global x
            x = 0
            for row in csvin:
                name = row[0]
                extent_dimension = row[1]
                height = row[2]
                width = row[3]
                depth = row[4]
                dimension_units = row[5]
                new_container_profile = {'jsonmodel_type': 'container_profile', 'name': name,
                                         'extent_dimension': extent_dimension, 'height': height,
                                         'width': width, 'depth': depth, 'dimension_units': dimension_units}
                container_profile_data = json.dumps(new_container_profile)
                create_profile = requests.post(api_address.get() + '/container_profiles', headers=headers.get(), data=container_profile_data).json()
                writeoutfile = outfileprocess(txtfile, create_profile)
                i = i + 1
            update_attempts.set(str(i))
            txtfile.write('\n' + 'Total update attempts: ' + str(i) + '\n')
            txtfile.write('Records updated successfully: ' + str(x) + '\n')
            timer(starttime)            
            txtfile.close()
            write = writetolog()
            printoutput.insert(INSERT, write)
            done = script_finished()
        else:
            return
    #if anything goes wrong above the error script is initialized
    except Exception:
        errormessage = errors()
        update_attempts.set(str(i))
        updates_success.set(str(x))
        write = writetolog()
        printoutput.insert(INSERT, write)

#add locations to AS    
def locations():
    go = areyousure()
    #if user selects OK script will continue
    if go == True:
        starttime = time.time()
        heady = head()
        csvin = csvopen()
        txtfile = writefile()
        #If directory is selected script will continue
        if txtfile != None:
            #variable to hold count of update attempts
            i = 0
            #global variable to hold count of objects successfully updated; find better way?
            global x
            x = 0
            try:
                for row in csvin:
                    if len(row) == 8:
                        building = row[0]
                        room = row[1]
                        coordinate_1_label = row[2]
                        coordinate_1_indicator = row[3]
                        coordinate_2_label = row[4]
                        coordinate_2_indicator = row[5]
                        coordinate_3_label = row[6]
                        coordinate_3_indicator = row[7]                                       
                        new_location = {'jsonmodel_type': 'location', 'building': building,
                                                 'room': room, 'coordinate_1_label': coordinate_1_label,
                                                 'coordinate_1_indicator': coordinate_1_indicator,
                                                 'coordinate_2_label': coordinate_2_label,
                                                 'coordinate_2_indicator': coordinate_2_indicator,
                                                 'coordinate_3_label': coordinate_3_label,
                                                 'coordinate_3_indicator': coordinate_3_indicator}
                        location_data = json.dumps(new_location)
                        create_location = requests.post(api_address.get() + '/locations', headers=heady, data=location_data).json()
                        writeoutfile = outfileprocess(txtfile, create_location)
                        i = i + 1
                    else:
                        wrongcsv()
                        return
            except:
                    errors()
                    return
            #do I need something here as well???
            update_attempts.set(str(i))
            txtfile.write('\n' + 'Total update attempts: ' + str(i) + '\n')
            txtfile.write('Records updated successfully: ' + str(x) + '\n')
            timer(starttime)
            txtfile.close()
            write = writetolog()
            printoutput.insert(INSERT, write)
            done = script_finished()
        #if no directory is selected a pop-up message will appear and function will terminate
        else:
            return
    #if user selects Cancel a pop-up message will appear and function will terminate
    else:
        return

#add top containers to AS
def topcontainers():
    try:
        go = areyousure()
        if go == True:
            starttime = time.time()
            heady = head()
            csvin = csvopen()
            txtfile = writefile()
            #variable to hold count of update attempts
            i = 0
            #variable to hold count of objects successfully updated
            global x
            x = 0
            for row in csvin:
                barcode = row[0]
                indicator = row[1]
                container_profile_uri = row[2]
                locations = row[3]
                start_date = row[4]
                if len(barcode) == 14:
                    create_tc = {'barcode': barcode, 'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                                 'container_locations': [{'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': start_date,
                                                          'ref': locations}],
                                 'jsonmodel_type': 'top_container', 'repository': {'ref': '/repositories/12'}}
                else:
                    create_tc = {'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                                 'container_locations': [{'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': start_date,
                                                          'ref': locations}],
                                 'jsonmodel_type': 'top_container', 'repository': {'ref': '/repositories/12'}}
                tcdata = json.dumps(create_tc)
                tcupdate = requests.post(api_address.get() + '/repositories/12/top_containers', headers=headers.get(), data=tcdata).json()
                writeoutfile = outfileprocess(txtfile, tcupdate)
                i = i + 1
            #add count of total update attempts to log file
            update_attempts.set(str(i))
            txtfile.write('\n' + 'Total update attempts: ' + str(i) + '\n')
            txtfile.write('Records updated successfully: ' + str(x) + '\n')
            timer(starttime)
            txtfile.close()
            write = writetolog()
            printoutput.insert(INSERT, write)
            done = script_finished()
        else:
            return
    except Exception:
        errormessage = errors()
        update_attempts.set(str(0))
        updates_success.set(str(0))
        write = writetolog()
        printoutput.insert(INSERT, write)

#add restrictions to AS
def restrictions():
    go = areyousure()
    #if user selects OK script will continue
    if go == True:
        starttime = time.time()
        heady = head()
        csvin = csvopen()
        txtfile = writefile()
        #If an output directory is selected script will continue
        if txtfile != None:
            #variable to hold count of update attempts
            i = 0
            #global variable to hold count of objects successfully updated; find better way?
            global x
            x = 0
            try:
                for row in csvin:
                    if len(row) == 5:
                        i = i + 1
                        archival_object_URI = row[0]
                        restriction_type = row[1]
                        restriction_text = row[2]
                        begin_date = row[3]
                        end_date = row[4]
                        #gets resource to edit
                        ao_json = requests.get(api_address.get() + archival_object_URI, headers=heady).json()
                        new_restriction = {'jsonmodel_type': 'note_multipart',
                                            'publish': True,
                                            'rights_restriction': {'begin': begin_date, 'end': end_date, 'local_access_restriction_type': [restriction_type]},
                                            'subnotes': [{'content': restriction_text,
                                                  'jsonmodel_type': 'note_text',
                                                  'publish': True}],
                                            'type': 'accessrestrict'}
                        #append restriction note to resource, form into JSON, and post to AS; maybe add if notes not in....
                        if 'notes' not in ao_json.keys():
                            #add something like 'invalid resource'...
                            spreadsheet_error()
                            #change so two error messages don't show up...
                            errors()
                            #why doesn't the [notes] error message show up anymore?? Just HTTP stuff...check this later...and fix
                            continue
                        else:
                            ao_json['notes'].append(new_restriction)
                            ao_data = json.dumps(ao_json)
                            ao_update = requests.post(api_address.get() + archival_object_URI, headers=heady, data=ao_data).json()
                            writeoutfile = outfileprocess(txtfile, ao_update)
                    else:
                        wrongcsv()
                        return
            except:
                    errors()
                    return
            update_attempts.set(str(i))
            txtfile.write('\n' + 'Total update attempts: ' + str(i) + '\n')
            txtfile.write('Records updated successfully: ' + str(x) + '\n')
            timer(starttime)
            txtfile.close()
            write = writetolog()
            printoutput.insert(INSERT, write)
            done = script_finished()
        #if no directory is selected a pop-up message will appear and function will terminate
        else:
            return
    #if user selects Cancel a pop-up message will appear and function will terminate
    else:
        return

#link top containers to archival objects
def instances():
    try:
        starttime = time.time()
        go = areyousure()
        csvin = csvopen()
        txtfile = writefile()
        #variable to hold count of update attempts
        i = 0
        #variable to hold count of objects successfully updated
        x = 0
        for row in csvin:
            archival_object_uri = row[0]
            top_container_uri = row[1]
            barcode = row[2]
            indicator = row[3]
            archival_object_json = requests.get(api_address.get() + archival_object_uri, headers=headers).json()
            new_instance = {"container": {"barcode_1": barcode, "indicator_1": indicator, "type_1": "box"}, 
                                "instance_type": "mixed_materials", "jsonmodel_type": "instance", "sub_container": {"jsonmodel_type": "sub_container", 
                                "top_container": {"ref": top_container_uri}}}
            archival_object_json["instances"].append(new_instance)
            archival_object_data = json.dumps(archival_object_json)
            headers = asloginprocess()
            archival_object_update = requests.post(api_address.get() +archival_object_uri, headers=headers, data=archival_object_data).json()
            writeoutfile = outfileprocess(txtfile, archival_object_update, x)
            i = i + 1
        #add count of total update attempts to log file
        txtfile.write('\n' + 'Total update attempts: ' + str(i) + '\n')
        #add count of successful updates to log file
        elapsedTime = time.time() - startTime
        m, s = divmod(elapsedTime, 60)
        h, m = divmod(m, 60)
        elapsed_time.set('%d:%02d:%02d' % (h, m, s))
        update_attempts.set(str(i))
        counterval(writeoutfile)
        txtfile.write('Records updated successfully: ' + updates_success.get() + '\n')
        txtfile.close()
        write = writetolog()
        printoutput.insert(INSERT, write)
        done = script_finished()
    except Exception:
        errormessage = errors()
        update_attempts.set(str(i))
        counterval(writeoutfile)
        write = writetolog()
        printoutput.insert(INSERT, write)

#----------------------------------------------------------------GUI SETUP--------------------------------------------------------

#---------------------------------------MAINFRAME, CANVAS, SCROLLBAR-------------------------------------------#

#class to create scrollbar (from effbot)
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
#Need to create more classes eventually, but this works for now

#keeps the scrollbar even if window is resized
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

#mainframe and canvas, employing scrollbar class (from effbot)
root = Tk()
root.title('ArchivesSpace Collection Control Toolbox TEST GUI')
root.geometry('655x875')

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
authenticate = StringVar()
api_address = StringVar()
username_entry = StringVar()
password_entry = StringVar()
login_confirmed = StringVar()
filename_input = StringVar()
txt_name = StringVar()
txt_file = StringVar()
update_attempts = StringVar()
updates_success = StringVar()
elapsed_time = StringVar()
log_file = StringVar()
error_dialog = StringVar()

#------STEP 1: LOG IN TO THE ARCHIVESSPACE API-------#

#LOGIN HEADER LABEL
ttk.Label(mainframe, text='Step 1: Log in to the ArchivesSpace API: ', font=('Arial', 16)).grid(column=2, row=1, sticky=W)

#AS API URL
ttk.Label(mainframe, text='ArchivesSpace API URL: ', font=('Arial', 13)).grid(column=2, row=2, sticky=W)
api_entry = ttk.Entry(mainframe, width=30, textvariable=api_address)
api_entry.grid(column=2, row=3, sticky=(W, E))
#AS Username
ttk.Label(mainframe, text='ArchivesSpace Username: ', font=('Arial', 13)).grid(column=2, row=4, sticky=W)
username_input = ttk.Entry(mainframe, width=30, textvariable=username_entry)
username_input.grid(column=2, row=5, sticky=(W, E))
#AS Password
ttk.Label(mainframe, text='ArchivesSpace Password: ', font=('Arial', 13)).grid(column=2, row=6, sticky=W)
password_input = ttk.Entry(mainframe, width=30, textvariable=password_entry, show='*')
password_input.grid(column=2, row=7, sticky=(W, E))

#CONNECT BUTTON, LOGIN CONFIRMATION/DENIAL
connectbutton = ttk.Button(mainframe, text='Connect!', command=asloginprocess).grid(column=3, row=7, sticky=E)
ttk.Label(mainframe, textvariable=login_confirmed, font=('Arial', 16)).grid(column=3, row=5, sticky=E)

#-------STEP 2: SELECT INPUT CSV------#

#SELECT INPUT CSV HEADER
ttk.Label(mainframe, text='Step 2: Select input CSV: ', font=('Arial', 16)).grid(column=2, row=9, sticky=W)

#INPUT CSV BUTTON AND LABEL INDICATING WHICH FILE IS OPEN
selectfilebutton = ttk.Button(mainframe, text='Select Input CSV', command=opencsv).grid(column=3, row=9, sticky=E)
ttk.Label(mainframe, text='File selected: ', font=('Arial', 13)).grid(column=2, row=10, sticky=W)
ttk.Label(mainframe, textvariable=filename_input, width=90, font=('Arial', 12)).grid(column=2, row=11, columnspan=3, sticky=W)

#-------STEP 3: SELECT OUTPUT DIRECTORY------#

#OUTPUT TXT BUTTON AND LABEL INDICATING WHICH DIRECTORY IS OPEN
ttk.Label(mainframe, text='Step 3: Select output directory: ', font=('Arial', 16)).grid(column=2, row=13, sticky=W)
selectfilebutton = ttk.Button(mainframe, text='Select Output Directory', command=prewritefile).grid(column=3, row=13, sticky=E)
ttk.Label(mainframe, text='Directory selected: ', font=('Arial', 13)).grid(column=2, row=14, sticky=W)
ttk.Label(mainframe, textvariable=txt_name, width=40, font=('Arial', 12)).grid(column=2, row=15, columnspan=3, sticky=W)

#-------STEP 4: CHOOSE AN ACTION------#

#CHOOSE AN ACTION HEADER
ttk.Label(mainframe, text='Step 4: Choose an action: \n', font=('Arial', 16)).grid(column=2, row=16, sticky=W)

#ACTIONS TO CHOOSE FROM BUTTONS
containerbutton = ttk.Button(mainframe, text='Create container profiles', width=30, command=containerprofiles).grid(column=2, row=17, sticky=E)
locationbutton = ttk.Button(mainframe, text='Create locations', width=30, command=locations).grid(column=3, row=17, sticky=W)
topcontainerbutton = ttk.Button(mainframe, text='Create top containers', width=30, command=topcontainers).grid(column=2, row=18,sticky=E)
restrictionbutton = ttk.Button(mainframe, text='Add restrictions', width=30, command=restrictions).grid(column=3, row=18, sticky=W)
instancebutton = ttk.Button(mainframe, text='Create container instances', width=30, command=instances).grid(column=2, row=19, sticky=E)

#-------STEP 5: REVIEW OUTPUT------#

#REVIEW OUTPUT HEADER
ttk.Label(mainframe, text='\nStep 5: Review output: ', font=('Arial', 16)).grid(column=2, row=21, sticky=W)

#VIEW OUTPUT FILE BUTTON AND LABEL INDICATING WHICH FILE IS OPEN
selectfilebutton = ttk.Button(mainframe, text='View Output File', command=openoutput).grid(column=3, row=22, sticky=E)
ttk.Label(mainframe, text='File selected: ', font=('Arial', 13)).grid(column=2, row=22, sticky=W)
ttk.Label(mainframe, textvariable=txt_file, width=90, font=('Arial', 12)).grid(column=2, row=23, columnspan=3, sticky=W)

#VIEW ERROR LOG BUTTON
errorlogbutton = ttk.Button(mainframe, text='View Error Log', command=openerrorlog).grid(column=3, row=24, sticky=E)

#OUTPUT TEXT BOX
ttk.Label(mainframe, text='Output: ', font=('Arial', 13)).grid(column=2, row=24, sticky=W)
printoutput = tkst.ScrolledText(mainframe, wrap=WORD, width=60, height=10)
printoutput.grid(column=2, row=25, columnspan=3, sticky=W)

#RECORD UPDATE SUMMARY LABELS
ttk.Label(mainframe, text='Record updates attempted: ', width=30, font=('Arial', 13)).grid(column=2, row=26, sticky=E)
ttk.Label(mainframe, textvariable=update_attempts, width=30, font=('Arial', 12)).grid(column=3, row=26, sticky=W)
ttk.Label(mainframe, text='Records updated successfully: ', width=30, font=('Arial', 13)).grid(column=2, row=27, sticky=E)
ttk.Label(mainframe, textvariable=updates_success, width=30, font=('Arial', 12)).grid(column=3, row=27, sticky=W)
ttk.Label(mainframe, text='Elapsed time: ', width=30, font=('Arial', 13)).grid(column=2, row=28, sticky=E)
ttk.Label(mainframe, textvariable=elapsed_time, width=30, font=('Arial', 12)).grid(column=3, row=28, sticky=W) 

#----------------------------------------MORE MAINFRAME AND CANVAS STUFF-------------------------------------#

#FINISH CREATING CANVAS
canvas.create_window(0, 0, anchor=NW, window=mainframe)
mainframe.update_idletasks()
canvas.config(scrollregion=canvas.bbox('all'))

#SET SPACING BETWEEN WIDGETS
for child in mainframe.winfo_children():
    child.grid_configure(padx=1, pady=2)

#CREATE EXIT MENU AT TOP OF WINDOW  
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Exit', command=client_exit)
menubar.add_cascade(label='File', menu=filemenu)
root.config(menu=menubar)

#EXECUTE RESIZING FUNCTION UPON RESIZING
mainframe.bind('<Configure>', lambda event, canvas=canvas: onFrameConfigure(canvas))

#EXECUTE ARCHIVESSPACE LOGIN SCRIPT UPON PRESSING ENTER
root.bind('<Return>', asloginprocess)

#LAST BIT OF GUI INITIALIZATION
root.mainloop()
