from configparser import ConfigParser

class ConfigWriter():

    try:
        with open("config.ini", "x") as f:
            config = ConfigParser()

            config["Default"] = {
                "monitored_paths" : "C:\\Users\\Name\\Documents, C:\\Users\\Name\\Downloads",
                "filenames" : "virus, apple",
                "filetypes" : "csv, txt",
                "startTime" : "",
                "endTime" : "",
                "exactMatch" : "False",
                "caseSensitivity" : "True",
                "recursive" : "True",
                "report_location" : "C:\\Users\\Name\\Documents\\ObserverLog",
            }
            config["CustomSetup"] = {
                "monitored_paths" : "",
                "filenames" : "",
                "filetypes" : "",
                "startTime" : "",
                "endTime" : "2024/07/29 21:10",
                "exactMatch" : "False",
                "caseSensitivity" : "True",
                "recursive" : "True",
                "report_location" : "",
            }
            config.write(f)
            print("New config file created")
    except FileExistsError:
        print("Using existing config file")
        pass

#ConfigWriter()  #for testing