import os
import json
from threading import Thread
from flask import Flask,render_template

# https://www.parabol.co/
# https://www.oyorooms.com/

# curl https://www.007.com/wp-json/ -I -H origin:https://www.hacktify.in/
# Flask constructor initializor that says this main.py file works as a flask app
app = Flask(__name__)

# start of function fun1()
def fun1(url):
    os.system("start cmd /k python ./dirsearch/dirsearch.py -u {} -e php -b".format(url))
# end of function fun1()

# start of function fun2()
def fun2(modurl):

    if '/' in modurl:
        modurl = modurl.split('/',1)[0]
    
    os.system("start cmd /k python ./Sublist3r/sublist3r.py -d {} -t 50".format(modurl))
# end of function fun2()

# start of function fun3()
def fun3(url,modurl,origin):

    modurl = modurl.split('.')[0]
    # os.system("curl {} -I -H origin:{} > {}.txt ".format(url,origin,modurl))
    dict1={}
    # with open("{}.txt".format(modurl)) as fh:
  
    #     for line in fh: 
  
    #     # reads each line and trims of extra spaces  
    #     # and gives only the valid words 
    #         command, description = line.strip().split(None,1)
    #         dict1[command] = description.strip()
    with open("{}.txt".format(modurl)) as f:
        for line in f:
            if line.strip():  # non-empty line?
                key, value = line.split(None, 1)  # None means 'all whitespace', the default
                dict1[key] = value.split()

    # creating json file 
    # the JSON file is named as {modurl_response} 
    out_file = open("{}_response.json".format(modurl), "w") 
    json.dump(dict1, out_file, indent = 4, sort_keys = False) 
    out_file.close()

    # opens the json file in variable f,and json.load the f into dic variable
    f= open('{}_response.json'.format(modurl))
    dic = json.load(f)

    # check for exploitable case 1 conditions.
    if 'Access-Control-Allow-Origin:' and 'Access-Control-Allow-Credentials:' in dic.keys():
        
        if dic.get('Access-Control-Allow-Origin:')[0] == origin and dic.get('Access-Control-Allow-Credentials:')[0]=='true':
            s=dic.get('Link:')[0]
            print(s)
            l1=s.split(';',1)[0]
            l1=l1.split('<',1)[1]
            l1=l1.split('>',1)[0]
            print('Case 1 Possible.The entered domain is subject to exploitation.')
            
            # flask route 
            @app.route('/')
            def index():
                return render_template('CORS.html',link=l1)
        
        else:
            print('Case 1 Not Possible.Do You Want to check for Case 2?(yes/no)')
            choice = input(modurl)
            if choice.lower()=='yes':
                fun3_case2(modurl)
            elif choice.lower()=='no':
                print('Okay,Thank you!')
            else:
                print('Please give a valid input.')
    
    f.close()
# end of function fun3()

# start of function fun_case2()
def fun3_case2(modurl):
    print('Enter Origin:')
    # Here,origin is local variable for fun_case2() and its different from __main__
    origin = input()

    f= open('{}_response.json'.format(modurl))
    dic = json.load(f)

    if 'Access-Control-Allow-Origin:' and 'Access-Control-Allow-Credentials:' in dic.keys():
        
        if dic.get('Access-Control-Allow-Origin:')[0] == origin and dic.get('Access-Control-Allow-Credentials:')[0]=='true':
            print('Case 2 is successful,The given url is subject to exploitation,but you have to purchase the domain.')
        else:
            print('Given url is not vulnerable.')
    else:
        print('Case 2 also fails.The given domain is not vulnerable to exploitation.')

    f.close()
# end of function fun_case2()


if __name__ =='__main__':
    print('Enter URL:')
    url = input()
    print('Enter Origin:')
    origin = input()


    if 'www.' in url:
        modurl = url.split('www.',1)[1]
    else:
        if 'http' or 'https' in url:
            modurl = url.split('://',1)[1]
        else:
            print('Invalid URL.Please Try Entering A Valid URL.')
    
    # Thread(target = fun1,args=(url,)).start()
    # Thread(target = fun2,args=(modurl,)).start()
    # Thread(target = fun3,args=(url,modurl,origin)).start()
    fun3(url,modurl,origin)
    # Tells the flask app to run.Nescessary when using Flask.
    app.run()