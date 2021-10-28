from flask import Flask, render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from sqlalchemy.sql import select
from sentence_transformers import SentenceTransformer, util
import spacy
from spacy.matcher import Matcher
import zh_core_web_lg
import scipy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column

# MySql datebase
app2 = Flask(__name__)
app = Flask(__name__)

app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app2.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./Question.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./student.db"

# 模型( model )定義
# MySql datebase

db2 = SQLAlchemy(app2)
db = SQLAlchemy(app)
#
# # Student table
class Student(db.Model):
    __tablename__ = 'student'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(30), unique=True, nullable=False)
    ID = db.Column(db.String(10), nullable=False)
    department = db.Column(
        db.String(30), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)


    def __init__(self, name, ID, department):
        self.name = name
        self.ID = ID
        self.department = department
#
# db.create_all()
# Student1 = Student('黑崇瑜', 'N26090114', '1231')
# db.session.add(Student1)
# db.session.commit()

    # Question table
class QuestionZH(db2.Model):
    __tablename__ = 'question'
    idz = db2.Column(db2.Integer, primary_key=True)
    questionz =db2.Column(db2.String(50), nullable=False)
    insert_time = db2.Column(db2.DateTime, default=datetime.now)
    update_time = db2.Column(
        db2.DateTime, onupdate=datetime.now, default=datetime.now)

    def __init__(self, questionz ):
        self.questionz = questionz


class Question(db2.Model):
    __tablename__ = 'lab_question'

    qid = db2.Column(db2.Integer, primary_key=True)
    questiona = db2.Column(db2.String(50), nullable=False)
    insert_time = db2.Column(db2.DateTime, default=datetime.now)
    update_time = db2.Column(
        db2.DateTime, onupdate=datetime.now, default=datetime.now)


    def __init__(self, questiona):
        self.questiona = questiona

# Student1 = Student('黑崇瑜', 'N26090114', '1231')
# db2.session.add(Student1)
# db2.session.commit()


def find_student(name):
    return Student.query.filter_by(name = name).first()

def new_student(name, ID):
    if (find_student(name) == None):
        dename = department_find(ID)
        Student1 = Student(name, ID, dename)

        db.session.add(Student1)
        db.session.commit()
        return True
    else:
        return False

def delete_student(name):
    if (find_student(name)):
        query = find_student(name)
        db.session.delete(query)
        db.session.commit()
        return True
    else:
        return False

# 找 ID 對應到的系所名稱
def department_find(id):
    # 抓前面兩個字
    df = pd.read_csv("department.csv", encoding="utf-8")
    df['dep_num'] = df['dep_num'].str.split('\xa0').str[0]
    df['dep_name'] = df['dep_name'].str.split('\xa0').str[0]
    df['dep_name'] = df['dep_name'].str.replace(" ", "")
    dep_dict = df.set_index("dep_num").T.to_dict("list")

    return dep_dict[id[:2]][0]  # department name

# 更新學生ID
def update_student(up_name, up_ID):

    if (find_student(up_name)):
        student_tar = find_student(up_name)
        student_tar.ID = up_ID
        student_tar.department = department_find(student_tar.ID)
        db.session.commit()
        return True
    else:
        return False



question_en =[]
question_zh =[]

def select_question_en():
    sql = f'select questiona from lab_question'
    row = [item[0] for item in db2.engine.execute(sql).fetchall()]
    return row

def select_question_zh():
    sql = f'select questionz from question'
    row = [item[0] for item in db2.engine.execute(sql).fetchall()]
    return row

# 計算句子的相似程度
def similarity_calculate(questions,sentence_embeddings,queries, query_embeddings):

    for query, query_embedding in zip(queries, query_embeddings):
        distances = scipy.spatial.distance.cdist([query_embedding], sentence_embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

    for idx, distance in results[0:1]:
        if (1 - distance) < 0.35:
            resu = "I do not understand your question \n Please rephrase your question."
        else:
            resu = 'Your question is similar to :' + str(questions[idx]) + '\nThe similarity score is :' + str(1 - distance)
    return  resu


def en_question(query):
    model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')
    queries = [query]
    query_embeddings = model.encode(queries)
    # Database question
    question_en = select_question_en()
    sentence_embeddings = model.encode(question_en)
    return similarity_calculate(question_en,sentence_embeddings,queries, query_embeddings)


def zh_question(query):
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    queries = [query]
    query_embeddings = model.encode(queries)
    question_zh = select_question_zh()
    sentence_embeddings = model.encode(question_zh)
    return  similarity_calculate(question_zh,sentence_embeddings,queries, query_embeddings)



# query1 = 'Can you tell me about your final project ?'
# query = '這堂課的作業會很難嗎?'
# # en_question(query)
# zh_question(query1)

# 英文句子判斷
def get_question(text):
    # for _char in text:
    #     if '\u4e00' <= _char <= '\u9fa5':
    #         respon = zh_question(text)
    #         return respon
    #     else :
    #         respon = en_question(text)
    #         return respon
    respon = en_question(text)
    return respon

# 中文
def get_questionz(text):
    respon = zh_question(text)
    return respon


# get_qusetion(query)
# print(get_qusetion(query))


