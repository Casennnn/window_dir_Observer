from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
from winotify import Notification
import getpass, os


#this class does the main tasks of the observer, including but not limited logging, record the event at a designated location, trigger system notification, detect appearance of files with specified pattern
class Handler(PatternMatchingEventHandler):
    def __init__(self, filename ="", caseSensitive = True, extension = "", exactMatch = True, reportpath = ''): #remove some default later
        self.filename = filename
        self.exactMatch = exactMatch
        self.reportpath = reportpath
        if extension =="":
            PatternMatchingEventHandler.__init__(self,patterns=[f"*{filename}*.*"], case_sensitive= caseSensitive,
        ignore_directories=False,ignore_patterns=None)
        else:
            PatternMatchingEventHandler.__init__(self,patterns=[f"*{filename}*.{extension}"], case_sensitive= caseSensitive,
            ignore_directories=False,ignore_patterns=None)

    def log(self,message):
        formatted_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(formatted_datetime, "-", message)  #log to terminal
        with open(self.reportpath, 'a') as file:
            print(formatted_datetime, "-", message, file=file)   #write to txt

    def on_created(self,event): #if file of specified file name appear
        if event.is_directory == False:
            rightmost_slash_index = event.src_path.rindex('\\') # Split the file path into the two parts
            location = event.src_path[:rightmost_slash_index]
            filename = event.src_path[rightmost_slash_index+1:]
            if self.exactMatch and filename.split(".")[0]==self.filename or not self.exactMatch:
                user = getpass.getuser()
                self.log(f"{user} created {filename} at {location} " )
                toast = Notification("Windows Directory Observer",f"{user} created {filename}", f"at {location}",duration = 'short')
                toast.show()


    def on_moved(self,event):
        if event.is_directory == False:
            user = getpass.getuser()
            dest_rightmost_slash_index = event.dest_path.rindex('\\') # Split the file path into the two parts
            dest_location = event.dest_path[:dest_rightmost_slash_index]
            dest_filename = event.dest_path[dest_rightmost_slash_index+1:]
            src_rightmost_slash_index = event.src_path.rindex('\\') # Split the file path into the two parts
            src_location = event.src_path[:src_rightmost_slash_index]
            src_filename = event.src_path[src_rightmost_slash_index+1:]
            if dest_location==src_location: #case where files are renamed
                #filter out case that the original filename match the pattern but not the final filename
                if self.filename in dest_filename:
                    if self.exactMatch and self.filename == dest_filename.split(".")[0] or not self.exactMatch:
                        self.log(f"{user} renamed {src_filename} to {dest_filename} at {dest_location} " )
                        toast = Notification("Windows Directory Observer",f"{user} renamed {src_filename} to {dest_filename}", f"at {dest_location}",duration = 'short')
                        toast.show()
                else:
                    pass
                
                
            else: #case where files are moved
                if self.exactMatch:
                    if self.filename==dest_filename.split(".")[0]:
                        self.log(f"{user} moved {dest_filename} from {src_location} to {dest_filename}" )
                        toast = Notification("Windows Directory Observer",f"{user} moved {dest_filename}", f"from {src_location} to {dest_filename}",duration = 'short')
                        toast.show()
                else:
                    self.log(f"{user} moved {dest_filename} from {src_location} to {dest_filename}" )
                    toast = Notification("Windows Directory Observer",f"{user} moved {dest_filename}", f"from {src_location} to {dest_filename}",duration = 'short')
                    toast.show()