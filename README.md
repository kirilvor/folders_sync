Folder Synchronization Program

Hello this program is designed to synchronize two folders, maintaining an identical copy of the source folder at the replica folder.
The synchronization is one-way, which ensures that changes made to the source folder are reflected in the target folder.

Usage:
1. Clone or download: Obtain the program's source code from the repository.
2. Install dependencies: Make sure the required Python libraries (e.g. os, shutil, time, argparse, hashlib) are installed.
3. Run the program: Run the Python script from the command line with the required arguments:

   python folders_sync.py <source_folder> <replica_folder> <interval> <log_file>

Replace <source_folder>, <replica_folder>, <interval>, and <log_file> with the actual paths and values.
