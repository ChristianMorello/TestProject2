#Python script for configuration management tool
# First create a user
from fcntl import DN_DELETE
from time import sleep
from subprocess import check_output
import os
import subprocess
from subprocess import Popen
import sys
import getpass
import random
import string
import time
 
# add user function
def add_user():
 
     # Ask for the input
     print("Enter Username ")
     username = input()   
 
     # Asking for users password
     sudoPassword = randomPasswordGenerator()

     os.system('useradd ' + username)
     command = 'sudo passwd --stdin ' + username
     p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
def randomPasswordGenerator():
    # Getting password length
    length = 9
    characterList = ""
 
    # Getting character set for password

    characterList += string.ascii_letters

    characterList += string.digits
    
    password = []
    for i in range(length):
        
        # Picking a random character from our 
        # character list
        randomchar = random.choice(characterList)

        # appending a random character to password
        password.append(randomchar)
    
    # printing password as a string
    stringPassword = "".join(password)
    print("The random password is " + stringPassword)
    return stringPassword


def install_items():
    inputb = input("Is there enough storage to update the system: Y or N): ")
    if inputb == 'Y':
        os.system('sudo dnf upgrade')
    os.system('sudo yum -y install httpd')
    os.system('sudo yum -y install php-{common,gmp,fpm,curl,intl,pdo,mbstring,gd,xml,cli,zip}')
    os.system('sudo firewall-cmd --permanent --zone=public --add-service=http')
    os.system('sudo firewall-cmd --permanent --zone=public --add-service=https')
    os.system('firewall-cmd --permanent --add-port=80/tcp')
    os.system('firewall-cmd --reload')
    os.system('systemctl enable --now httpd')
    os.system('sudo dnf module enable php')
    os.system('sudo chkconfig httpd on')

def configurePHPfile():
    phpFileContents = ["<!DOCTYPE html>", "<html>", "<body>", "<?php", "$AEST = date_default_timezone_set('Australia/Melbourne');", "echo 'Last name: Morello';", "echo 'AEST Time is: ' . $AEST . '<br>'';", "$CEST = date_default_timezone_set('Italy');", "echo 'AEST Time is: ' . $CEST . '<br>';", "?>", "</body>", "</html>"]
    f = open("/var/www/html/index.php", "w")
    for i in phpFileContents:
        f.write(i + '\n')
    f.close()

def configureSwapFile():
    out = check_output(["swapon", "-s"])
    sf = "swapfile"
    if "swapfile" in out.decode():
        deleteSwap = input("There seems to be another swapfile made, would you like it removed: (Yes or No)")
        if deleteSwap == "Yes":
            os.system("swapoff -v /swapfile")
            with open("/etc/fstab", 'r') as file: 
                 swapData = file.readlines()
            swapData[len(swapData)-1] = ""
            with open("/etc/fstab", 'w') as file: 
                 for i in swapData:
                     file.write(i) 
            os.system("rm -f /swapfile")
        sf = "swapfile2"
        print("swapfile found")
    os.system('sudo dd if=/dev/zero of=/'+sf+'count=4096 bs=1MiB')
    os.system('sudo chmod 600 /' + sf)
    os.system('sudo mkswap /' + sf)
    os.system('sudo swapon /' + sf)
    a = open("/etc/fstab", "a")
    a.write('/' + sf + '   swap    swap    sw  0   0')
    a.close()
def disableSeLinux():
    os.system("sudo setenforce 0")
    count = 0
    number = 0
    with open("/etc/selinux/config", 'r') as file: 
        data = file.readlines()
    for t in data:
        if "SELINUX=d" in t:
            number = count
        elif "SELINUX=e" in t:
            number = count
        elif "SELINUX=p" in t:
            number = count
        count = count + 1
    data[number] = 'SELINUX=disabled' + '\n'
    with open("/etc/selinux/config", 'w') as file: 
        for i in data:
            file.write(i) 
            
print("Test Code? (Yes or No)")
input_b = input()
if input_b == "No":
    add_user()
    install_items()
    time.sleep(10)
    configurePHPfile()
    time.sleep(10)
    configureSwapFile()
    time.sleep(10)
    disableSeLinux()
elif input_b == "Yes":
    a = True
    while a == True:
        input_a = input("Write either, 1, 2, 4, 5, 6 or complete: ")
        if input_a == "1":
            # Step 1
            add_user()
        elif input_a == "2":
            # Step 2 And 3
            install_items()
        elif input_a == "4":
            # Step 4
            configurePHPfile()
        elif input_a == "5":
            # Step 5
            configureSwapFile()
        elif input_a == "6":
            # Step 6
            disableSeLinux()
        elif input_a == "stop":
            a = False
logRemoval = input("If error came up for no storage space left, logs can be removed. Answer Yes Or NO:")
if logRemoval == "Yes":
    os.system("sudo logrotate /etc/logrotate.conf --force")
