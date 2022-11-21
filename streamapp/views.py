 
from os.path import dirname, join
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http.response import StreamingHttpResponse
from streamapp.camera import VideoCamera
from django.template.loader import render_to_string
 
from django.template import loader, Context
from json import dumps 
from django.template.defaulttags import register
from threading import Thread
import requests
 
import os
 
#path='/staticfiles'
cloud_config= {
        'secure_connect_bundle': join(dirname(__file__), "secure-connect-database.zip")
}
#auth_provider = PlainTextAuthProvider('Datauser', 'database@1')
#cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
#session = cluster.connect()
d= {'hi': 'hindi','en': 'english','ta': 'tamil','kn': 'kannada', 'te': 'telugu','ml' : 'malayalam','mr': 'marathi','gu': 'gujarati','pa': 'punjabi', 'cs': 'czech', 'hu': 'hungarian', 'sq': 'albanian', 'mg': 'malagasy', 'yo': 'yoruba', 'gd': 'scots gaelic', 'mt': 'maltese', 'bn': 'bengali', 'st': 'sesotho', 'az': 'azerbaijani', 'hy': 'armenian', 'hr': 'croatian', 'am': 'amharic', 'pt': 'portuguese', 'lt': 'lithuanian', 'tl': 'fil ipino', 'mn': 'mongolian', 'ceb': 'cebuano', 'lv': 'latvian', 'fil': 'Filipino', 'my': 'myanmar (burmese)', 'hmn': 'hmong', 'ar': 'arabic', 's u': 'sundanese', 'cy': 'welsh', 'no': 'norwegian', 'ja': 'japanese', 'uk': 'ukrainian', 'el': 'greek', 'sw': 'swahili', 'fr': ' french', 'ky': 'kyrgyz', 'kk': 'kazakh',  'km': 'khmer', 'sv': 'swedish', 'id': 'indonesian', 'fa': 'persian', 'ku': 'kurdish (k urmanji)', 'zh-tw': 'chinese (traditional)', 'be': 'belarusian', 'sr': 'serbian', 'ht': 'haitian creole',  'de': 'german',  'ps': 'pashto', 'ha': 'hausa', 'ru': 'russian',  'gl': 'galician', 'co': 'corsican', 'so': 'somali', 'th': 'tha i', 'uz': 'uzbek', 'ms': 'malay', 'da': 'danish', 'ny': 'chichewa', 'sn': 'shona', 'nl': 'dutch', 'lo': 'lao', 'fy': 'frisian ', 'sl': 'slovenian', 'fi': 'finnish', 'ig': 'igbo', 'et': 'estonian', 'tr': 'turkish', 'bg': 'bulgarian', 'eu': 'basque', 'haw': 'hawaiian', 'sk': 'slovak', 'si': 'sinhala', 'ne': 'nepali', 'ro': 'romanian', 'ca': 'catalan', 'xh': 'xhosa', 'ga': 'irish', 'lb': 'luxembourgish', 'jw': 'javanese', 'iw': 'hebrew', 'zh-cn': 'chinese (simplified)', 'tg': 'tajik', 'ko': 'korean', 'ur': 'urdu', 'it': 'italian', 'zu': 'zulu',  'mk': 'macedonian', 'sm': 'samoan', 'es': 'spanish', 'sd': 'sindhi',  'pl': 'polish', 'vi': 'vietnamese',  'ka': 'georgian', 'yi': 'yiddish', 'la': 'latin', 'eo': 'esperanto', 'af': 'afrikaans', 'is': 'icelandic', 'bs': 'bosnian', 'mi': ' maori', 'zh': 'chinese', 'he': 'Hebrew'}

#row = session.execute("select release_version from system.local").one()
#if row:
 #   print(row[0])
#else:
 #   print("An error occurred.")
#session.set_keyspace('data')

############

ids=[]


def index(request):
    return render(request, 'streamapp/input.html')
def quiz(request):

    return render(request, 'streamapp/copyquiz.html',{'a':3,'q1':{"QUESTION 1 Who developed the Python language?":['.py','.p','.c','.java'],"Which one of the following is the correct extension of the Python file?":['Zim Den','Guido van Rossum','Niene Stom','Wick van Rossum','.py','.python','.p','.java'],"QUESTION 1 Who developed the Python language?":['.py','.p','.c','.java'],"Which one of the following is the correct extension of the Python file?":['Zim Den','Guido van Rossum','Niene Stom','Wick van Rossum','.py','.python','.p','.java'],"QUESTION 1 Who developed the Python language?":['.py','.p','.c','.java'],"Which one of the following is the correct extension of the Python file?":['Zim Den','Guido van Rossum','Niene Stom','Wick van Rossum','.py','.python','.p','.java']}})

def take(request):
 
    global ids
    global d
    st=request.POST.get('st')
    user = request.POST.get('user')
    b = request.POST.get('pass')
    if st.lower()=="teacher":
        ids.append(user)
      #  futures = []
     #   query = "SELECT id FROM teacher"
       # futures.append(session.execute_async(query))
       # l = []
       # for future in futures:
       #     rows = future.result()
       #     l.append(str(rows[0].id))
      #  if user in l:
      #      c = "Sorry" + " " + "Please Login Account Already Exists"
       #     return render(request, 'streamapp/input.html', {'resultt': c,'d':d})
    #    else:
    ##        insert_statement = session.prepare("INSERT INTO teacher (id,psw) VALUES (?,?)")
      #      session.execute(insert_statement, [user, b])
       #     c =user.capitalize() 
       
        return render(request, 'streamapp/home.html',{'user':""})
    else:
        ids.append(user)
        futures = []
        query = "SELECT id FROM userdata"
      #  futures.append(session.execute_async(query))
       # l = []
        #for future in futures:
         #   rows = future.result()
          #  l.append(str(rows[0].id))
        #if user in l:
         #   c = "Sorry" + " " + "Please Login Account Already Exists"
          #  return render(request, 'streamapp/input.html', {'resultt': c,'d':d})
        #else:
         #   insert_statement = session.prepare("INSERT INTO userdata (id,pass) VALUES (?,?)")
          #  session.execute(insert_statement, [user, b])
           # c =user.capitalize() 
        return render(request, 'streamapp/home.html',{'user':""})

def add(request):
    global dpass
    global ids
    global user
    global d
    dpass=""
    st=request.POST.get('st')
    user=request.POST.get('user')
    passl=request.POST.get('pass')
    if False:
        print('cart id exists')
    else:
        if st.lower()!="teacher":
            try:
                query = "SELECT * FROM userdata WHERE id=%s"
             #   a=session.execute_async(query, [user])
                #for future in futures:
           #     rows = a.result()
           #     print(rows[0].field_2_)
          #      dpass=rows[0].field_2_
                if passl==dpass:
                    c =user.capitalize() 
                    return render(request, 'streamapp/home.html',{'user':""})
                else:
                    c = "Sorry" + " " + user +" Wrong Password Please Try Again"
                    return render(request, 'streamapp/home.html',{'user':""})
            except:
                c = "Sorry" + " " + user +" Please Sign Up Try Again"
                return render(request, 'streamapp/home.html',{'user':""})
        else:
            try:
                query = "SELECT * FROM teacher WHERE id=%s"
          #      a=session.execute_async(query, [user])
                #for future in futures:
           #     rows = a.result()
           #     print(rows[0].psw)
           #     dpass=rows[0].psw
                if passl==dpass:
                    c =user.capitalize() 
                    return render(request, 'streamapp/home.html',{'user':""})
                else:
                    c = "Sorry" + " " + user +" Wrong Password Please Try Again"
                    return render(request, 'streamapp/home.html',{'user':""})
            except:
                c = "Sorry" + " " + user +" Please Sign Up Try Again"
                return render(request, 'streamapp/home.html',{'user':""})
        

Test=False
frame1=""
def gen(camera):
    global frame1
    global Test
    global user
    while True:
        if Test==True:
            print(frame1)
          #  session.set_keyspace('data')
          #  insert_statement = session.prepare("INSERT INTO userdata (id,marks) VALUES (?,?)")
         #   session.execute(insert_statement, [user,str(frame1)])
            print("finaly break")
            break
        frame,frame1 = camera.get_frame()
        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_fee(request):
        global Test
        print("I AM THERE")
        Test=True
        c=request.POST.get('num1')
       # c = "WELCOME" + " " +"THIS IS YOUR TEST SUMMARY"
        futures = []
        query = "SELECT * FROM userdata WHERE id=%s"
 
      #  futures.append(session.execute_async(query,[user]))
        a=str(frame1).split(" ")
        print(l,a)
        c=a
        
        a1=c[-1]
        print(a)

        return render(request, 'streamapp/marks.html', {'c': a[:-1],'c1':['Number of Times Mouth Opened','Number of Times Head Up','Number of Times Head Down','Number of Times Head Left','Number of Times Head Right','Number of Times Left the Test'],'s':a1})

def video_feed(request):
    print(Test)
    if not(Test):
        return StreamingHttpResponse(gen(VideoCamera()),
                        content_type='multipart/x-mixed-replace; boundary=frame')
    print("video freed")
    return render(request, 'streamapp/wrong.html', {'res': "bryeu", 'data': False})
global l
l=[]
def video(request):
    fileObj=request.FILES['in']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    p="C:/Users/tanka/Downloads/video_stream-master/video_stream-master"+filePathName
    print(p)
    return render(request, 'streamapp/landt.html',{'res':"File Uploaded Sucessfull",'user':'Joseph'})
def startexm(request):
    return render(request, 'streamapp/home.html',{'user':""})
def record(request):
    return render(request, 'streamapp/rec.html')
def new(request):
    global d
    return render(request, 'streamapp/landss.html',{'d':d})    
 
 