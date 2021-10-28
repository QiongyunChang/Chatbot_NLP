from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
from testdb import new_student, find_student, delete_student,update_student,get_question,department_find,get_questionz
import re
#import Homework as HW

app = Flask(__name__)


def handle_message( text ):
    reply_all = []

    pattern_new = re.compile('新增學生:(.+)/學號:(.+)')
    pattern_delete = re.compile('刪除學生:(.+)')
    pattern_search = re.compile('查詢學生:(.+)')
    pattern_update = re.compile('更新學號:(.+)/(.+)')
    pattern_question = re.compile('Q:(.+)')
    pattern_questionzh = re.compile('問題:(.+)')
    pattern_sayhi = re.compile('Hi !')
    if pattern_new.findall(text):
        tokens = pattern_new.findall(text)
        name = tokens[0][0]
        ID = tokens[0][1]
        result = new_student(name, ID)
        if (result):
            response = "學生新增成功 \n 輸入: 查詢學生:XXX 即可以確認資料是否正確 \n 如果要刪除個人資訊輸入: 刪除學生:XXX 即可 \n" \
                       "更新學號:XXX/XXX ' \n"
        else:
            response = "學生已存在"

    elif pattern_delete.findall(text):

        tokens = pattern_delete.findall(text)
        name = tokens[0]

        result = delete_student(name)
        if (result):
            response = "學生刪除成功"
        else:
            response = "學生不存在 \n 可以輸入: 新增學生:XXX/學號:XXX 來新增資訊"


    elif pattern_search.findall(text):
        tokens = pattern_search.findall(text)
        name = tokens[0]
        if (find_student(name)):
            query = find_student(name)
            ID = query.ID
            department = query.department
            response = "姓名:" + name + "\n學號:" + ID + "\n科系:" + department

        else:
            response = "學生不存在 \n " \
                       "好像還沒新增資料呢 \n 可以輸入: 新增學生:XXX/學號:XXX 來新增資訊"

    # Update
    elif pattern_update.findall(text):
        tokens = pattern_update.findall(text)
        up_name = tokens[0][0]
        up_ID = tokens[0][1]
        # department_name = department_find(up_ID)
        result = update_student(up_name, up_ID)
        if (result):
            response = "更新成功! "
        else:
            response = "學生不存在"


    # # Asking a question
    elif pattern_question.findall(text):
        tokens = pattern_question.findall(text)
        questionask = tokens[0]
        result = get_question(questionask)
        response = result
    # 中文
    elif pattern_questionzh.findall(text):
        tokens = pattern_questionzh.findall(text)
        questionas = tokens[0]
        response =  get_questionz(questionas)
        print(response,'*****')

    elif pattern_sayhi(test):
        response = "Hi ! 歡迎加入 Chatbot 課程與我們一起學習! \n 在開始之前先填一下資料吧 ! \n 新增學生:XXX/學號:XXX \n 有相關問題也可以透過輸入" \
                   "Q:英文問題 或是 問題:中文問題 來提問喔 "
    else:

        reply_all.append(text)
        response = '<<新增學生格式>>\n"新增學生:XXX/學號:XXX"\n\n<<刪除學生格式>>\n"刪除學生:XXX"\n\n<<查詢學生格式>>\n"查詢學生:XXX"\n\n<<詢問問題>>\nQ:"" or 問題:""\n\n<<更新學號格式>>\n"更新學號:"姓名"/ XXX"'

    reply_all.append(text)
    #response = '連到了啦'
    # 回覆文字訊息
    print(reply_all)

if __name__ == "__main__":
    qu="問題:今天上課上了甚麼?"
    # qu="Q:How's the project going?"
    # qu ="查詢學生:阿呆"
    print(qu)
    handle_message(qu)

