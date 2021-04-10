import os
from moviepy.editor import *
import moviepy.editor as mp
from os.path import dirname, join
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http.response import StreamingHttpResponse
from streamapp.camera import VideoCamera
from django.template.loader import render_to_string
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from django.template import loader, Context
from json import dumps 
from django.template.defaulttags import register
from threading import Thread
import requests
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import base64
import gtts
from deep_translator import GoogleTranslator
from moviepy.editor import *
from moviepy.editor import *
import pdfplumber
#path='/staticfiles'
cloud_config= {
        'secure_connect_bundle': join(dirname(__file__), "secure-connect-database.zip")
}
auth_provider = PlainTextAuthProvider('Datauser', 'database@1')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
d= {'hi': 'hindi','en': 'english','ta': 'tamil','kn': 'kannada', 'te': 'telugu','ml' : 'malayalam','mr': 'marathi','gu': 'gujarati','pa': 'punjabi', 'cs': 'czech', 'hu': 'hungarian', 'sq': 'albanian', 'mg': 'malagasy', 'yo': 'yoruba', 'gd': 'scots gaelic', 'mt': 'maltese', 'bn': 'bengali', 'st': 'sesotho', 'az': 'azerbaijani', 'hy': 'armenian', 'hr': 'croatian', 'am': 'amharic', 'pt': 'portuguese', 'lt': 'lithuanian', 'tl': 'fil ipino', 'mn': 'mongolian', 'ceb': 'cebuano', 'lv': 'latvian', 'fil': 'Filipino', 'my': 'myanmar (burmese)', 'hmn': 'hmong', 'ar': 'arabic', 's u': 'sundanese', 'cy': 'welsh', 'no': 'norwegian', 'ja': 'japanese', 'uk': 'ukrainian', 'el': 'greek', 'sw': 'swahili', 'fr': ' french', 'ky': 'kyrgyz', 'kk': 'kazakh',  'km': 'khmer', 'sv': 'swedish', 'id': 'indonesian', 'fa': 'persian', 'ku': 'kurdish (k urmanji)', 'zh-tw': 'chinese (traditional)', 'be': 'belarusian', 'sr': 'serbian', 'ht': 'haitian creole',  'de': 'german',  'ps': 'pashto', 'ha': 'hausa', 'ru': 'russian',  'gl': 'galician', 'co': 'corsican', 'so': 'somali', 'th': 'tha i', 'uz': 'uzbek', 'ms': 'malay', 'da': 'danish', 'ny': 'chichewa', 'sn': 'shona', 'nl': 'dutch', 'lo': 'lao', 'fy': 'frisian ', 'sl': 'slovenian', 'fi': 'finnish', 'ig': 'igbo', 'et': 'estonian', 'tr': 'turkish', 'bg': 'bulgarian', 'eu': 'basque', 'haw': 'hawaiian', 'sk': 'slovak', 'si': 'sinhala', 'ne': 'nepali', 'ro': 'romanian', 'ca': 'catalan', 'xh': 'xhosa', 'ga': 'irish', 'lb': 'luxembourgish', 'jw': 'javanese', 'iw': 'hebrew', 'zh-cn': 'chinese (simplified)', 'tg': 'tajik', 'ko': 'korean', 'ur': 'urdu', 'it': 'italian', 'zu': 'zulu',  'mk': 'macedonian', 'sm': 'samoan', 'es': 'spanish', 'sd': 'sindhi',  'pl': 'polish', 'vi': 'vietnamese',  'ka': 'georgian', 'yi': 'yiddish', 'la': 'latin', 'eo': 'esperanto', 'af': 'afrikaans', 'is': 'icelandic', 'bs': 'bosnian', 'mi': ' maori', 'zh': 'chinese', 'he': 'Hebrew'}

row = session.execute("select release_version from system.local").one()
if row:
    print(row[0])
else:
    print("An error occurred.")
session.set_keyspace('data')

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
        futures = []
        query = "SELECT id FROM teacher"
        futures.append(session.execute_async(query))
        l = []
        for future in futures:
            rows = future.result()
            l.append(str(rows[0].id))
        if user in l:
            c = "Sorry" + " " + "Please Login Account Already Exists"
            return render(request, 'streamapp/input.html', {'resultt': c,'d':d})
        else:
            insert_statement = session.prepare("INSERT INTO teacher (id,psw) VALUES (?,?)")
            session.execute(insert_statement, [user, b])
            c =user.capitalize() 
            return render(request, 'streamapp/landt.html', {'user': c,'d':d})
    else:
        ids.append(user)
        futures = []
        query = "SELECT id FROM userdata"
        futures.append(session.execute_async(query))
        l = []
        for future in futures:
            rows = future.result()
            l.append(str(rows[0].id))
        if user in l:
            c = "Sorry" + " " + "Please Login Account Already Exists"
            return render(request, 'streamapp/input.html', {'resultt': c,'d':d})
        else:
            insert_statement = session.prepare("INSERT INTO userdata (id,pass) VALUES (?,?)")
            session.execute(insert_statement, [user, b])
            c =user.capitalize() 
            return render(request, 'streamapp/landt.html', {'user': c,'d':d})

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
                a=session.execute_async(query, [user])
                #for future in futures:
                rows = a.result()
                print(rows[0].field_2_)
                dpass=rows[0].field_2_
                if passl==dpass:
                    c =user.capitalize() 
                    return render(request, 'streamapp/lands.html', {'user': c,'d':d})
                else:
                    c = "Sorry" + " " + user +" Wrong Password Please Try Again"
                    return render(request, 'streamapp/input.html', {'result': c,'d':d})
            except:
                c = "Sorry" + " " + user +" Please Sign Up Try Again"
                return render(request, 'streamapp/input.html', {'result': c,'d':d})
        else:
            try:
                query = "SELECT * FROM teacher WHERE id=%s"
                a=session.execute_async(query, [user])
                #for future in futures:
                rows = a.result()
                print(rows[0].psw)
                dpass=rows[0].psw
                if passl==dpass:
                    c =user.capitalize() 
                    return render(request, 'streamapp/landt.html', {'user': c,'d':d})
                else:
                    c = "Sorry" + " " + user +" Wrong Password Please Try Again"
                    return render(request, 'streamapp/input.html', {'result': c,'d':d})
            except:
                c = "Sorry" + " " + user +" Please Sign Up Try Again"
                return render(request, 'streamapp/input.html', {'result': c,'d':d})
        

Test=False
frame1=""
def gen(camera):
    global frame1
    global Test
    global user
    while True:
        if Test==True:
            print(frame1)
            session.set_keyspace('data')
            insert_statement = session.prepare("INSERT INTO userdata (id,marks) VALUES (?,?)")
            session.execute(insert_statement, [user,str(frame1)])
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
 
        futures.append(session.execute_async(query,[user]))
        l = []
        for future in futures:
            rows = future.result()
            l.append(str(rows[0].marks))
            a=str(rows[0].marks).split(" ")
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
    return render(request, 'streamapp/home.html',{'user':user})
def record(request):
    return render(request, 'streamapp/rec.html')
def new(request):
    global d
    return render(request, 'streamapp/landss.html',{'d':d})    
def vid(request):
    if "1" in request.POST:
        futures = []
        query = "SELECT * FROM teacher"
        ids_to_fetch=[1]
        for user_id in ids_to_fetch:
            futures.append(session.execute_async(query))
        for i in futures:
            rows = i.result()
            a=rows[0].trans
        a=a.strip('][').split(',') 
        s=a[0].strip("'")
        return render(request, 'streamapp/recout.html',{'res':s})
    elif "2" in request.POST: 
        futures = []
        query = "SELECT * FROM teacher"
        ids_to_fetch=[1]
        for user_id in ids_to_fetch:
            futures.append(session.execute_async(query))
        for i in futures:
            rows = i.result()
            a=rows[1].trans
        a=a.strip('][').split(',') 
        s=a[0].strip("'")
        return render(request, 'streamapp/recout.html',{'res':s})
  
def trans(request):
    if "1" in request.POST:
        futures = []
        query = "SELECT * FROM teacher"
        ids_to_fetch=[1]
        for user_id in ids_to_fetch:
            futures.append(session.execute_async(query))
        for i in futures:
            rows = i.result()
            a=rows[0].trans
        a=a.strip('][').split(',') 
        return render(request, 'streamapp/transout.html',{'res':a[1]})
    elif "2" in request.POST: 
        futures = []
        query = "SELECT * FROM teacher"
        ids_to_fetch=[1]
        for user_id in ids_to_fetch:
            futures.append(session.execute_async(query))
        for i in futures:
            rows = i.result()
            a=rows[1].trans
        a=a.strip('][').split(',')
        return render(request, 'streamapp/transout.html',{'res':a[1]})
def index_1(request):
    
    d= {'hi': 'hindi','en': 'english','ta': 'tamil','kn': 'kannada', 'te': 'telugu','ml' : 'malayalam','mr': 'marathi','gu': 'gujarati','pa': 'punjabi', 'cs': 'czech', 'hu': 'hungarian', 'sq': 'albanian', 'mg': 'malagasy', 'yo': 'yoruba', 'gd': 'scots gaelic', 'mt': 'maltese', 'bn': 'bengali', 'st': 'sesotho', 'az': 'azerbaijani', 'hy': 'armenian', 'hr': 'croatian', 'am': 'amharic', 'pt': 'portuguese', 'lt': 'lithuanian', 'tl': 'fil ipino', 'mn': 'mongolian', 'ceb': 'cebuano', 'lv': 'latvian', 'fil': 'Filipino', 'my': 'myanmar (burmese)', 'hmn': 'hmong', 'ar': 'arabic', 's u': 'sundanese', 'cy': 'welsh', 'no': 'norwegian', 'ja': 'japanese', 'uk': 'ukrainian', 'el': 'greek', 'sw': 'swahili', 'fr': ' french', 'ky': 'kyrgyz', 'kk': 'kazakh',  'km': 'khmer', 'sv': 'swedish', 'id': 'indonesian', 'fa': 'persian', 'ku': 'kurdish (k urmanji)', 'zh-tw': 'chinese (traditional)', 'be': 'belarusian', 'sr': 'serbian', 'ht': 'haitian creole',  'de': 'german',  'ps': 'pashto', 'ha': 'hausa', 'ru': 'russian',  'gl': 'galician', 'co': 'corsican', 'so': 'somali', 'th': 'tha i', 'uz': 'uzbek', 'ms': 'malay', 'da': 'danish', 'ny': 'chichewa', 'sn': 'shona', 'nl': 'dutch', 'lo': 'lao', 'fy': 'frisian ', 'sl': 'slovenian', 'fi': 'finnish', 'ig': 'igbo', 'et': 'estonian', 'tr': 'turkish', 'bg': 'bulgarian', 'eu': 'basque', 'haw': 'hawaiian', 'sk': 'slovak', 'si': 'sinhala', 'ne': 'nepali', 'ro': 'romanian', 'ca': 'catalan', 'xh': 'xhosa', 'ga': 'irish', 'lb': 'luxembourgish', 'jw': 'javanese', 'iw': 'hebrew', 'zh-cn': 'chinese (simplified)', 'tg': 'tajik', 'ko': 'korean', 'ur': 'urdu', 'it': 'italian', 'zu': 'zulu',  'mk': 'macedonian', 'sm': 'samoan', 'es': 'spanish', 'sd': 'sindhi',  'pl': 'polish', 'vi': 'vietnamese',  'ka': 'georgian', 'yi': 'yiddish', 'la': 'latin', 'eo': 'esperanto', 'af': 'afrikaans', 'is': 'icelandic', 'bs': 'bosnian', 'mi': ' maori', 'zh': 'chinese', 'he': 'Hebrew'}


    
    
    c={'d':d}

    return render(request, 'streamapp/ip.html',c )


def submit(request):


    d_type = request.POST.get("transcript_1", None)
    d1_type = request.POST.get("transcript_2", None)
    d2_type = request.POST.get("transcript_3", None)
   

    if d1_type:
        lan=request.POST.get('lan')
        fileObj=request.FILES['myfile']
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)
        a=str(filePathName)    
        a=a[7:]
        p=os.path.abspath(os.path.join('media', a))
        print(p)
        from gtts import gTTS
        te=''
        pdf = pdfplumber.open(p)
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            te += page.extract_text()
        out = GoogleTranslator(source='en', target=lan).translate(text=te)
        t=gTTS(str(out),lang=lan)
        pdf.close()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        t.save("%s.mp3" % os.path.join(BASE_DIR+'/media',a))
        params={'outremain':out[200:],'out':out[:200],'outaud':filePathName+".mp3"}
        print(params)
        return render(request,'streamapp/ip.html',params)



    if d_type:

        lan=request.POST.get('lan')
        fileObj=request.FILES['myfile']
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)
        a=str(filePathName)    
        a=a[7:]
        p=os.path.abspath(os.path.join('media', a))
        print(p)
        


        from threading import Thread
        import requests

        import base64
        

        vid=p#filw
        clip = VideoFileClip(vid)
        clipA = VideoFileClip(vid)
        clipB = VideoFileClip(vid)
        clipC = VideoFileClip(vid)
        clipD = VideoFileClip(vid)
        def intervals(parts, duration):
            part_duration = duration / parts
            return [(i * part_duration, (i + 1) * part_duration) for i in range(parts)]


        duration = clip.duration
        dur = (intervals(4, duration))

        import moviepy.editor as mp


        def a():
            x1 = dur[0][0]
            y1 = dur[0][1]
            clip1 = clipA.subclip(x1, y1)
            clip1.write_videofile("clip1.mp4")
            clipa = mp.VideoFileClip(r"clip1.mp4")
            clipa.audio.write_audiofile(r"v1.wav")


        def b():
            x2 = dur[1][0]
            y2 = dur[1][1]

            clip2 = clipB.subclip(x2, y2)
            clip2.write_videofile("clip2.mp4")
            clipb = mp.VideoFileClip(r"clip2.mp4")
            clipb.audio.write_audiofile(r"v2.wav")


        def c():
            x3 = dur[2][0]
            y3 = dur[2][1]

            clip3 = clipC.subclip(x3, y3)
            clip3.write_videofile("clip3.mp4")
            clipc = mp.VideoFileClip(r"clip3.mp4")
            clipc.audio.write_audiofile(r"v3.wav")


        def d():
            x4 = dur[3][0]
            y4 = dur[3][1]

            clip4 = clipD.subclip(x4, y4)
            clip4.write_videofile("clip4.mp4")
            clipd = mp.VideoFileClip(r"clip4.mp4")
            clipd.audio.write_audiofile(r"v4.wav")


        a1 = Thread(target=a)
        a2 = Thread(target=b)
        a3 = Thread(target=c)
        a4 = Thread(target=d)
        a1.start()
        a2.start()
        a3.start()
        a4.start()
        a1.join()
        a2.join()
        a3.join()
        a4.join()
        import speech_recognition as sr
        
        from pydub import AudioSegment
        from pydub.silence import split_on_silence

        r = sr.Recognizer()

        def get_large_audio_transcription(path):
            sound = AudioSegment.from_wav(path)
            chunks = split_on_silence(sound,
                min_silence_len = 500,
                silence_thresh = sound.dBFS-14,
                keep_silence=500,
            )
            folder_name = "audio-chunks"
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            whole_text = ""
            for i, audio_chunk in enumerate(chunks, start=1):
                chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
                audio_chunk.export(chunk_filename, format="wav")
                with sr.AudioFile(chunk_filename) as source:
                    audio_listened = r.record(source)
                    try:
                        text = r.recognize_google(audio_listened)
                    except sr.UnknownValueError as e:
                        print("Error:", str(e))
                    else:
                        text = f"{text.capitalize()}. "
                        print(chunk_filename, ":", text)
                        whole_text += text
            return whole_text
        out=""
        for i in range(1,5):
            path = "v"+str(i)+".wav"

            out=out+get_large_audio_transcription(path)
        # print("\nFull text:", out)

        #lan='te'#input lang
        out = GoogleTranslator(source='en', target=lan).translate(text=out)
        from gtts import gTTS
        t=gTTS(str(out),lang=lan)
        t.save("final.mp3")
        
        from mutagen.mp3 import MP3
        audio = MP3("final.mp3")
        print(audio.info.length)
        # loading video gfg
        

        # loading audio file
        print(clip.duration)
        audioclip = AudioFileClip("final.mp3").subclip(0, int(audio.info.length))

        # adding audio to the video clip
        videoclip = clip.set_audio(audioclip)
        videoclip.write_videofile(p) 

        
        
    
        params = {'filePathName':filePathName}
        return render(request,'streamapp/ip.html',params)



    if d2_type:

        
        lan=request.POST.get('lan')
        fileObj=request.FILES['myfile']
        file_extension=fileObj.name.split('.')[-1]
        
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)
        z=str(filePathName)    
        z=z[7:]
        p=os.path.abspath(os.path.join('media', z))
       

        if file_extension =='pdf':




            from gtts import gTTS
            te=''
            pdf = pdfplumber.open(p)
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                te += page.extract_text()
            
            import requests
            r = requests.post(
                "https://api.deepai.org/api/summarization",
                data={
                    'text': te,
                },
                headers={'api-key': '718a2393-cc34-42e8-9129-bd7fe0ead6a4'}
            )
            sum=(r.json())
            sum_out=sum["output"]




            out = GoogleTranslator(source='en', target=lan).translate(text=sum_out)
            t=gTTS(str(out),lang=lan)
            pdf.close()
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            t.save("%s.mp3" % os.path.join(BASE_DIR+'/media',z))
            params={'outremain':out[200:],'out':out[:200],'outaud':filePathName+".mp3"}
            print(params)
            return render(request,'streamapp/ip.html',params)

        else:
            


            from threading import Thread
            import requests

            import base64
            

            vid=p#filw
            clip = VideoFileClip(vid)
            clipA = VideoFileClip(vid)
            clipB = VideoFileClip(vid)
            clipC = VideoFileClip(vid)
            clipD = VideoFileClip(vid)
            def intervals(parts, duration):
                part_duration = duration / parts
                return [(i * part_duration, (i + 1) * part_duration) for i in range(parts)]


            duration = clip.duration
            dur = (intervals(4, duration))

            import moviepy.editor as mp


            def a():
                x1 = dur[0][0]
                y1 = dur[0][1]
                clip1 = clipA.subclip(x1, y1)
                clip1.write_videofile("clip1.mp4")
                clipa = mp.VideoFileClip(r"clip1.mp4")
                clipa.audio.write_audiofile(r"v1.wav")


            def b():
                x2 = dur[1][0]
                y2 = dur[1][1]

                clip2 = clipB.subclip(x2, y2)
                clip2.write_videofile("clip2.mp4")
                clipb = mp.VideoFileClip(r"clip2.mp4")
                clipb.audio.write_audiofile(r"v2.wav")


            def c():
                x3 = dur[2][0]
                y3 = dur[2][1]

                clip3 = clipC.subclip(x3, y3)
                clip3.write_videofile("clip3.mp4")
                clipc = mp.VideoFileClip(r"clip3.mp4")
                clipc.audio.write_audiofile(r"v3.wav")


            def d():
                x4 = dur[3][0]
                y4 = dur[3][1]

                clip4 = clipD.subclip(x4, y4)
                clip4.write_videofile("clip4.mp4")
                clipd = mp.VideoFileClip(r"clip4.mp4")
                clipd.audio.write_audiofile(r"v4.wav")


            a1 = Thread(target=a)
            a2 = Thread(target=b)
            a3 = Thread(target=c)
            a4 = Thread(target=d)
            a1.start()
            a2.start()
            a3.start()
            a4.start()
            a1.join()
            a2.join()
            a3.join()
            a4.join()
            import speech_recognition as sr
            
            from pydub import AudioSegment
            from pydub.silence import split_on_silence

            r = sr.Recognizer()

            def get_large_audio_transcription(path):
                sound = AudioSegment.from_wav(path)
                chunks = split_on_silence(sound,
                    min_silence_len = 500,
                    silence_thresh = sound.dBFS-14,
                    keep_silence=500,
                )
                folder_name = "audio-chunks"
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                whole_text = ""
                for i, audio_chunk in enumerate(chunks, start=1):
                    chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
                    audio_chunk.export(chunk_filename, format="wav")
                    with sr.AudioFile(chunk_filename) as source:
                        audio_listened = r.record(source)
                        try:
                            text = r.recognize_google(audio_listened)
                        except sr.UnknownValueError as e:
                            print("Error:", str(e))
                        else:
                            text = f"{text.capitalize()}. "
                            print(chunk_filename, ":", text)
                            whole_text += text
                return whole_text
            out=""
            for i in range(1,5):
                path = "v"+str(i)+".wav"

                out=out+get_large_audio_transcription(path)

            
            # print("\nFull text:", out)
            
            #out="Hello everyone welcome to the project news app. Latest cena problem statement of this project. The news aggregator algorithm acts as an one stop destination for various categories of dressing use like. Sports national news science extra. Elected from various new circulations is. Given the category of news the user likes to sirf. An interactive interface designs and displays the latest news for the category. 18 seconds. Latest some applications and scenarios. The uses of this algorithm are many in fact that uses a lot of versatile. Commentary today's i was a missing you stop for all existing news. Aspiring businessman who wishes to run a competition and advertising capability of different news companies. There is no better place than one like this. And false how different new system support a single in. Vacillating comparison. Working follower of news who wants to get updated and let latest news. This new system is just what he or she might be looking for. Kishangarh jump code pretty much make up the day for many in many ways. Latest tech stack involved in this project. Task name using django python and some news api. Now let us see some sample input and output of this application. Starting from. Wide variety of news categories. 50 world business. Oats health and science. Let me classified application which contains. Free options one s you can see the headlines of the news. Are also the description of the news. And if you want to read the whole article you can also click on the respective headlines to redirect to its homepage. Read the whole article is located. Latest wrap up thank you."
            
            import requests
            r = requests.post(
                "https://api.deepai.org/api/summarization",
                data={
                    'text': out,
                },
                headers={'api-key': '718a2393-cc34-42e8-9129-bd7fe0ead6a4'}
            )
            sum=(r.json())
            sum_out=sum["output"]
            
            


                
            from gtts import gTTS
            out = GoogleTranslator(source='en', target=lan).translate(text=sum_out)
            t=gTTS(str(out),lang=lan)
            
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            t.save("%s.mp3" % os.path.join(BASE_DIR+'/media',z))
            params={'outremain':out[200:],'out':out[:200],'outaud':filePathName+".mp3"}
            print(params)
            return render(request,'streamapp/ip.html',params)


            
    
