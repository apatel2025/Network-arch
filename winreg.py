#------------------------------------------------------------------------------
# Description: This Script lets the user handle windows registry using python.
#			   Using command line parameters to provide input in order to 
#			   perform different operations.	
#
# Parameters:  sys.argv[0] = Root Key/ Root key path
#			   sys.argv[1] = Value name 
#  			   sys.argv[2] = The value itself
#
# Author: A. Patel
# Date: 2018-07-06                 
#------------------------------------------------------------------------------

#importing all necessary modules 
import sys
import _winreg as winreg
import win32api
import win32security

#defining main
def main():

	#defining a few variable to allow the user to change values by updating the privileges
	access= win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
	token= win32security.OpenProcessToken(win32api.GetCurrentProcess(),access) 
	Secure= win32security.LookupPrivilegeValue(None, "SeBackupPrivilege")
	win32security.AdjustTokenPrivileges(token,0,[(Secure,win32security.SE_PRIVILEGE_ENABLED)])

#to execute all commands of the script
if __name__=="__main__":

	#dictionary to locate root key objects by root key abbreviation 
	HK = {}
	HK['HKCR']=winreg.HKEY_CLASSES_ROOT
	HK['HKCU']=winreg.HKEY_CURRENT_USER
	HK['HKLM']=winreg.HKEY_LOCAL_MACHINE
	HK['HKU']=winreg.HKEY_USERS
	HK['HKCC']=winreg.HKEY_CURRENT_CONFIG

	#using the try and except command so that if any code block causes an error, the code will stop executing
try:
	if len(sys.argv) == 1 :
		#if no parameters provided this part of the code prints a list of root key values
		print "Root key values are: ",     
		print HK.keys()
  
	if len(sys.argv) > 1 :
#at least one command line parameter provided
		if sys.argv[1].find('\\') > 0:
	# \ is present in key, so there must be a subkey
	# root key precedes the \  Convert to upper to simplify the lookup
			RootKey=sys.argv[1][0:sys.argv[1].find('\\')].upper()
	# everything after the \ is one or more subkeys
			SubKeys=sys.argv[1][sys.argv[1].find('\\')+1:]

			if SubKeys.find('\\') > 0:
			# \ in the subkeys means there is more than one 
			# extract the first subkey
				SubKey=SubKeys[0:SubKeys.find('\\')]
				SubKeys=SubKeys[SubKeys.find('\\')+1:]
			else:
		#just one subkey
				SubKey=SubKeys
				SubKeys=''
		else:
		# if there are no subkeys
			RootKey=sys.argv[1].upper()
			SubKey=''
			SubKeys=''
	
	#printing an error message when something other than the root key is inserted in the command line parameter
	if not RootKey in HK.keys():
		print "Invalid root key", RootKey
	
	else:
		print RootKey,SubKey, SubKeys
		#open first subkey
		OurKey=winreg.OpenKey(HK[RootKey],SubKey)
		
	#keep searching until no more subkeys are left
	while not SubKeys == '':
	
		if SubKeys.find('\\') > 0:
			SubKey=SubKeys[0:SubKeys.find('\\')]
			SubKeys=SubKeys[SubKeys.find('\\')+1:]
		
		else:
			SubKey=SubKeys
			SubKeys=''
			OurKey=winreg.OpenKey(OurKey,SubKey)
	  
    #print the subkeys and values of the key specified by the user
	for subkey in range(winreg.QueryInfoKey(OurKey) [0]):
		print winreg.EnumKey(OurKey,subkey) ,"\n"
	 
	for subkey in range(winreg.QueryInfoKey(OurKey) [1]):
		print winreg.EnumValue(OurKey,subkey)[0:2], "\n"  
    
	#code block to save the backup file
	if len(sys.argv) > 2:
		FILE = sys.argv[2]
		if FILE.find('File:') == 0:
			winreg.SaveKey(OurKey,FILE[5:])
		else:
			KeyName=sys.argv[2]
			Value=winreg.QueryValueEx(OurKey,KeyName) [0]
		
			print "The path is " + sys.argv[1]+"\\"+sys.argv[2]
			print "\nValue of" ,KeyName, "is" , Value 
		
	#code block for assigning new values to the subkeys
	if len(sys.argv) > 3:
		NewKey=winreg.OpenKey(OurKey,None,0,winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(NewKey,KeyName,0,winreg.QueryValueEx(OurKey,KeyName)[1],sys.argv[3])
		print "The new value is:", winreg.QueryValueEx(OurKey,KeyName)[0]
			
except Exception:
	pass

#closing main	
main()	
