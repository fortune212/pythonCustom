urlArray = []

urlEmfile = open("filterMailTo.txt", 'a')
#urlFile = open("urlEmail.txt", 'r')
urlFile = open("emails.txt", 'r')

for url in urlFile.readlines():
   url = url.strip()
   url = url.lstrip('mailto:')
   if url != "\n" and (url + "\n") not in urlArray:     
     urlArray.append(url + "\n")
     urlEmfile.write(url + "\n")

urlFile.close() 
urlEmfile.close()
