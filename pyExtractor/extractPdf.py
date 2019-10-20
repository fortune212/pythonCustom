#python 2.7
#pdf reader

import PyPDF2, os
import requests
import requests.exceptions
import re
import codecs

# a set of crawled emails
emails = []

#for extracted urls
extraced_urls = []

#read the extrated.txt file and append to array
if os.stat("extrated.txt").st_size != 0:
  extratedFile = open("extrated.txt", 'r')
  print("Reading extrated.txt file")
  for urlExt in extratedFile.readlines():
    urlExt = urlExt.strip()
    if urlExt != "\n":    
      extraced_urls.append(urlExt)
  extratedFile.close() 

#read email file and append to array
if os.stat("emails.txt").st_size != 0:    
    print("Reading emails.txt file")
    emailFile = open("emails.txt", 'r')
    for emailExt in emailFile.readlines(): 
      emailExt = emailExt.strip()     
      if emailExt != "\n" :              
        emails.append(emailExt)
    emailFile.close()    


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
                    elif "video" in urlStr:    
                      url = True
                    elif "Video" in urlStr:    
                      url = True
                    elif ".pdf" in urlStr:    
                      url = True
                    elif ".zip" in urlStr:    
                      url = True
                    elif ".mp" in urlStr:    
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

                    elif "tumblr.com" in urlStr:    
                      url = True

                    return url               

##################################################################################
#extractPdf - Extract pdf file
##################################################################################
def extractPdf(pdfUrl):

  #Add header file
  
  response = requests.get(pdfUrl, stream = True) 
  #response = requests.get(pdfUrl)
  
  #wb(write binary) into a file
  #with open("python.pdf","wb") as pdfFileObj: 
    #for chunk in r.iter_content(chunk_size=1024): 
         # writing one chunk at a time to pdf file 
         #if chunk: 
             #pdfFileObj.content(chunk) 

  #with open('python.pdf', 'wb') as pdfFileObj:
    #pdfFileObj.write(response.content)
    #for chunk in response.iter_content(chunk_size=1024):
      #if chunk:
        #pdfFileObj.write(response.content)
    #pdfFileObj.close()

  with codecs.open('python.pdf', 'wb', encoding='utf8') as pdfFileObj:
    pdfFileObj.write(response.content)

  pdfFileObj.close()
  
  pdfFileObj = open("python.pdf","rb")

  # creating a pdf reader object 
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
  # printing number of pages in pdf file 
  #print(pdfReader.numPages) 
  
  # creating a page object 
  pageObj = pdfReader.getPage(0) 
  
  # extracting text from page 
  text = pageObj.extractText()
  parsePdf(text) 
  
  # closing the pdf file object 
  pdfFileObj.close() 

##################################################################################
#parsePdf - Extract urls and emails in pdf file using regex
##################################################################################
def parsePdf(urlText):
  try:
      wwwRegList = []
      #if data is not string, try decoding, else error(except)
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
      
    print("\t problem with pdf email extraction")               

    #save to file
    #open email.txt and append
    if len(new_emails):
      emailFile = open("pdfEmails.txt", 'a') 
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
  
      if fulUrl not in wwwRegList:
        if fulUrl not in extraced_urls:
          if parseUrl(fulUrl):                     
            filteredFile = open("pdfUrlFilter.txt", 'a')
            filteredFile.write(fulUrl + "\n")
            filteredFile.close()
          else:
            specialAtt = open("pdfUrl.txt", 'a')
            specialAtt.write(fulUrl + "\n")
            specialAtt.close()
          
    #Compare regex extracted urls vs bs extracted urls (http(s) vs http(s))
    while len(wwwRegTuple):  
      tupleUrl = wwwRegTuple.pop(0)
      fulUrl = tupleUrl[0] + '://' + tupleUrl[1] + tupleUrl[2]
      fulUrl = fulUrl.strip()

      #save urls(http:// | https:// www.url.com) file
      if fulUrl not in extraced_urls: 
        if parseUrl(fulUrl):                     
          filteredFile = open("pdfUrlFilter.txt", 'a')
          filteredFile.write(fulUrl + "\n")
          filteredFile.close()
        else:
          specialAtt = open("pdfUrl.txt", 'a')
          specialAtt.write(fulUrl + "\n")
          specialAtt.close()

##################################################################################    
#Program start
##################################################################################
pdfUrl = 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf'
extractPdf(pdfUrl)