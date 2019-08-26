from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
#from collections import deque
import re
import urllib.robotparser
import random
import datetime
import os
import time

from socket import error
import errno

numOfProcessedUrl = 0
numOfUrlToProc = 0

# a set of crawled emails
emails = []

#Read url from file
new_urls = []

#for extracted urls
extraced_urls = []

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

getInst = input("What kind of file do you want to extract. \n\t hit 'U' for web urls or 'F' for local file(search.html) : ")

readProcPrimer = 1

#Wait list
#Add 3 mins wait for each domain
def waitList(base_url):
  now = datetime.datetime.now()
  twoMin = now.minute + 3

  print("\t process successful")

  #minute cannot be greater than 59, 
  if twoMin < 59:
    exTime = now.replace(minute = twoMin)
    waiting.append(base_url)
    expTime.append(exTime)
    print("\t wait (wait url domain) \n")
    updateWaitList()
  else:
    print("\t sleep 30 (delay url domain) \n")
    time.sleep(30)

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

#extract urls and emails using regex
def regexExtract(urlText, url):
    #Use regex to extract url and emails      
    #Return a list of extracted emails and urls(array)
    #possible error
    #urlText should be a string(utf-8) else(error), 
    #It could be binary or non utf-8 string (iso-notString)    
    try:
      if type(urlText) != str:
        urlText = urlText.decode()
      new_emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urlText, re.I)
      urlht = re.findall(r"(http|ftp|ftps|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
      wwwRegTuple = re.findall(r"(http|ftp|ftps|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
      regTuple = re.findall(r"(www).([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
          
    except:      
      #assign arrays, it could be called below
      new_emails = []
      urlht = []
      wwwRegTuple = []
      regTuple = []
      urlText = ""
      
      if url != "":
        #save url to file
        print("\t problem with email extraction, moving url to extProb.txt")
        contNotStrFile = open("extProb.txt", 'a')
        contNotStrFile.write(url + "\n")
        contNotStrFile.close() 
      else:
        print("\t problem with email extraction")               

    #save to file
    #open email.txt and append
    if len(new_emails):
      emailFile = open("emails.txt", 'a') 
      while len(new_emails):
          if new_emails[0] not in emails:
            get_email = new_emails.pop(0)
            emails.append(get_email)  
            emailFile.write(get_email + "\n")
          else:
            new_emails.pop(0)
      emailFile.close()
    
    #get the array of tuple and convert it to array of string urls
    #get the url thats starts with "http/https"
    #strip the "http/https" and make it start with "www."
    while len(urlht):
      tupleUrl = urlht.pop(0)
      if tupleUrl != "\n":
        fulUrl = tupleUrl[1] + tupleUrl[2]
        fulUrl = fulUrl.strip()
        wwwRegList.append(fulUrl)

    #get the array of tuple and convert it to array of string urls
    #get the url thats starts with 'www'
    #Compare with the ones that start with "http/https"(already stripped)
    #this is because urls that start with "http/https" can also exist in "www." urls
    while len(regTuple):    
      tupleUrl = regTuple.pop(0)  
      fulUrl = tupleUrl[0] + '.' + tupleUrl[1] + tupleUrl[2]
      fulUrl = fulUrl.strip()
  
      if (fulUrl + "\n") not in wwwRegList:
        if (fulUrl + "\n") not in extraced_urls:
          if parseUrl(fulUrl):                     
            filteredFile = open("specialAttFilter.txt", 'a')
            filteredFile.write(fulUrl + "\n")
            filteredFile.close()
          else:
            specialAtt = open("specialAtt.txt", 'a')
            specialAtt.write(fulUrl + "\n")
            specialAtt.close()
          
    #Compare regex extracted urls vs bs extracted urls (http(s) vs http(s))
    while len(wwwRegTuple):  
      tupleUrl = wwwRegTuple.pop(0)
      fulUrl = tupleUrl[0] + '://' + tupleUrl[1] + tupleUrl[2]
      fulUrl = fulUrl.strip()

      #save urls(http:// | https:// www.url.com) file
      if (fulUrl + "\n") not in extraced_urls: 
        if parseUrl(fulUrl):                     
          filteredFile = open("specialAttFilter.txt", 'a')
          filteredFile.write(fulUrl + "\n")
          filteredFile.close()
        else:
          specialAtt = open("specialAtt.txt", 'a')
          specialAtt.write(fulUrl + "\n")
          specialAtt.close()

#Check wait list for due timers
#current time shouldnt be greater than that time
#trying printing the times, to get be sure
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
            
#process url and extract new urls and emails
#if request doesnt work(maybe bad network),
#try again, if it doesnt work again, 
#save the url to file and assign empty string to urltext
def htmlPageRead(url,base_url):
    try:             
      headers = { 'User-Agent' : headerList[random.randrange(0, 9)]}
      request = urllib.request.Request(url, None, headers)
      response = urllib.request.urlopen(request)
      urlText = response.read()                      
      
    except error as e:
        print("\t" + str(e))
        print("\t moving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write(str(e) + "\n" + url + "\n\n")                     
        exceptFile.close()
        urlText = ""

    except:
        print(e)
        print("\t moving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write(str(e) + "\n" + url + "\n\n")                     
        exceptFile.close()
        urlText = ""

    # create a beutiful soup for the html document
    if urlText != "":
      soup = BeautifulSoup(urlText, 'lxml')
    
      #Open url.txt file and append urls
      urlFile = open("url.txt", 'a') 
      extratedFile = open("extrated.txt", 'a')    
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
          if link == '' and newLink != 'None' and newLink.find("@") !=-1 and not newLink.startswith('#'):                      
            print("\t Possible url email, moving url to urlEmail.txt")
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

          if link != "" and link not in extraced_urls:
            if parseUrl(link):
              urlFilterFile.write(link + "\n")               
            else:            
              extraced_urls.append(link)
              urlFile.write(link + "\n") #temporary storage
              extratedFile.write(link + "\n") #permananent storage       
          
      #Close url files
      urlFile.close()
      extratedFile.close()
      urlFilterFile.close()
      urlEmailFile.close()

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

##################################################################################    
#Program start
##################################################################################

#get numOfUrlToProc from user
if (getInst == "U" or getInst == "u"):  
  numOfUrlToProc = int(input("Enter number of urls you intend to process: "))
  checkRobot = input("\nWould you like robot.txt to parse your urls, hit y for yes : ")
  delay = input("\nWould you to use delay option, hit y for yes : ")

#read the extrated.txt file and append to array
if os.stat("extrated.txt").st_size != 0 and (numOfUrlToProc < 1 or (getInst == "U" or getInst == "u") or (getInst == "F" or getInst == "f")):  
  extratedFile = open("extrated.txt", 'r')
  print("Reading extrated.txt file")
  for urlExt in extratedFile.readlines():
   if urlExt != "\n":
    urlExt = urlExt.strip()
    extraced_urls.append(urlExt)
  extratedFile.close() 

#read email file and append to array
if os.stat("emails.txt").st_size != 0 and (numOfUrlToProc < 1 or (getInst == "U" or getInst == "u") or (getInst == "F" or getInst == "f")):    
    print("Reading emails.txt file")
    emailFile = open("emails.txt", 'r')
    for emailExt in emailFile.readlines():      
      if emailExt != "\n" :
        emailExt = emailExt.strip()      
        emails.append(emailExt)
    emailFile.close()    
  
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
    if urlLink != "\n":
      urlLink = urlLink.strip('\'"')
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

    print("Processing %s" % url)   

    if url != "" or url != "\n":
      # extract base url to resolve relative links &    
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
        print("\t moving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write("\t" + str(e) + "\n" + url + "\n\n")                     
        exceptFile.close()
        url = "" 

      except:        
        print("\t moving to exception.txt")
        exceptFile = open("exception.txt", 'a')        
        exceptFile.write("\t" + str(e) + "\n" + url + "\n\n")                     
        exceptFile.close()
        url = "" 

      #if crawling is not allowed in the website
      #move the url to robots.txt and robotArray(for easy parsing)
      if not rp.can_fetch("*", base_url) and url:
        if url != "\n":
          print("\t Adding url to robot.txt")
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
    slashFile = open("fileSpecial.txt", 'a')
    extratedFile = open("extrated.txt", 'a')
    fileUrlEmailFile = open("fileUrlEmail.txt", 'a')
    
    # create a beutiful soup for the html document
    soup = BeautifulSoup(copiedFile, 'lxml')
    
    for anchor in soup.find_all("a"): 
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") ==-1 and anchor.attrs["href"].find("tel") ==-1 and anchor.attrs["href"].find("@") ==-1 and anchor.attrs["href"].find("mail.") ==-1  else ''
        link = link.strip()
        link = link.strip('\'"')

        newLink = str(anchor.get('href'))
        newLink = newLink.strip()
        if link == '' and newLink != 'None' and not newLink.startswith('#'):                      
          print("\t Possible url email, moving url to fileUrlEmail.txt")
          fileUrlEmailFile.write(newLink + '\n')

        # resolve relative links
        if link.startswith('/') or link.startswith('#'):
          slashFile.write(newLink + "\n")
          link = ""
        if link != "" and not link.startswith('http'):
          if not link.startswith('https'):
            #link = "http://" + link  #could be https, but http should work in both place
            slashFile.write(link + "\n")
            link = ""
        if link != "" and link not in extraced_urls:
          extraced_urls.append(link)
          searchUrlFile.write(link + "\n")
          extratedFile.write(link + "\n")                

    #Close files    
    searchUrlFile.close()
    extratedFile.close()
    slashFile.close()
    copiedFile.close()
    fileUrlEmailFile.close()

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