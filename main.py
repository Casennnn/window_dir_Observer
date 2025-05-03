from configparser import ConfigParser
from configwriter import ConfigWriter
import threading, sys, time, os
from watchdog.observers import Observer
from myHandler import Handler
from datetime import datetime, timedelta


ConfigWriter() #creating a config file if not exist
config = ConfigParser()
config.read("config.ini")


#-----for choosing setup-----
while True:
    setup = input("Press Enter if using the default setup: ")
    if setup == '':
        config_data = config["Default"]
        break
    else:
        try:
            config_data = config[setup]
            break
        except:
            print("Setup not found!")
#-----for choosing setup-----




#-----for getting the configuration-----
if config_data['monitored_paths']==""  or config_data['exactMatch']=="" or config_data['caseSensitivity']=="" or config_data['recursive']=="" or config_data['report_location']=="" :
    print("Missing required arguments!! Please check your config.ini")
    exit(1)
listOfPath = [item.strip() for item in config_data['monitored_paths'].split(',')]
for path in listOfPath:
    if not os.path.exists(path):
        print("monitored_paths not exist!!")
        exit(1)
matchFilename = [item.strip() for item in config_data['filenames'].split(',')]
matchExtension = [item.strip() for item in config_data['filetypes'].split(',')]
try:
    isCaseSensitive = config_data.getboolean("caseSensitivity")
    isRecursive = config_data.getboolean("recursive")
    isExactMatch = config_data.getboolean("exactMatch")
except:
    print("Boolean variables are not input correctly!! Check caseSensitivity, recursive, and exactMatch!!")
    exit(1)
if config_data['startTime'] == "":
    progStartTime = datetime.now()
else:
    try:
        progStartTime = datetime.strptime(config_data['startTime'], "%Y/%m/%d %H:%M")
    except:
        print("Start time format incorrect!!")
        exit(1)
    if progStartTime<=datetime.now():
        print("Start time has to be later than current time!! Leave the start time empty if you want to start the program now.")
        exit(1)

if config_data['endTime'] == "":
    progEndTime = datetime.now()+timedelta(hours=1)
else:
    try:
        progEndTime = datetime.strptime(config_data['endTime'], "%Y/%m/%d %H:%M")
    except:
        print("End time format incorrect!!")
        exit(1)
    if progStartTime>=progEndTime:
        print("End time has to be later than start time!! Leave the end time empty if you want to run program for one hour.")
        exit(1)

reportpath = config_data['report_location']
if not os.path.exists(reportpath):
        print("report_location not exist!!")
        exit(1)
formatted_datetime = progStartTime.strftime("at_%H%M_on_%Y%m%d")
reportpath+="\\log_"+formatted_datetime+".txt"
#-----for getting the configuration-----



            
#-----function for monitoring a specific path-----
def direct_mon(path,fileName="", caseSensitivity = True, extension = "", exactMatch = True, recursive = True, reportpath = ''):  # remove some default later
    event_handler = Handler(filename= fileName, caseSensitive = caseSensitivity, extension= extension, exactMatch = exactMatch, reportpath = reportpath)
    observer = Observer()
    observer.schedule(event_handler, path, recursive = recursive)
    observer.start()
    while True:
        time.sleep(1000)  #running the handler infinitely
#-----function for monitoring a specific path-----




if __name__ == "__main__":
    if datetime.now()<progStartTime: #would be the scheduled case where we have to wait to start       
        print("Scheduled start time is ",config_data['startTime'],". Waiting to start observer...")     
        time.sleep((progStartTime-datetime.now()).total_seconds())
        
    for i in range(len(listOfPath)):
        for j in range(len(matchFilename)):
            for k in range(len(matchExtension)):
                t1 = threading.Thread(target=direct_mon, args=[listOfPath[i],matchFilename[j],isCaseSensitive,matchExtension[k],isExactMatch,isRecursive,reportpath], daemon= True)
                t1.start()            
    print("\nStart Observation...")
    print("=====================")
    time.sleep((progEndTime-datetime.now()).total_seconds())  #controlling the termination of the program
    print("=====================")
    print("Finish Observation")
    
        