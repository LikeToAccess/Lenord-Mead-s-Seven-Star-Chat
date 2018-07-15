from ftplib import FTP
from hashlib import md5
from os import system, remove
from time import sleep, time
from getpass import getpass as passIn

#
# Verifies that the login informaition is valid
#
def login():
	global username
	global passwd
	
	grabFile("login.txt")
	myHash = md5(passwd).hexdigest()  # turns the normal password into a hashed version
	check_user = readFile(True, "login.txt", 1).lower()
	check_pass = readFile(True, "login.txt")
	check_user = " ".join(check_user).split()  # changes the check_user to a list to remove the appending new line character
	check_user = "".join(check_user)  # changes back into a string

	if check_user == username:
		check_user = True
		print "\nUsername is a match"
	else:
		check_user = False
		print "\nUsername does not match"
		
	if check_pass == myHash:
		check_pass = True
		print "Password is a match\n"
	else:
		check_pass = False
		print "Password does not match\n"
		
	sleep(2)
	
	if check_user and check_pass:
		return True
	else:
		return False
	
#
# Sends informaition to server
#
def signup():
	global username
	global passwd

	myHash = md5(passwd).hexdigest()  # turns the normal password into a hashed version
	writeFile(username, myHash, "login.txt")  # writes the userbame and hashed password to the file
	
	clear()
	print "loading..."
	setup()
	clear()
	
	sendFile("login.txt", "login.txt")  # sends login.txt data to the server as login.txt

#
# Sets up some initial variables.
#
def setup(badconn = False, listdir = False):
    global ftp
    global buff
    global username
    
    message = readFile()
    writeFile(message,username)  # writes the username to the file 
    if badconn == False:  # checks if the client gets disconnected
        try:
            ftp.quit()
        except:
            setup(True)
    server = "files.000webhost.com"
    buff = 1024  # buffersize affects speed of data sent from server to client
    ftp = FTP(server)
    ftp.login(user='savetheblue', passwd='12345678')  # connects the client to the server
    if listdir == True:
        ftp.retrlines('LIST')  # prints a list of directories

#
# Takes a file from the server.
#
def grabFile(filename="recv.txt"):
    global ftp
    global buff
    
    localfile = open(filename, "wb")
    try:
        ftp.retrbinary("RETR "+filename, localfile.write, buff)  # takes a file from the server and writes it's data to a local file
    except:
        localfile.close()
        setup()
        grabFile(filename)
    
    localfile.close()
    localfile = open(filename, "r")
    message = localfile.readline().split()
    message = " ".join(message)  # changes the message variable from a list to a string
    localfile.close()
    return message

#
# Sends a file to the server.
#
def sendFile(filename="message.txt", filename2="recv.txt"):
    global username
    global log
    global ftp

    message = readFile()
    writeFile(message,username)  # writes the username to the file
    f = open(filename,"rb")
    ftp.storbinary('STOR '+filename2, f)  # sends the file data to the server
    f.close()

#
# Reads a text file.
#
def readFile(readlines=False, filename="message.txt", line=2, user=False):
    localfile = open(filename,"r")
    
    if not user:
        message = readFile(user=True)  # user param prevents recursion
        writeFile(message,username)  # writes the username to the file
    if readlines:
        log = localfile.readlines()  # reads all lines of a file
        log = log[line-1]  # reads a specified line in a file
    else:
        log = localfile.readline()  # reads the first line of a file
        
    localfile.close()
    return log

#
# Writes to a text file.
#
def writeFile(text1, text2=None, filename="message.txt"):
    f = open(filename,"w")
    
    if not text2:
        f.write(text1)  # writes one line of text
    else:
    	f.writelines(text1+"\n"+text2)  # writes two lines of text
    	
	f.close()

#
# Appends to a text file.
#
def appendFile(text1, text2=None, filename="login.txt"):
	f = open(filename,"a")
	
	if not text2:
		f.write(text1)  # writes one line to the end of a file
	else:
		f.write(text1)  # writes two lines to the end of a file
		f.write(text2)  # 
		
	f.close()
	
#
# Clears the screen
#
def clear():
	system("clear")  # clears the screen of all text

#
# Finds the latency between to points in time
#
def latency(time1, time2):
            	speed = (time2-time1) * 1000  # finds the difference beyween the two times and converts tge messurment to milli-seconds
            	speed = str(speed)  # converts speed from a float to a string
            	if len(str(speed)) < 13:  # if the leangth is less than thirteen chars then it puts on zeros until it is 13
            		speed = " ".join(speed).split()  # changes speed from a string to a list
            		for i in range(13-len(speed)):
            			speed.append("0")  # puts zeros on the end
            		speed = "".join(speed)  # changes speed back to a string
            	print "latency:   ", speed + "ms"
	
#
# Loop that calles other functions
#
def main():
    clear()
	
    global username
    global passwd
    global recv
    
    print "WELCOME TO LENORD MEAD'S SEVEN STAR CHAT\n"
    sleep(1)
    
    print "We value our client privacy and encrypt all user informaition. Therefore we use secure Password input, when entering a Password no characters will apear."
    sleep(3)
    
    print "(Your Password will still be entered even if you can't see it)"
    sleep(1.8)
    
    print "\nIf you wish to continue Anonymous, leave the area bellow blank.\n\n"
    sleep(1.2)
    
    choice = raw_input('Do you want to "log in" or "sign up" for LM7SC?     ').lower()
    sleep(0.6)
    clear()
    
    choiceAwnsers = [["sign up", "signup"], ["login", "log in", "signin", "sign in"]]  # possible input choices for main menu
    
    if choice in choiceAwnsers[0]:
    	print "We value our client privacy and encrypt all user informaition. Therefore we use secure Password input, when entering a Password no characters will apear. (Your Password will still be entered even if you can't see it)\n\n"
    	username = raw_input("Enter a Username:     ").split()
    	passwd = passIn("Enter a Password:     ").split()
    	passwd_check = passIn("Re-Enter your Password:     ").split()
    	
    	if passwd == passwd_check:
    		print "New account", username, "created succesfully!"
    		sleep(1.5)
    	elif passwd != passwd_check:
    		print "Some how you FAILED to type your Password TWO times in a row. Better luck next time you will be registered as Anonymous."
    		sleep(2.6)
    		username = ["Anonymous"]
    
    elif choice in choiceAwnsers[1]:
    	username = raw_input("Enter your Username:     ").split()
    	passwd = passIn("Enter your Password:    ").split()
    	
    else:
    	username = ["Anonymous"]
    	passwd = ["spam"]
    
    passwd = passwd[0]
    check_latency = False
    
    # if username is two words, check the latency of the loop
    try:
    	spam_var = username[1]  # spam_var is just a test variable that is not used
    except IndexError as e:
    	check_latency = True
    	
    username = username[0]  # username can only be one word
    
    if choice in choiceAwnsers[0]:
    	signup()
    	print "Your data is valid. Thank you for using LM7SC!"
    
    elif choice in choiceAwnsers[1]:
    	if login():
    		print "Your data is valid. Thank you for using LM7SC!"
    	else:
			print "Your data is invalid. You will be registered as Anonamous. Thank you for using LM7SC!"
			username = "Anonyms"
			
        sleep(3.6)
    
    clear()
    print "setting up..."
    setup()
    
    clear()
    print "sending data..."
    writeFile("Type Text Here", username)  # writes Type Text Here on the first line of the file
    sendFile()
    
    clear()
    print "grabbing data..."
    recv = grabFile()  # recv helps determine when the user has changed the file or not
    
    clear()
    print "waiting for messages to be sent..."
    user = readFile(True, "recv.txt", 3)
    user_list = [user]
    print user, "has joined!"
    
    def loop():
        global log
        global recv
        
        log = readFile()
        First = True
        Running = True
        
        while Running:
            time1 = time()
 
            if recv == grabFile():  # if the file is unchanged don't print it's data
                recv = grabFile()
                
            elif recv != grabFile():  # if the file is changed print the data
            	writeFile(grabFile(),username)
            	if First:
            		clear()
            		First = False
            		
                print "<"+user+">",grabFile()  # formats the file data to print the username then the message
                if user != username and user not in user_list:
                	user_list.append(user)
                	print user, "has joined!"
                	print "Current users:",
                	for client in range(len(user_list)):
                		print user_list[client],
                	print ""
                	
                
                recv = grabFile()
                
            if log == readFile():  # if the local file is unchanged don't send it to the server
                log = readFile()
            elif log != readFile():  # if the local file is chanhed upload it's data to the server
                sendFile()
                log = readFile()
                
            if not check_latency:
                latency(time1, time())  # finds the latency between the beginning of the loop and the current time
        
        ftp.quit()
    
    # runs the loop and if an error occurs it resets and tries again
    try:
        loop()
    except:
        setup()
        loop()

main()
