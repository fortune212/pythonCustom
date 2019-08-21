#Filter file script
#Objective
#This script will scan for url(or lines) file 
#for lines that contain some given phrase(s)
#It move match lines(urls) to a seperate file

#open special attention file,
#read all line into array
#search each line for given phrase or words
  #loop through the array and pop out the matches
  #you will be left with unmatched words in the array
  #delete the file and append the new list of words

import os

file_urls = []
getInp = ""

#Read file into array
if os.stat("specialAtt.txt").st_size != 0:
    spAttFile = open("specialAtt.txt", 'r')    
    print("Reading specialAtt.txt file")
    
    for urls in spAttFile.readlines():
      if urls != "\n":
        urls = urls.strip()
        file_urls.append(urls)
    spAttFile.close() 

#Search the array for given strings
#save the lines to sorturl.txt file
while file_urls or getInp:
           #save to file
            if os.stat("sorturl.txt").st_size != 0:
              print("sorturl.txt is not empty, it will be overwritten after the process")
              
            getInp = input("hit 'y' for continue & 'n' for exit : ")

            if getInp == 'y' or 'Y': #if yes
                sortUrlFile = open ("sorturl.txt", 'w')
                sortUrlFile.write("") #clear file
                sortUrlFile.close()

                spAttFile = open("specialAtt.txt", 'w') 
                spAttFile.write("") #clear file
                spAttFile.close() 
               
                #open file for appending
                sortUrlFile = open ("sorturl.txt", 'a')
                spAttFile = open("specialAtt.txt", 'a')
                
                while file_urls:
                    url = file_urls.pop(0)   
                    url = url.strip()                 

                    if url == "\n":    
                      pass

                    elif "/fonts" in url:    
                      sortUrlFile.write(url + "\n")

                    elif "json" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "/css" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".css" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".svg" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "/svg" in url:    
                      sortUrlFile.write(url + "\n")

                    elif "/img" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".img" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "json" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "/css" in url:    
                      sortUrlFile.write(url + "\n")

                    elif ".css" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".ico" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".jpg" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".JPG youtube" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".gif" in url:    
                      sortUrlFile.write(url + "\n")

                    elif "/image" in url:    
                      sortUrlFile.write(url + "\n")
                    elif ".pdf" in url:    
                      sortUrlFile.write(url + "\n")

                    elif "youtube" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "bootstrap" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "w3.org" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "twitter" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "facebook" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "instagram" in url:    
                      sortUrlFile.write(url + "\n")

                    elif "play.google" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "plus.google" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "itunes.apple" in url:    
                      sortUrlFile.write(url + "\n")
                    elif "apple." in url:    
                      sortUrlFile.write(url + "\n")

                    else:
                      spAttFile.write(url + "\n")
               
                sortUrlFile.close() 
                spAttFile.close()  
                print("process completed")
                exit(0)  

            elif getInp == 'n' or 'N': #if no
                print("exitintg")
                exit(0)
            else:
                print("invalid input \n")
                getInp = input("hit 'y' for continue & 'n' for exit : ")