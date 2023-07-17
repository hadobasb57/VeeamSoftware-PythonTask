# VeeamSoftware-PythonTask
Python Task Solved Adam Hadobas

The FolderSync.py script here is made for keeping an exact replica of the source folder at the destination (replica) folder.
It's starting command line syntax looks like this:
python FolderSync.py "Source_Folder_Path" "Replica_Folder_Path" Sync_Interval(int) "Log_File_Path"

e.g.: python FolderSync.py "C:\Source" "C:\Replica" 10 "C:\Log.txt"

The script:
- Checks if the folders are present (makes the replica folder/subfolders if needed).
- Deletes things from Replica_Folder_Path if they are not in the Source_Folder_Path.
- Copies things from Source_Folder_Path to Replica_Folder_Path.
- Logs the process (in command line and into the log file at the end).
- Does these repetead as set in the Sync_Interval (every x seconds).
