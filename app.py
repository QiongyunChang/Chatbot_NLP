from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
from db import new_student, find_student, delete_student,update_student,get_question,department_find,get_questionz
import re
#import Homework as HW

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header valuexlrd
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_all = []

    pattern_new = re.compile('新增學生:(.+)/學號:(.+)')
    pattern_delete = re.compile('刪除學生:(.+)')
    pattern_search = re.compile('查詢學生:(.+)')
    pattern_update = re.compile('更新學號:(.+)/(.+)')
    pattern_qusetion = re.compile('Q:(.+)')
    pattern_qusetionzh = re.compile('問題:(.+)')
    if pattern_new.findall(text):
        tokens = pattern_new.findall(text)
        name = tokens[0][0]
        ID = tokens[0][1]
        result = new_student(name, ID)
        if (result):
            response = "學生新增成功"
        else:
            response = "學生已存在"
    elif pattern_delete.findall(text):

        tokens = pattern_delete.findall(text)
        name = tokens[0]

        result = delete_student(name)
        if (result):
            response = "學生刪除成功"
        else:
            response = "學生不存在"

    elif pattern_search.findall(text):
        tokens = pattern_search.findall(text)
        name = tokens[0]
        if (find_student(name)):
            query = find_student(name)
            ID = query.ID
            department = query.department
            response = "姓名:" + name + "\n學號:" + ID + "\n科系:" + department + "\n"

        else:
            response = "學生不存在"

    # Update
    elif pattern_update.findall(text):
        tokens = pattern_update.findall(text)
        up_name = tokens[0][0]
        up_ID = tokens[0][1]
        department_name = department_find(up_ID)
        print(department_name)
        result = update_student(up_name, up_ID)
        if (result):
            response = "更新成功"
        else:
            response = "學生不存在"


    # # Asking a question
    elif pattern_qusetion.findall(text):
        tokens = pattern_qusetion.findall(text)
        questionask = tokens[0]
        result = get_question(questionask)
        response = result
    # 中文
    elif pattern_qusetionzh.findall(text):
        tokens = pattern_qusetionzh.findall(text)
        questionas = tokens[0]
        result = get_questionz(questionas)
        response = result
    else:

        reply_all.append(TextSendMessage(text="格式錯誤!!!"))
        response = '<<新增學生格式>>\n"新增學生:XXX/學號:XXX"\n\n<<刪除學生格式>>\n"刪除學生:XXX"\n\n<<查詢學生格式>>\n"查詢學生:XXX"\n\n<<詢問問題>>\nQ:"" or 問題:""\n\n<<更新學號格式>>\n"更新學號:"姓名"/ XXX"'

    reply_all.append(TextSendMessage(text=response))
    #response = '連到了啦'
    # 回覆文字訊息
    line_bot_api.reply_message(event.reply_token, reply_all)
if __name__ == "__main__":
    app.run(debug=True)
