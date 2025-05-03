
# Windows Directory Observer

This project is made for monitoring the appearance of specified files in specified directories. Upon detection, the event will be recorded. Further configuration can be made by changing the arguments in the configuration file.


## Prerequisites
- Python Installation
  - Directories Monitor requires Python version 3.6 or higher to be installed on your system.
  - You can download the latest version of Python from the official Python website: https://www.python.org/downloads/
  - Make sure to add Python to your system's PATH environment variable during the installation process to be able to run Python from the command line.
- Dependencies
  - Directories Monitor uses the external modules below:
    - configparser, winotify, threading, watchdog
  - Some of them may already be installed as build-in modules if you are using the latest version of Python. If you don't have these modules installed, you can install it using pip, the Python package manager as follows:    
  ```bash
  pip install winotify 
  ```

## Installation

After downloading the `.zip` file, keep all files in the same directory. Keep the name of the configuration file unchanged as `config.ini`. Read the next session and make sure you have the configuration file paramenters correct. Change the paths location to an existing path before running.

In case of deleting the configuration file accidentally, running the `main.py` will recreate the default configuration file.



    
## Configuration file
The key names are case-insensitive. The following is an example of the configuration file `config.ini`:
```bash
[Default]
monitored_paths = C:\Users\Name\Documents, C:\Users\Name\Downloads
filenames = virus, apple
filetypes = csv, txt
startTime = 
endTime = 2024/07/29 21:10
exactMatch = False
caseSensitivity = True
recursive = True
report_location = C:\Users\Name\Documents\ObserverLog

[CustomSetup]
monitored_paths = 
filenames = 
filetypes = 
startTime = 
endTime = 2024/07/29 21:10
exactMatch = False
caseSensitivity = True
recursive = True
report_location = 

```

- **monitored_paths:** The directories to be monitored. The path can be directly copied and pasted from the file explorer. Use a comma to delimit if there are more than one path.
- **filenames:(optional)** 
  `Default=""` The specific filenames that you want to observe. Leaving it empty with **exactMatch** set to be false implies that all files will be observed. Use a comma to delimit if there are more than one name.
- **filetypes:(optional)** 
  `Default=""` The file types that you want to observe. Leaving it empty implies that all file types will be observed. Use a comma to delimit if there are more than one file type.
- **startTime:(optional)** 
  `Default=datetime.now()` The starting time of the observer in the format of `YYYY/MM/DD HH:mm`. It has to be a time later than the current time. Leaving it empty implies the program will start observing instantly when it is run.
- **endTime:(optional)** `Default=datetime.now()+timedelta(hours=1)` The stopping time of the observer in the format of `YYYY/MM/DD HH:mm`. It has to be a time later than the starting time. Leaving it empty implies the program will stop observing one hour later.
- **exactMatch:** True implies that it will look for exactly the **filenames** stated; False imples that it will look for files that contain the **filenames** stated. It accepts:
  `True/true/Yes/yes/False/false/No/no`  
- **caseSensitivity:** 
  True implies that the observer is case-sensitive when matching **filenames**, vice versa. It accepts:
  `True/true/Yes/yes/False/false/No/no`
- **recursive:** 
  True implies that the observer will look for all sub-directories inside **monitored_paths**; False implies that the observer will only look for files in the **monitored_paths** but not including their sub-directories. It accepts:
  `True/true/Yes/yes/False/false/No/no`
- **report_location:** 
  The path that the logging file will be outputted. The output filename will be in the format of`log_at_HHmm_on_YYYYMMDD.txt`




The script utilizes a configuration file that offers several benefits:

- **Accessibility for Non-Coders:** Users without a deep understanding of coding can easily amend the settings of the script in a straightforward manner.
- **Intuitive Syntax:** The `.ini` file format uses a syntax that is similar to ordinary English, with items delineated by commas and no need for quotation marks around strings or brackets around lists.
- **Simplicity:** Users can directly copy and paste the paths they want to monitor, without having to worry about escaping backslashes or navigating complex configuration structures.


## Usage
Once the parameters are input correctly to the configuration file, you can run the `main.py` file, and you will be prompted to input the setup, press enter if Default is the desired setup. 

Run the `main.py` by either clicking it in file explorer directly or run the command line after navigating in the terminal to the directory where the file is located:
```terminal
python -u main.py
```

You can save your preferred configuration by inputting parameters in the configuration file under [CustomSetup]. When you run the `main.py`, type in "CustomSetup"(case-sensitive) to use your customized setup. You can create more than one customized setup by copying the whole session and appending it in the `config.ini`.


## Assumptions
- The time recorded is based on the system time that the program is running on. 
- Filenames do not have dot `.` (the dot in file extension is not included) 
- All files are having a file extension, e.g. `.csv` `.docx` `.zip` etc.
- The exact match option is only on the filename, file extensions are set to be always exact match, e.g. if you are looking for `.doc`, the program will not monitor files of `.docx`, if you want to look for both, you can input `doc, docx` in the extension parameters of the configuration file.

## Optimizations
Threading is used rather than multiprocessing because the oberver is more I/O bound instead of CPU bound. This program does not involve complicated calculation, but oberving the directories are predominantly an I/O operation as it requires reading and processing file system data. By threading, it allows concurrent observation of multiple paths efficiently. The script is optimized by having conditional statements to skip unnecessary calculations. 

Also, the program's termination is optimized by using a precalculated running time as an argument to time.sleep() instead of regularly checking the current time, which saves resources compared to continuously monitoring the time.

## Further Extensibility/Features
- Easily Scalable Monitoring
  - Additional directories, filenames, file types can all be added to the program easily by simply appending the path in the configuration file by a comma
- Customized Configuration
  - User can add different custom setups in the configuration file so that the desired parameters can be used without the need to change the configuration file everytime
- Folders Observation
  - The watchdog module used is able to identify whether the event is driven by a file change or a directory change. Therefore, this observer can be easily extended to folder Observation.
- Autosaved Logging
  - Even when the program is terminated during runtime, the logging messages will already be recorded in a separate file in the path provided.
- Input validation 
  - There is error checking for the inputs in the configuration file. In case of invalid parameters, the script will print an error message and exit with code 1.


## Author

- [Casen Chan](https://www.github.com/Casennnn)

