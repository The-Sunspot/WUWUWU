import click
from flask_app import app,db,User,Team,School,Sheet,View
from os import name
from re import S

#创建管理员指令--------------------------------------------------
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')

#创建数据库指令--------------------------------------------------
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.') 
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

#导入--------------------------------------------------------------
@app.cli.command()
def filein():
    f=open('a.csv',mode='r',encoding='UTF-8')

    for i in f.readlines():
        fk=i.replace("\n","")
        i=fk.split(",")
        print(i)
        t=Team(
            school=i[0],
            id=i[1],
            name1=i[2],
            name2=i[3],
            name3=i[4],
            teacher=i[5],
            score1=0.0,
            score2=0.0,
            score3=0.0,
            score4=0.0,
            score=0.0,
        )
        sch=School.query.filter(School.name==t.school).first()
        if not sch:
            sch=School(name=t.school)
            db.session.add(sch)
            db.session.commit()
            sch=School.query.filter(School.name==t.school).first()
        t.schoolid=sch.id
        db.session.add(t)
    db.session.commit()
