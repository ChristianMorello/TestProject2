# Python script for configuration management tool
# First create a user
from fcntl import DN_DELETE
import os
import subprocess
import sys
import getpass
import random
import string
 
# add user function
# Sourced from https://www.geeksforgeeks.org/add-a-user-in-linux-using-python-script/
def add_user():
 
     # Ask for the input
     username = input("Enter Username ")   
 
     # Asking for users password
     password = randomPasswordGenerator()
        
     os.system('useradd ' + username)
     os.system('passwd ' + password)
     os.system(password)

# Sourced from https://www.geeksforgeeks.org/create-a-random-password-generator-using-python/

def randomPasswordGenerator():
    # Getting password length
    length = 14
    characterList = ""
 
    # Getting character set for password

    characterList += string.ascii_letters

    characterList += string.digits

    characterList += string.punctuation
    
    password = []
    
    for i in range(length):
    
        # Picking a random character from our 
        # character list
        randomchar = random.choice(characterList)
        
        # appending a random character to password
        password.append(randomchar)
    
    # printing password as a string
    print("The random password is " + "".join(password))
    return password

def install_items():
    os.system('sudo nf upgrade')
    os.system('sudo yum -y install httpd')
    os.system('sudo yum -y install php')
    os.system('firewall-cmd --permanent --add-port=80/tcp')
    os.system('firewall-cmd --reload')
    os.system('systemctl enable --now http')
    os.system('sudo chkconfig httpd on')

def configurePHPfile():
    phpFileContents = ["<!DOCTYPE html>", "<html>", "<body>", "<?php", "$AEST = date_default_timezone_set('Australia/Melbourne');", "echo 'Last name: Morello';", "echo 'AEST Time is: ' . $AEST . '<br>'';", "$CEST = date_default_timezone_set('Italy');", "echo 'AEST Time is: ' . $CEST . '<br>';", "?>", "</body>", "</html>"]
    f = open("/var/www/html/index.php", "w")
    for i in len(phpFileContents):
        f.write(i + '\n')
    f.close()

def configureSwapFile():
    os.system("sudo dd if=/dev/zero of=/swapfile count=4096 bs=1MiB")
    os.system("sudo chmod 600 /swapfile")
    os.system("sudo mkswap /swapfile")
    os.system("sudo swapon /swapfile")
    a = open("/etc/fstab", "a")
    a.write("/swapfile   swap    swap    sw  0   0")
    a.close()

def disableSeLinux():
    with open("/etc/selinux/config", 'r') as file: 
        data = file.readlines()
    for t in data:
        if t == "SELINUX=disabled":
            continue
        elif t == "SELINUX=enforcing":
            t = "SELINUX=disabled"
        elif t == "SELINUX=permissive":
            t = "SELINUX=disabled"
    
    with open("/etc/selinux/config", 'w') as file: 
        file.writelines(data) 


a = True
while a == True:
    print("Step 1, Step 2, Step 4, Step 5 or Step 6")
    input_a = input()
    if input_a == 1:
        # Step 1
        add_user()
    elif input_a == 2:
        # Step 2 And 3
        install_items()
    elif input_a == 4:
        # Step 4
        configurePHPfile()
    elif input_a == 6:
        # Step 5
        configureSwapFile()
    elif input_a == 6:
        # Step 6
        disableSeLinux()