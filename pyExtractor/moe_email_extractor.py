from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
import re
import urllib.robotparser
import random
import datetime
import os
import time

from socket import error, timeout
import errno

numOfProcessedUrl = 0
numOfProcessedEmail = 0

numOfUrlToProc = 0

# a set of crawled emails
emails = []

#Read url from file
new_urls = []

#for extracted urls
extracted_urls = []

# robots.txt sites
robot = []

# waiting urls
waiting = []
expTime = []

wwwRegList = []

#headers to choose randomly
headerList = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
  'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
  'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
  'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
  'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.16',
  'Opera/9.00 (Windows NT 5.1; U; en)',
  'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
]

getInst = input("What kind of file do you want to extract. \n\thit 'U' for web urls or 'F' for local file(search.html) : ")

readProcPrimer = 1

##################################################################################
#Waitlist - Add 3 mins wait for each domain
##################################################################################
def waitList(base_url):
  now = datetime.datetime.now()
  twoMin = now.minute + 3

  print("\tprocess successful")

  #minute cannot be greater than 59, 
  if twoMin < 59:
    exTime = now.replace(minute = twoMin)
    waiting.append(base_url)
    expTime.append(exTime)
    print("\twait (wait url domain) \n")
    updateWaitList()
  else:
    print("\tsleep 30 (delay url domain) \n")
    time.sleep(30)

##################################################################################
#parseUrl - filter url function
##################################################################################
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

                    elif "github" in urlStr:    
                      url = True

                    elif "microsoft" in urlStr:    
                      url = True

                    elif "gmail" in urlStr:    
                      url = True

                    elif "pinterest" in urlStr:    
                      url = True

                    elif ".css" in urlStr:    
                      url = True
                    elif ".ico" in urlStr:    
                      url = True
                    elif ".jpg" in urlStr:    
                      url = True
                    elif ".JPG" in urlStr:    
                      url = True

                    elif ".exe" in urlStr:    
                      url = True
                    elif ".dll" in urlStr:    
                      url = True

                    elif ".jpeg" in urlStr:    
                      url = True
                    elif ".JPEG" in urlStr:    
                      url = True
                    elif ".png" in urlStr:    
                      url = True
                    elif ".PNG" in urlStr:    
                      url = True
                    elif ".gif" in urlStr:    
                      url = True

                    elif "help." in urlStr:    
                      url = True
                    elif "accounts." in urlStr:    
                      url = True
                    elif "account." in urlStr:    
                      url = True

                    elif "/image" in urlStr:    
                      url = True
                    elif "video" in urlStr:    
                      url = True
                    elif "Video" in urlStr:    
                      url = True
                    elif ".pdf" in urlStr:    
                      url = True

                    elif ".xls" in urlStr:    
                      url = True
                    elif ".csv" in urlStr:    
                      url = True
                    elif ".zip" in urlStr:    
                      url = True
                    elif ".mp" in urlStr:    
                      url = True

                    elif "linkedin" in urlStr:    
                      url = True   

                    elif ".webm" in urlStr:    
                      url = True  

                    elif ".t." in urlStr:    
                      url = True
                                        
                    elif "cookies" in urlStr:    
                      url = True 
                    elif "mozilla" in urlStr:    
                      url = True       
                    elif "support." in urlStr:    
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
                    elif "amazon." in urlStr:    
                      url = True
                    elif "sign" in urlStr:    
                      url = True
                    elif "login" in urlStr:    
                      url = True

                    elif "tumblr.com" in urlStr:    
                      url = True

                    return url               

##################################################################################
#regexExtract - extract urls and emails using regex
#  possible error - urlText should be a string(utf-8) else(error), 
#                   It could be binary or non utf-8 string (iso-notString)
##################################################################################
def regexExtract(urlText, url): 
    global numOfProcessedEmail
    try:
      #if data is not string, try decoding, else error
      if type(urlText) != str:
        urlText = urlText.decode()
 
      #Extract the url and email from string
      new_emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urlText, re.I)
      urlht = re.findall(r"(http|ftp|ftps|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
      wwwRegTuple = re.findall(r"(http|ftp|ftps|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
      regTuple = re.findall(r"(www).([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
          
    except:      
      #Instantiate local variables with proper values after error, it could be called below
      new_emails = []
      urlht = []
      wwwRegTuple = []
      regTuple = []
      urlText = ""
      
      #If url is not empty, save the url
      if url != "":
        print("\tproblem with email extraction, moving url to extProb.txt")
        contNotStrFile = open("extProb.txt", 'a')
        contNotStrFile.write(url + "\n")
        contNotStrFile.close() 
      else:
        print("\tproblem with email extraction")               

    #save to file
    #open email.txt and append
    if len(new_emails): 
      emailFile = open("emails.txt", 'a')
      while len(new_emails):
          if not new_emails[0].startswith('.') and new_emails[0] not in emails and '.PNG' not in new_emails[0] and '.png' not in new_emails[0] and '.JPG' not in new_emails[0] and '.jpeg' not in new_emails[0] and '.JPEG' not in new_emails[0] and '.jpg' not in new_emails[0]and '.amazon' not in new_emails[0]:
            get_email = new_emails.pop(0)
            numOfProcessedEmail = numOfProcessedEmail + 1
            print("\tsaving email ", numOfProcessedEmail)
            emails.append(get_email)  
            emailFile.write(get_email + "\n")
          else:
            new_emails.pop(0)
      emailFile.close()
    
    #get the array of tuple and convert it to array of string urls
    #get the url thats starts with "http/https"
    #strip the "http/https" and make it start with "www."
    while len(urlht) and (readExtractedFile == "Y" or readExtractedFile == "y"):
      tupleUrl = urlht.pop(0)
      if tupleUrl != "\n":
        fulUrl = tupleUrl[1] + tupleUrl[2]
        fulUrl = fulUrl.strip()
        wwwRegList.append(fulUrl)
 
    #open extracted.txt
    extractedFile = open("extrated.txt", 'a')

    #get the array of tuple and convert it to array of string urls
    #get the url thats starts with 'www'
    #Compare with the ones that start with "http/https"(already stripped)
    #this is because urls that start with "http/https" can also exist in "www." urls
    while len(regTuple) and (readExtractedFile == "Y" or readExtractedFile == "y"):    
      tupleUrl = regTuple.pop(0)  
      fulUrl = tupleUrl[0] + '.' + tupleUrl[1] + tupleUrl[2]
      fulUrl = fulUrl.strip()
  
      if fulUrl not in wwwRegList:
        if fulUrl not in extracted_urls:
          extracted_urls.append(fulUrl)
          extractedFile.write(fulUrl + "\n")
          if parseUrl(fulUrl):                     
            filteredFile = open("specialAttFilter.txt", 'a')
            filteredFile.write(fulUrl + "\n")
            filteredFile.close()
          else:
            specialAtt = open("specialAtt.txt", 'a')
            specialAtt.write(fulUrl + "\n")
            specialAtt.close()
          
    #Compare regex extracted urls vs bs extracted urls (http(s) vs http(s))
    while len(wwwRegTuple) and (readExtractedFile == "Y" or readExtractedFile == "y"):
      tupleUrl = wwwRegTuple.pop(0)
      fulUrl = tupleUrl[0] + '://' + tupleUrl[1] + tupleUrl[2]
      fulUrl = fulUrl.strip()

      #save urls(http:// | https:// www.url.com) file
      if fulUrl not in extracted_urls: 
        extracted_urls.append(fulUrl)
        extractedFile.write(fulUrl + "\n")
        if parseUrl(fulUrl):                     
          filteredFile = open("specialAttFilter.txt", 'a')
          filteredFile.write(fulUrl + "\n")
          filteredFile.close()
        else:
          specialAtt = open("specialAtt.txt", 'a')
          specialAtt.write(fulUrl + "\n")
          specialAtt.close()

    extractedFile.close()

##################################################################################
#updateWaitList - Check wait list for due timers
##################################################################################
def updateWaitList():    
    arraylen = len(waiting)  
    count = 0  
    
    while count < arraylen:      
      currentTime = datetime.datetime.now()
      count = count + 1

      if currentTime >= expTime[0]:
        waiting.pop(0)
        expTime.pop(0)
      else:
        break            

##################################################################################    
#htmlPageRead - process url and extract new urls and emails
##################################################################################
def htmlPageRead(url,base_url):
    excpt = ""

    try:             
      headers = { 'User-Agent' : headerList[random.randrange(0, 9)]}
      request = urllib.request.Request(url, None, headers)
      response = urllib.request.urlopen(request, timeout=20)
      urlText = response.read()         
      
    except error as e:
        print("\t" + str(e))
        print("\tmoving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write(str(e) + "\n" + url + "\n\n")                     
        exceptFile.close()
        urlText = ""

    except timeout:
      excpt = "timeout"

    except:
      excpt = "unk"
        
    if excpt != "":
        print("\t" + excpt + "\tmoving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write("\t" + excpt + "\n" + url + "\n\n")                     
        exceptFile.close() 
        urlText = ""

    # create a beautiful soup for the html document
    if urlText != "":
      soup = BeautifulSoup(urlText, 'lxml')

      if (readExtractedFile == "Y" or readExtractedFile == "y"):
        extractedFile = open("extrated.txt", 'a')
    
      #Open url.txt file and append urls
      urlFile = open("url.txt", 'a')    
      urlFilterFile = open("urlFilter.txt", 'a')
      urlEmailFile = open("urlEmail.txt", 'a')

      #check for urls with bs4
      for anchor in soup.find_all("a"):
          # extract link url from the anchor and look email links that could be in url form        
          link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") ==-1 and anchor.attrs["href"].find("tel") ==-1 and anchor.attrs["href"].find("@") ==-1 and anchor.attrs["href"].find("mail.") ==-1  else ''
          link = link.strip()
          link = link.strip('\'"')
          
          newLink = str(anchor.get('href'))
          newLink = newLink.strip()
          if link == '' and newLink != 'None' and newLink.find("mailto:") !=-1 and newLink.find("@") !=-1 and not newLink.startswith('#'):                      
            print("\tPossible url email, moving url to urlEmail.txt")
            urlEmailFile.write(newLink + '\n')           

          # resolve relative links
          if link.startswith('/'):
            link = base_url + link
          elif link.startswith('#'):
            link = link.strip('#')
            if link != "":
              link = base_url + link

          if link != "" and not link.startswith('http'):
            if not link.startswith('https'):
              link = path + link 

          if (readExtractedFile == "Y" or readExtractedFile == "y") and link != "" and link not in extracted_urls:
            if parseUrl(link):
              print("\tmoving to urlFilter.txt")
              urlFilterFile.write(link + "\n")               
            else: 
              print("\tmoving to url.txt")                         
              urlFile.write(link + "\n") #temporary storage          
            extracted_urls.append(link)
            extractedFile.write(link + "\n") #permananent storage    

          elif (readExtractedFile == "Y" or readExtractedFile == "y") and link != "":   
            print("\turl already extracted")
          
      #Close url files
      urlFile.close()      
      urlFilterFile.close()
      urlEmailFile.close()

      if (readExtractedFile == "Y" or readExtractedFile == "y"):
        extractedFile.close()

      #Extract email and url using regex
      regexExtract(urlText, url)         

    #This will run only once in the program, 
    #delete processed.txt before using it for the new program
    global readProcPrimer 
    if os.stat("processed.txt").st_size != 0 and readProcPrimer == 1:
      readProcPrimer = 0      
      procUrlFile = open("processed.txt", 'w')
      procUrlFile.write("")
      procUrlFile.close
    
    #Save processed urls to file
    procUrlFile = open("processed.txt", 'a')
    procUrlFile.write(url + "\n")
    procUrlFile.close()   
    
    #increment number of processed urls
    global numOfProcessedUrl
    numOfProcessedUrl = numOfProcessedUrl + 1 
    print('\tProcessed urls = ',numOfProcessedUrl)

##################################################################################    
#Program start
##################################################################################

#get numOfUrlToProc from user
if (getInst == "U" or getInst == "u"):  
  numOfUrlToProc = int(input("Enter number of urls you intend to process: "))
  checkRobot = input("\nWould you like robot.txt to parse your urls, hit y for yes : ")
  delay = input("\nWould you to use delay option, hit y for yes : ")
  readExtractedFile = input("\nWould you to read and write to extracted and email file , hit y for yes : ")

#read the extrated.txt file and append to array
if (readExtractedFile == "Y" or readExtractedFile == "y") and os.stat("extrated.txt").st_size != 0 and (numOfUrlToProc < 1 or (getInst == "U" or getInst == "u") or (getInst == "F" or getInst == "f")):  
  extractedFile = open("extrated.txt", 'r')
  print("Reading extrated.txt file")
  for urlExt in extractedFile.readlines():
    urlExt = urlExt.strip()
    if urlExt != "\n":    
      extracted_urls.append(urlExt)
  extractedFile.close() 

#read email file and append to array
if (readExtractedFile == "Y" or readExtractedFile == "y") and os.stat("emails.txt").st_size != 0 and (numOfUrlToProc < 1 or (getInst == "U" or getInst == "u") or (getInst == "F" or getInst == "f")):    
    print("Reading emails.txt file")
    emailFile = open("emails.txt", 'r')
    for emailExt in emailFile.readlines(): 
      if '.png' not in emailExt and '.PNG' not in emailExt and '.jpg' not in emailExt and '.JPEG' not in emailExt and '.jpeg' not in emailExt and '.amazon' not in emailExt:
        emailExt = emailExt.strip()     
        if emailExt != "\n" :              
          emails.append(emailExt)
    emailFile.close()   

#Filter .png .jpg
#emailFile = open("emails.txt", 'w')
#emailFile.write("")
#emailFile.close()
#emailFile = open("emails.txt", 'a')

#while len(emails):   
#  emailFile.write(emails.pop() + "\n")

#emailFile.close() 
#exit(0)

#loop program
while numOfProcessedUrl < numOfUrlToProc and os.stat("url.txt").st_size != 0 and (getInst == "U" or getInst == "u"): 
  #runtime.txt, for storing runtime urls
  #these urls are read into array, any interuption = data loss 
  if os.stat("runtime.txt").st_size != 0:
    runTimeFile = open("runtime.txt", 'w')
    runTimeFile.write("")
    runTimeFile.close()

  urlFile = open("url.txt", 'r')
  runTimeFile = open("runtime.txt", 'a')

  for urlLink in urlFile.readlines():
    urlLink = urlLink.strip('\'"')
    if urlLink != "\n":      
      new_urls.append(urlLink)
      runTimeFile.write(urlLink + "\n")

  urlFile.close() 
  runTimeFile.close()

  #Empty the url.txt file
  urlFile = open("url.txt", 'w')
  urlFile.write("")  
  urlFile.close()
  
  #Process the urls
  #If file is not empty
  while len(new_urls) and numOfProcessedUrl < numOfUrlToProc:    
    #Read a url and remove it from the array
    url = new_urls.pop() 
    url = url.strip()  
      
    if parseUrl(url) :
      specialAtt = open("specialAtt.txt", 'a')
      specialAtt.write(url + "\n")
      specialAtt.close()
      url = ""

    if url != "" or url != "\n":
      # extract base url to resolve relative links &  
      print("Processing %s" % url)   
      parts = urlsplit(url)
      base_url = "{0.scheme}://{0.netloc}".format(parts)
      robot_url = "{0.scheme}://{0.netloc}/robots.txt".format(parts)   
      path = url[:url.rfind('/')+1] if '/' in parts.path else url

    #if the website is already in waiting list
    #Move the url to the last queue
    if url != "" and (delay == 'y' or delay == 'Y'):   
      if base_url in waiting:
        print('\n url domain in waiting list')   
        urlFile = open("url.txt", 'a')
        urlFile.write(url + "\n")
        urlFile.close()
        url = ""
        
    #Check for robots.txt
    #Handle possible network error, this is the first url request
    if url != "" and (checkRobot == "y" or checkRobot == "Y"):
      try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robot_url)
        rp.read()
      
      except error as e:
        print("\t" + str(e))
        print("\tmoving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write("\t" + str(e) + "\n" + url + "\n\n")                     
        exceptFile.close()
        url = "" 

      except:        
        print("\tunk \tmoving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write("\tunk \n" + url + "\n\n")                     
        exceptFile.close()
        url = "" 

      #if crawling is not allowed in the website
      #move the url to robots.txt and robotArray(for easy parsing)
      if not rp.can_fetch("*", base_url) and url:
        if url != "\n":
          print("\tAdding url to robot.txt")
          robotFile = open("robot.txt", 'a')
          robotFile.write(url + "\n")
          robot.append(url)         
          robotFile.close()
          url = "" 

    if url != "":
      htmlPageRead(url,base_url)
      if (delay == 'y' or delay == 'Y'):
        waitList(base_url)
  
  #this will not work if delay != y because waiting list will be empty
  if len(waiting) and (delay == 'y' or delay == 'Y'):
    updateWaitList()

#process file option
if (getInst == "F" or getInst == "f"):     
    #Open url.txt file and append urls
    copiedFile = open("search.html", 'r')
    searchUrlFile = open("searchUrlFile.txt", 'a')
    slashFile = open("searchSpecialAtt.txt", 'a')
    extractedFile = open("extrated.txt", 'a')
    searchUrlEmailFile = open("searchUrlEmail.txt", 'a')
    
    # create a beautiful soup for the html document
    soup = BeautifulSoup(copiedFile, 'lxml')
    
    for anchor in soup.find_all("a"): 
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") ==-1 and anchor.attrs["href"].find("tel") ==-1 and anchor.attrs["href"].find("@") ==-1 and anchor.attrs["href"].find("mail.") ==-1  else ''
        link = link.strip()
        link = link.strip('\'"')

        newLink = str(anchor.get('href'))
        newLink = newLink.strip()
        if link == '' and newLink != 'None' and newLink.find("@") !=-1 and not newLink.startswith('#'):                      
          print("\tPossible url email, moving url to searchUrlEmail.txt")
          searchUrlEmailFile.write(newLink + '\n')

        # resolve relative links
        if link.startswith('/') or link.startswith('#'):
          slashFile.write(newLink + "\n")
          link = ""
        if link != "" and not link.startswith('http'):
          if not link.startswith('https'):
            #link = "http://" + link  #could be https, but http should work in both place
            slashFile.write(link + "\n")
            link = ""
        if link != "" and link not in extracted_urls:
          extracted_urls.append(link)
          searchUrlFile.write(link + "\n")
          extractedFile.write(link + "\n")                

    #Close files    
    searchUrlFile.close()
    extractedFile.close()
    slashFile.close()
    copiedFile.close()
    searchUrlEmailFile.close()

    copiedFile = open("search.html", 'r')
    emlStr = copiedFile.read()
    copiedFile.close()
         
    #extract emails and urls with regex
    regexExtract(emlStr, "")


elif (getInst != "U" or getInst != "u") and (numOfUrlToProc == 0):
  print("Invalid option..F for file, U for web urls")

#if new url array is not empty, append the urls to url.txt file
if len(new_urls) or os.stat("runtime.txt").st_size != 0:
  urlFile = open("url.txt", 'a')
  while len(new_urls):
    urlFile.write(new_urls.pop(0))
  urlFile.close()

  if os.stat("runtime.txt").st_size != 0:
    runTimeFile = open("runtime.txt", 'w')
    runTimeFile.write("")
    runTimeFile.close()  

if (numOfProcessedUrl < numOfUrlToProc) and (os.stat("url.txt").st_size == 0) and (getInst == "U" or getInst == "u"):
  print("process didn't complete because url.txt file is empty")
elif (numOfUrlToProc == 0) and (os.stat("search.html").st_size == 0) and (getInst == "F" or getInst == "f"):
  print("process didn't complete because search.html file is empty")
else:
  print("process completed")

exit(0)