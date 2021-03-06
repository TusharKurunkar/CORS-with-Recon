import os
import json
from threading import Thread
from flask import Flask,render_template

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
    os.system("curl {} -I -H origin:{} > {}.txt ".format(url,origin,modurl))
    
    dic=fileconv(modurl)
    # check for exploitable case 1 conditions.
    status_code=int(dic.get('HTTP/1.1')[0])
    if status_code>=200 and status_code<300:
        if 'Link:' in dic.keys() or ('Access-Control-Allow-Origin:' in dic.keys() and 'Access-Control-Allow-Credentials:' in dic.keys()):

            if 'Link:' in dic.keys() or (dic.get('Access-Control-Allow-Origin:')[0] == origin and dic.get('Access-Control-Allow-Credentials:')[0] == 'true'):

                if 'Link:' in dic.keys():

                    s=dic.get('Link:')[0]
                    l1=s.split(';',1)[0]
                    l1=l1.split('<',1)[1]
                    l1=l1.split('>',1)[0]

                    print('Case 1 Possible.The entered domain is subject to exploitation.')

                    # flask route
                    @app.route('/')
                    def case1():
                        return render_template('CORS.html', link=l1)

                else:
                    print('Case 1 Not Possible.Do You Want to check for Case 2?(yes/no)')
                    choice = input()
                    # yes
                    if choice.lower()=='yes':
                        fun3_case2(url,modurl)
                    elif choice.lower()=='no':
                        print('Okay,Thank you!')
                    else:
                        print('Please give a valid input.')
            else:
                print('The given URL is not vulnerable to CORS')
    elif status_code>=300:
        print('Not Applicable becauce of {} status code.'.format(status_code))
    else:
        print('The given URL is not vulnerable to CORS')
    
# end of function fun3()

# start of function fun_case2()
def fun3_case2(url,modurl):
    print('Enter Origin:')
    # Here,origin is local variable for fun_case2() and its different from __main__
    origin = input()

    os.system("curl {} -I -H origin:{} > {}.txt ".format(url, origin, modurl))
    
    dic=fileconv(modurl)

    if 'Access-Control-Allow-Origin:' in dic.keys() and 'Access-Control-Allow-Credentials:' in dic.keys():
        
        if dic.get('Access-Control-Allow-Origin:')[0] == origin and dic.get('Access-Control-Allow-Credentials:')[0]=='true':
            print('Please visit. http://127.0.0.1:5000/case2')
            
            @app.route('/case2')
            def case2():
                return render_template('home.html',message='Case 2 is successful,The given url is subject to exploitation,but you have to purchase the domain.')
        
        else:
            print('Given url is not vulnerable.')
            
    else:
        print('Case 2 also fails.The given domain is not vulnerable to exploitation.')

# end of function fun_case2()

def fileconv(modurl):

    dict1={}

    with open("{}.txt".format(modurl)) as f:
        for line in f:
            if line.strip():  # non-empty line?
                key, value = line.split(None, 1)  # None means 'all whitespace', the default
                if 'Link:' in dict1.keys() and key == 'Link:':
                    key = 'Link1:'
                dict1[key] = value.split()

    # creating json file 
    # the JSON file is named as {modurl_response} 
    out_file = open("{}_response.json".format(modurl), "w") 
    json.dump(dict1, out_file, indent = 4, sort_keys = False) 
    out_file.close()

    # opens the json file in variable f,and json.load the f into dic variable
    f= open('{}_response.json'.format(modurl))
    dic = json.load(f)

    f.close()

    return dic

if __name__ =='__main__':
    print('Enter URL:')
    url = input()
    print('Enter Origin:')
    origin = input()


    if 'www.' in url or 'api.' in url:
        if 'www.' in url:
            modurl = url.split('www.',1)[1]
        elif 'api.' in url:
            modurl = url.split('api.',1)[1]
    elif 'www.' not in url:
        if 'http' in url or 'https' in url:
            modurl = url.split('://',1)[1]
        else:
            print('Invalid URL.Please Try Entering A Valid URL.')
    
    Thread(target = fun1,args=(url,)).start()
    Thread(target = fun2,args=(modurl,)).start()
    fun3(url,modurl,origin)
    # Tells the flask app to run.Nescessary when using Flask.
    app.run()