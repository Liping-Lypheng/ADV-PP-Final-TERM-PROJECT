import requests

bot_token= '7238316965:AAGRFHDNvwUKuBG_WeDg8xQG898Ed8PECaY'
chat_id = '@lyphengchannel'

def sendmessage (message, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data={
          "chat_id": chat_id,
          "text": message,
          "parse_mode": "HTML"}
    r = requests.post(url, data = data)
    print (r.status_code)

def sendhtml (message, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendHTML"
    data={
          "chat_id": chat_id,
          "text": message,
          "parse_mode": "HTML"}
    r = requests.post(url, data = data)
    print (r.status_code)

def sendPhotoLocal(photolink, caption):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    data = {
        "chat_id": chat_id,
        "caption" : caption,
        "parse_mode": "HTML"
    }
    file = {
        "photo": photolink,
    }
    r = requests.post(url, data = data, files=file)
    print (r.status_code)

def sendVideoLocal(videolink,caption):
    url = f'https://api.telegram.org/bot{bot_token}/sendVideo'
    data = {
        "chat_id": chat_id,
        "caption": caption,
        "parse_mode": 'HTML',
    }
    file = {
        "video": videolink
    }
    r = requests.post(url, data=data,files=file)
    print(r.status_code)

def sendDocument(document,caption):
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    data = {
        "chat_id": chat_id,
        "document": document,
        "caption": caption
    }
    r = requests.post(url, data=data)
    print(r.status_code)

def sendVideoOnline(videolink,caption):
    url = f'https://api.telegram.org/bot{bot_token}/sendVideo'
    data = {
        "chat_id": chat_id,
        "video": videolink,
        "caption": caption,
        "parse_mode": 'HTML',
    }
    r = requests.post(url, data=data)
    print(r.status_code)

def sendPhotoOnline(photolink, caption):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    data = {
        "chat_id": chat_id,
        "photo": photolink,
        "caption" : caption,
        "parse_mode": "HTML"
    }

    r = requests.post(url, data = data)
    print (r.status_code)