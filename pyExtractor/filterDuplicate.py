urlArray = []

urlEmfile = open("filterMailTo.txt", 'a')
#urlFile = open("urlEmail.txt", 'r')
urlFile = open("url.txt", 'r')

for url in urlFile.readlines():
   url = url.strip()
   url = url.lstrip('mailto:')
   if url != "\n" and url not in urlArray:     
     urlArray.append(url)
     urlEmfile.write(url + "\n")

urlFile.close() 
urlEmfile.close()
