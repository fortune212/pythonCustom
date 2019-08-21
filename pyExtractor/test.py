def htmlPageRead(url,base_url):
    try:             
      headers = { 'User-Agent' : headerList[random.randrange(0, 9)]}
      request = urllib.request.get(url=url, headers=headers, verify=False)
      response = urllib.request.urlopen(request)      
      urlHtmlPageRead = response.read()
      urlText = urlHtmlPageRead.decode()     

      print("Processing %s" % url)

      #search for emails
      new_emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urlText, re.I)

    except type(urlText) != str:
        #save url to file
        specialAtt = open("specialAtt.txt", 'a')
        specialAtt.write(url + "\n")
        specialAtt.close()

      #save email to file
      #open email.txt and append
      if len(new_emails):
        emailFile = open("emails.txt", 'a') 
        while len(new_emails) and new_emails[0] not in emails:
          get_email = new_emails.pop(0)
          emails.append(get_email)  
          emailFile.write(get_email + "\n")                     
        emailFile.close()
       
      #for urls with regex (urlht = wwwRegTuple)
      urlht = re.findall(r"(http|ftp|ftps|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
      wwwRegTuple = re.findall(r"(http|ftp|ftps|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)
      regTuple = re.findall(r"(www).([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", urlText, re.I)

      #get the array of tuple and convert it to array of string urls
      while len(urlht):
        tupleUrl = urlht.pop(0)
        fulUrl = tupleUrl[1] + tupleUrl[2]
        fulUrl = fulUrl.strip()
        wwwRegList.append(fulUrl)

      #check for www. url in wwwRegList
      while len(regTuple):    
        tupleUrl = regTuple.pop(0)  
        fulUrl = tupleUrl[0] + '.' + tupleUrl[1] + tupleUrl[2]
        fulUrl = fulUrl.strip()
  
        #save urls(www.url.com) file
        if fulUrl not in wwwRegList:   
          specialAtt = open("specialAtt.txt", 'a')
          specialAtt.write(fulUrl + "\n")
          specialAtt.close()

      # create a beutiful soup for the html document
      soup = BeautifulSoup(urlText, 'lxml')
    
      #Open url.txt file and append urls
      urlFile = open("url.txt", 'a') 
      extratedFile = open("extrated.txt", 'a')   

      #check for urls with bs4
      for anchor in soup.find_all("a"): 
          # extract link url from the anchor
          link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") ==-1 and anchor.attrs["href"].find("tel") ==-1 and anchor.attrs["href"].find("#") ==-1  else ''
          link = link.strip()
          link = link.strip('\'"')

          # resolve relative links
          if link.startswith('/'):
            link = base_url + link
          if not link.startswith('http'):
            if not link.startswith('https'):
              link = path + link 

          if link not in extraced_urls:
            extraced_urls.append(link)
            urlFile.write(link + "\n") #temporary storage
            extratedFile.write(link + "\n") #permananent storage
        
      #Close files
      urlFile.close()
      extratedFile.close()

      #increment number of processed urls
      global numOfProcessedUrl
      numOfProcessedUrl = numOfProcessedUrl + 1

      while len(wwwRegTuple):  
        tupleUrl = wwwRegTuple.pop(0)
        fulUrl = tupleUrl[0] + '://' + tupleUrl[1] + tupleUrl[2]
        fulUrl = fulUrl.strip()

        #save urls(http:// | https:// www.url.com) file
        if fulUrl not in extraced_urls:   
          specialAtt = open("specialAtt.txt", 'a')
          specialAtt.write(fulUrl + "\n")
          specialAtt.close()        

#This function can only return the following errors(except)
  #string ref b4 assignment 
  #error 404 

#call it, if error 404, check google cache, else save url in a file and process nothing
#if string error, try again, then save url in a file and process nothing

def urlLeech(url,base_url):
    try:
        htmlPageRead(url,base_url)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            try:
              url = 'http://webcache.googleusercontent.com/search?q=cache:'+url
              htmlPageRead(url, base_url)
            except:
              #save url to file
              specialAtt = open("specialAtt.txt", 'a')
              specialAtt.write(url + "\n")
              specialAtt.close()
        else:
          #save url to file
          specialAtt = open("specialAtt.txt", 'a')
          specialAtt.write(url + "\n")
          specialAtt.close()    