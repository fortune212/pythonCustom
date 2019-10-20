#This programs parses a file and remove any duplicate urls
#It also has an option of sorting suspected urls and saving them specialAttFilter.txt

import os.path
from os import path

urlArray = []
loopPrime = 1

#filter url function
def parseUrl(urlStr):
  
                    url = False                  

                    if "/fonts" in urlStr:    
                      url = True

                    elif "json" in urlStr:    
                      url = True
                    elif "/css" in urlStr:    
                      url = True
                    elif ".css" in urlStr:    
                      url = True
                    elif ".svg" in urlStr:    
                      url = True
                    elif "/svg" in urlStr:    
                      url = True

                    elif "/img" in urlStr:    
                      url = True
                    elif ".img" in urlStr:    
                      url = True
                    elif "json" in urlStr:    
                      url = True
                    elif "/css" in urlStr:    
                      url = True

                    elif ".css" in urlStr:    
                      url = True
                    elif ".ico" in urlStr:    
                      url = True
                    elif ".jpg" in urlStr:    
                      url = True
                    elif ".JPG" in urlStr:    
                      url = True
                    elif ".png" in urlStr:    
                      url = True
                    elif ".PNG" in urlStr:    
                      url = True
                    elif ".gif" in urlStr:    
                      url = True

                    elif "/image" in urlStr:    
                      url = True
                    elif ".pdf" in urlStr:    
                      url = True
                    elif ".zip" in urlStr:    
                      url = True

                    elif "youtube" in urlStr:    
                      url = True
                    elif "bootstrap" in urlStr:    
                      url = True
                    elif "w3.org" in urlStr:    
                      url = True
                    elif "twitter" in urlStr:    
                      url = True
                    elif "facebook" in urlStr:    
                      url = True
                    elif "instagram" in urlStr:    
                      url = True
                    elif "wordpress." in urlStr:    
                      url = True

                    elif "play.google" in urlStr:    
                      url = True
                    elif "plus.google" in urlStr:    
                      url = True
                    elif "itunes.apple" in urlStr:    
                      url = True
                    elif "apple." in urlStr:    
                      url = True
                    elif "sign" in urlStr:    
                      url = True
                    elif "login" in urlStr:    
                      url = True

                    return url               

##################################################################################    
#Program start
##################################################################################

while loopPrime == 1:
  getRead = input("\nWhat is the name of the file you want to read(press q to exit):  ")
  if getRead == 'q' or getRead == 'Q':
    exit(0)
  elif not (path.exists(getRead) and os.stat(getRead).st_size != 0):
    print("\tFile is empty or does not exist, try again.")  
  else:
    getReadFile = open(getRead, 'r')
    loopPrime = 0

while loopPrime == 0:
  getWrite = input("\nWhat is the name of the file you want to write(press q to exit): ")
  if getWrite == 'q' or getRead == 'Q':
    getReadFile.close() #close the open file
    exit(0)
  elif not path.exists(getWrite):
    print("\tFile does not exist but will be created")  
    getWriteFile = open(getWrite, 'a')
    loopPrime = 2
  else:
    getWriteFile = open(getWrite, 'a')
    loopPrime = 2

getInst = input("\nWould you like to sort unwanted urls, hit 'y' for yes(press q to exit): ")
if getInst == 'q' or getInst == 'Q':
    getReadFile.close()
    getWriteFile.close() #close the open files
    exit(0)  
elif getInst == 'y' or getInst == 'Y':
  print("\nunwanted urls will be kept in specialAttFilter.txt")
  filterFile = open("specialAttFilter.txt", 'a')

for url in getReadFile.readlines():
  url = url.strip()
  if (url != "\n") and (url not in urlArray):    
    #check if it contains unwanted strings(call function) and option yes
    if (getInst == 'y' or getInst == 'Y') and parseUrl(url):              
      filterFile.write(url + '\n')
    else:        
      getWriteFile.write(url + '\n')     
    urlArray.append(url) #append array

getReadFile.close() 
getWriteFile.close()

if getInst == 'y' or getInst == 'Y':
  filterFile.close()