import os, sys, getpass,re
from settings import *
from utils import *
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain
def type_password():
    password1= getpass.getpass("Enter Password:")
    password2= getpass.getpass("Enter Password Again:")
    if password1==password2:
	return True, password1
    else:
	return False, "Passwords do not match"

def type_email():
    email=raw_input("Enter Email:  ")
    if re.match(email_re, email):
	return True, email
    else:
	return False, "Not a Valid Email Id"
    

def create():
    username=raw_input("Enter the Username for Admin Status:  ")
    try:
	a=Admin.load(username)
	print "Username %s is already an Admin" % username
	sys.exit(0)
    except KeyError:
	a=User()
	a.username= username
	result, email = type_email()
	while result==False:
	    print email
	    result, email = type_email()
	x,y=type_password()
	while x==False:
	    print "Your passwords did not match\n. Try Again"
	    x,y =type_password()
	user = create_user(username=username, password=y, email=email)
	user.save()
	admin =Admin.create(username=username)
	admin.save()
	print "Admin created Successfully"

if __name__=="__main__":
    
    create()
    
