import os
from threading import Thread

# https://www.parabol.co/

def fun1(url):
    os.system("start cmd /k python ./dirsearch/dirsearch.py -u {} -e php -b".format(url))

def fun2(url):
    modurl = url.split('www.',1)[1]

    if '/' in modurl:
        modurl = modurl.split('/',1)[0]
    
    os.system("start cmd /k python ./Sublist3r/sublist3r.py -d {} -t 50".format(modurl))

if __name__ =='__main__':
    print('Enter URL:')
    url = input()
    
    Thread(target = fun1,args=(url,)).start()
    Thread(target = fun2,args=(url,)).start()

