from ftplib import FTP
import os.path

# instructor client
# Func 1: create a folder in ftp server
# Func 2: upload exam question file to the folder
# Func 3: download student's answer file from the folder

def makeDirectory():
    print("------------ Create directory ------------")
    print("Building connection to the ftp server...")
    ftp = FTP()
    ftp.connect('127.0.0.1', 2121)
    print("Connected the ftp server.")
    user = input("Please enter the username: ")
    password = input("Please enter the password: ")
    ftp.login(user=user, passwd=password)
    print("Logged in successfully")
    dir_name = input("Please enter the name of folder you want to create: ")
    ftp.mkd(dir_name)
    print(dir_name, "created.")
    ftp.quit()
    print("------------ Directory Creation Finished------------")

def uploadFile():
    print("------------ Upload file ------------")
    print("Building connection to the ftp server...")
    ftp = FTP()
    ftp.connect('127.0.0.1', 2121)
    print("Connected the ftp server.")
    user = input("Please enter the username: ")
    password = input("Please enter the password: ")
    ftp.login(user=user, passwd=password)
    print("Logged in successfully")

    dir_name = input("Please enter the name of folder you want to go to: ")
    if dir_name in ftp.nlst():
        # change to the directory of the exam folder
        ftp.cwd(dir_name)
        print("Current directory:", ftp.pwd())
    else :
        print("Folder not found, please create the directory first. If you have created the directory, please check the directory name entered.")
        ftp.quit()
        exit(1)

    filepath = input("Please enter the local path of the file you want to upload to server: ")
    if not os.path.isfile(filepath):
        print("Entered file not found.")
        exit(1)
    filename = input("Please name the file in the server: ")

    file = open(filepath, 'rb')
    ftp.storbinary('STOR '+filename, file)
    file.close()
    print("File uploaded successfully")
    ftp.quit()
    print("------------ File Upload Finished------------")

def downloadFile():
    print("------------ Download file ------------")
    print("Building connection to the ftp server...")
    ftp = FTP()
    ftp.connect('127.0.0.1', 2121)
    print("Connected the ftp server.")
    user = input("Please enter the username: ")
    password = input("Please enter the password: ")
    ftp.login(user=user, passwd=password)
    print("Logged in successfully")

    dir_name = input("Please enter the name of folder you want to go to: ")
    if dir_name in ftp.nlst():
        # change to the directory of the exam folder
        ftp.cwd(dir_name)
        print("Current directory:", ftp.pwd())
    else :
        print("Folder not found, please create the directory first. If you have created the directory, please check the directory name entered.")
        ftp.quit()
        exit(1)

    filename = input("Please enter the name of file you want to download: ")
    if filename not in ftp.nlst():
        print("File not found.")
        exit(1)
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()
    print("------------ File Download Finished------------")

if __name__ == '__main__':
    print("File Transfer Client Start.")
    print("Available command: mkdir, upload, download, exit")
    while True:
        command = input("Please enter the command: ")
        if command == "mkdir":
            makeDirectory()
        elif command == "upload":
            uploadFile()
        elif command == "download":
            downloadFile()
        elif command == "exit":
            print("Program Exited.")
            exit(1)
        else:
            print("Invalid command.")
            print("Available command: mkdir, upload, download, exit")