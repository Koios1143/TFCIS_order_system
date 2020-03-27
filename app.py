import os, sys,re,yaml
from flask import Flask, request
from pymessenger import Bot
from json_write import modify
from datetime import datetime,timedelta

app = Flask(__name__)
config_data = open('secret.yml','r',newline='')
config = yaml.load(config_data)
PAGE_ACCESS_TOKEN = config['PAGE_ACCESS_TOKEN']
bot = Bot(PAGE_ACCESS_TOKEN)
lists = {}

def check_date(date):
    try:
        date = datetime.strptime(str(datetime.now().year) + '/' + date, "%Y/%m/%d")
        print('date: ' + str(date))
        now = datetime.now()
        print('now: ' + str(now))
        if(now - date >= timedelta(days = 1)):
            return False
        return True
    except:
        return False

@app.route("/", methods=["GET"])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if (not request.args.get("hub.verify_token")== config['verify_token']):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    log(data)
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                # IDs
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
    if messaging_event.get("message"):
        # Extracting text message
        reply_text = ''
        if "text" in messaging_event["message"]:
            ordi_text_message = messaging_event["message"]["text"]
            striped_text_message = ordi_text_message.replace(' ','')
            if(ordi_text_message[0:2] == '預約'):
                regex = re.compile(r'預約([0-9]*\/[0-9]*)')
                match = regex.search(striped_text_message)
                if(match == None):
                    reply_text = '輸入格式錯誤!\n請輸入 預約 月/日'
                else:
                    date = match.group(1)
                    if(check_date(date) == True):
                        result = modify(date,sender_id,True,'record.json')
                        if(result == 'File Open Error'):
                            reply_text = '檔案開啟失敗!'
                        elif(result == 'Write Error'):
                            reply_text = '檔案寫入錯誤'
                        elif(result == 'Success'):
                            reply_text = '預約成功!\n時間:' + str(date)
                        else:
                            reply_text = '出現意外狀況!\n請聯絡開發者'
                    else:
                        reply_text = '日期格式錯誤!'
            elif(ordi_text_message[0:4] == '取消預約'):
                regex = re.compile(r'取消預約([0-9]*\/[0-9]*)')
                match = regex.search(striped_text_message)
                if(match == None):
                    reply_text = '輸入格式錯誤!\n請輸入 取消預約 月/日'
                else:
                    date = match.group(1)
                    if(check_date(date) == True):
                        result = modify(date,sender_id,False,'record.json')
                        if(result == 'File Open Error'):
                            reply_text = '檔案開啟失敗!'
                        elif(result == 'Write Error'):
                            reply_text = '檔案寫入錯誤'
                        elif(result == 'Success'):
                            reply_text = '取消預約成功!\n時間:' + str(date)
                        elif(result == 'Not Found'):
                            reply_text = '要先預約才能取消預約w'
                        else:
                            reply_text = '出現意外狀況!\n請聯繫開發者'
                    else:
                        reply_text = '日期格式錯誤!'
            else:
                reply_text = ordi_text_message
        else:
           reply_text = "no text"
        # Echo
        response = reply_text
        bot.send_text_message(sender_id, reply_text)
    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=8888)