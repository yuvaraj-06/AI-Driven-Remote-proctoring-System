import requests

url = "https://youtube-to-mp4.p.rapidapi.com/url=&title"

querystring = {"url":"https://www.youtube.com/watch?v=IfNB5RTxnhI"}

headers = {
    'x-rapidapi-key': "aa0e0452dbmsh1bd02053e0682f2p16604ajsn24e5063183f8",
    'x-rapidapi-host': "youtube-to-mp4.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)