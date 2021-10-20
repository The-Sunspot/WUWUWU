import out
from flask_app import app,db,User,Team,School,Sheet,View
from flask import render_template, request, url_for, redirect, flash,send_file, send_from_directory,make_response,current_app
from flask_login import login_required,logout_user,login_user

#登录界面--------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


#登出界面--------------------------------------------------------------------------
@app.route('/logout')
@login_required  # 视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页

#主页--------------------------------------------------------------------------
@app.route('/')
def index():
    print("hi")
    return render_template('index.html')


#录入-----------------------------------------------------------------------------
@app.route('/studentupdate',methods=['GET','POST'])
@login_required 
def update_student():
    if request.method=='POST':
        name1=request.form.get('name1')
        name2=request.form.get('name2')
        name3=request.form.get('name3')
        teacher=request.form.get('teacher')
        school=request.form.get('school')
        num=request.form.get('num')
        address=""
        #try:
        #    num=int(num)
        #except ValueError:
        #    flash('数据输入错误，请重新输入！')  
         #   return redirect(url_for('update_student'))
        
        stu=Team.query.filter_by(id=num).first()
        if stu:
            flash('队伍已经存在，修改请使用编辑')  
            return redirect(url_for('update_student'))

        stu=Team(
            name1=name1,
            name2=name2,
            name3=name3,
            school=school,
            teacher=teacher,
            id=num,
            address=address,
            score1=0.0,
            score2=0.0,
            score3=0.0,
            score4=0.0,
            score=0.0
        )
        target_school=School.query.filter_by(name=school).first()
        if not target_school:
            new_school=School(name=school)
            db.session.add(new_school)
            db.session.commit()
            target_school=School.query.filter_by(name=school).first()
        stu.schoolid=target_school.id
        db.session.add(stu)
        db.session.commit()
        flash(u'队伍信息添加成功!')
        return redirect(url_for('update_student'))
    stud=Team.query.all()
    return render_template('updatestu.html',student=stud)

#录入成绩------------------------------------------------
@app.route('/sheets',methods=['GET','POST'])
@login_required 
def submitsheet():
    if request.method=='POST':
        type=request.form.get('type')
        teamnum=request.form.get('teamnum')
        score=request.form.get('score')
        try:
            score=float(score)
            #teamnum=int(teamnum)
        except ValueError:
            flash('数据输入错误，请重新输入！')  # 显示错误提示
            return redirect(url_for('submitsheet'))
        if type=="地质技能综合应用":
            t=1
        elif type=="野外地质技能":
            t=2
        elif type=="地质标本鉴定":
            t=3
        else:
            t=4
        shet=Sheet(
            type=t,
            teamid=teamnum,
            score=score,
        )
        db.session.add(shet)

        stu = Team.query.filter(Team.id==teamnum).first()
        if stu is None:
            flash(u'没有这支队伍')
            return redirect(url_for('submitsheet'))
        #scho= School.query.filter(School.id==stu.schoolid).first()
        
        if t==1:
            stu.score1=score
        elif t==2:
            stu.score2=score
        elif t==3:
            stu.score3=score
        else:
            stu.score4=score
        stu.score=stu.score1+stu.score2+stu.score3+stu.score4
        
        db.session.commit()
        flash('评分表已提交！')
        return redirect(url_for('submitsheet'))
    return render_template('sheets.html')

#第一项
@app.route('/first')
def firstitem():
    stu=Team.query.order_by(Team.score1.desc()).all()
    return render_template('rank.html',student=stu)



@app.route('/second')
def seconditem():
    stu=Team.query.order_by(Team.score2.desc()).all()
    return render_template('rank2.html',student=stu)

@app.route('/third')
def thirditem():
    stu=Team.query.order_by(Team.score3.desc()).all()
    return render_template('rank3.html',student=stu)

@app.route('/fourth')
def fourthitem():
    stu=Team.query.order_by(Team.score4.desc()).all()
    return render_template('rank4.html',student=stu)

#队排，仅算abc
@app.route('/totalr')
def totalrank():
    stu=Team.query.all()
    stu=sorted(stu,key=lambda x:(x.score1+x.score2+x.score3),reverse=True) 
    return render_template('totalr.html',student=stu)

#校排名，按所有队abc总分排
@app.route('/abcrank')
def abcrank():
    school=School.query.all()
    schools=[]

    for sch in school:
        team_in_sch=Team.query.filter_by(schoolid=sch.id).all()
        view=View(sch.id,sch.name)
        for teams in team_in_sch:
            view.sum1+=teams.score1
            view.sum2+=teams.score2
            view.sum3+=teams.score3
        view.sum=view.sum1+view.sum2+view.sum3
        schools.append(view)
        
    schools=sorted(schools,key=lambda x:(-x.sum))
    return render_template('abcrank.html',school=schools)

#校排名，按abcd四项校最高分排
@app.route('/schor')
def schoolrank():
    school=School.query.all()
    schools=[]

    for sch in school:
        team_in_sch=Team.query.filter_by(schoolid=sch.id).all()
        view=View(sch.id,sch.name)
        for teams in team_in_sch:
            view.maxs1=max(view.maxs1,teams.score1)
            view.maxs2=max(view.maxs2,teams.score2)
            view.maxs3=max(view.maxs3,teams.score3)
            view.maxs4=max(view.maxs4,teams.score4)
        view.totalmax=view.maxs1+view.maxs2+view.maxs3+view.maxs4
        schools.append(view)

    schools=sorted(schools,key=lambda x:(-x.totalmax))
    return render_template('schor.html',school=schools)

@app.route('/export')
def export():
    return render_template('export.html')



@app.route('/studentupdate/delete/<stu_id>',methods=['POST'])
@login_required 
def delete_student(stu_id):
    student=Team.query.get_or_404(stu_id)
    db.session.delete(student)
    db.session.commit()
    flash('选手已删除')
    return redirect(url_for('update_student'))


@app.route('/edit/<stu_id>',methods=['GET','POST'])
@login_required 
def edit(stu_id):
    stu=Team.query.get_or_404(stu_id)
    # jsheet=JudgeSheet.query.filter(JudgeSheet.group==stu.group,JudgeSheet.snum==stu.name).all()
    if request.method=='POST':
        name1=request.form['name1']
        name2=request.form['name2']
        name3=request.form['name3']
        school=request.form['school']
        teacher=request.form['teacher']
        num=request.form['num']
        addr=''#request.form['address']
        #try:
        #    num=int(num)
        #except ValueError:
        #        flash('数据输入错误，请重新输入！')  # 显示错误提示
        #        return redirect(url_for('edit',stu_id=stu_id))
        stu.name1=name1
        stu.name2=name2
        stu.name3=name3
        stu.teacher=teacher
        stu.school=school
        stu.num=num
        stu.address=addr
        # stu.tele=tele
        # stu.score=score
        db.session.commit()
        flash('信息已修改')
        return redirect(url_for('update_student'))
    return render_template('edit.html',stu=stu)


@app.route('/download/team/<type_>')
def downloadforteam(type_):
    if type_ =='sum':
        filename=out.WirteTeamTotalRank()
    else:
        filename=out.WirteTeamSingleRank(type_)
        
    return current_app.send_static_file(filename)

@app.route('/download/school/<type_>')
def downloadforschool(type_):
    if type_ =='ABC':
        filename=out.WirteSchoolABCSumRank()
    else:
        filename=out.WirteSchoolABCDMaxRank()
        
    return current_app.send_static_file(filename)