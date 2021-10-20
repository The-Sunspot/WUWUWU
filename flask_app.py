import os
import sys
from flask import Flask
from flask_login import LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#-----------------------------------------------------------------init
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.run(debug=True)

#app.root_path在本机上指向了根目录上层，上网查询后发现应使用app.instance_path更优
#app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
#print(prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db')))

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.instance_path), os.getenv('DATABASE_FILE', 'data.db'))
#print(prefix + os.path.join(os.path.dirname(app.instance_path), os.getenv('DATABASE_FILE', 'data.db')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 关闭对模型修改的监控

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'
#login_manager.init_app(app)

#----------------------------------------------------------------------------------database
class Team(db.Model):
    id=db.Column(db.String(10),primary_key=True)#编号
    name1=db.Column(db.String(100))#三个队员
    name2=db.Column(db.String(100))
    name3=db.Column(db.String(100))
    teacher=db.Column(db.String(100))#指导教师
    school=db.Column(db.String(100))#所在学校
    schoolid=db.Column(db.Integer,db.ForeignKey('school.id'))
    address=db.Column(db.String(100))#联系方式？
    score1=db.Column(db.Float)#四项得分
    score2=db.Column(db.Float)
    score3=db.Column(db.Float)
    score4=db.Column(db.Float)
    score=db.Column(db.Float)#总分？

class Sheet(db.Model):
    id=db.Column(db.Integer,primary_key=True)#编号
    type=db.Column(db.Integer)
    teamid=db.Column(db.String(100),db.ForeignKey('team.id'))
    score=db.Column(db.Float)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class School(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

#查询用视图
class View():
    sum1=0.0
    sum2=0.0
    sum3=0.0
    sum=0.0
    maxs1=0.0
    maxs2=0.0
    maxs3=0.0
    maxs4=0.0
    totalmax=0.0
    def __init__(self,id,name):
        self.id=id
        self.name=name



@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

import views,cmd,out