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
          if link == '' and not newLink.startswith('#'):                        
            print("\t Possible url email, moving url to urlEmail.txt")
            urlEmailFile.write(newLink + '\n')           

          # resolve relative links
          if link.startswith('/'):
            link = base_url + link
          elif link.startswith('#'):
            link = link.strip('#')
            link = base_url + link

          if not link.startswith('http'):
            if not link.startswith('https'):
              link = path + link 

          if link not in extraced_urls:
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

def regexExtract(urlText):
    #Use regex to extract url and emails      
    #Return a list of extracted emails and urls(array)
    #possible error
    #urlText should be a string(utf-8) else(error), 
    #It could be binary or non utf-8 string (iso-notString)
    try:
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
      
      #save url to file
      print("\t problem with email extraction, moving url to extProb.txt")
      contNotStrFile = open("extProb.txt", 'a')
      contNotStrFile.write(url + "\n")
      contNotStrFile.close()                

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
