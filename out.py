import datetime
import xlwt
import os
from flask_app import app,db,User,Team,School,Sheet,View
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required,logout_user,login_user
dict={'A':'地质技能综合应用排名','B':'野外地质技能竞赛排名','C':'地质标本鉴定竞赛排名','D':'地学知识抢答竞赛排名','SUM':'总分'}

def WirteTeamSingleRank(typ):
    
    wb=xlwt.Workbook()
    sheet=wb.add_sheet(dict[typ])
    teamlist=[]
    if typ=='A':
        teamlist=Team.query.order_by(Team.score1.desc()).all()
    elif typ=='B':
        teamlist=Team.query.order_by(Team.score2.desc()).all()
    elif typ=='C':
        teamlist=Team.query.order_by(Team.score3.desc()).all()
    elif typ=='D':
        teamlist=Team.query.order_by(Team.score4.desc()).all()
    print(teamlist)
    print(typ)
    sheet.write(0,0,'队伍编号')
    sheet.write(0,1,'学校名称')
    sheet.write(0,2,'参赛学生')
    sheet.write(0,3,'指导教师')
    sheet.write(0,4,'得分')
    if teamlist is not None:
        x=1
        for team in teamlist:
            sheet.write(x,0,team.id)
            sheet.write(x,1,team.school)
            sheet.write(x,2,team.name1+','+team.name2+','+team.name3)
            sheet.write(x,3,team.teacher)
            if typ=='A':
                sheet.write(x,4,team.score1)
            elif typ=='B':
                sheet.write(x,4,team.score2)
            elif typ=='C':
                sheet.write(x,4,team.score3)
            elif typ=='D':
                sheet.write(x,4,team.score4)
            x+=1
    now = datetime.datetime.now().time().strftime('%H时%M分')
    path='static'
    fileName = typ+dict[typ]+"队伍排名" + now + ".xls"
    file_path =  os.path.join(os.path.dirname(app.instance_path),path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path,fileName)    
    try:
        f = open(file_path, 'r')
        f.close()
    except IOError:
        f = open(file_path, 'w')
        f.close()
    wb.save(file_path)
    return fileName
    
def WirteTeamTotalRank():
    
    wb=xlwt.Workbook()
    sheet=wb.add_sheet('队伍总分排名')
    teamlist=Team.query.all()
    teamlist=sorted(teamlist,key=lambda x:(x.score1+x.score2+x.score3),reverse=True) 
    sheet.write(0,0,'队伍编号')
    sheet.write(0,1,'学校名称')
    sheet.write(0,2,'参赛学生')
    sheet.write(0,3,'指导教师')
    sheet.write(0,4,dict['A']+'得分')
    sheet.write(0,5,dict['B']+'得分')
    sheet.write(0,6,dict['C']+'得分')
    sheet.write(0,7,'总分')
    if teamlist is not None:
        x=1
        for team in teamlist:
            sheet.write(x,0,team.id)
            sheet.write(x,1,team.school)
            sheet.write(x,2,team.name1+','+team.name2+','+team.name3)
            sheet.write(x,3,team.teacher)
            sheet.write(x,4,team.score1)
            sheet.write(x,5,team.score2)
            sheet.write(x,6,team.score3)
            sheet.write(x,7,team.score1+team.score2+team.score3)
            x+=1
    now = datetime.datetime.now().time().strftime('%H时%M分')
    path='static'
    fileName = "ABC总分队伍排名" + now + ".xls"
    file_path =  os.path.join(os.path.dirname(app.instance_path),path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path,fileName)    
    try:
        f = open(file_path, 'r')
        f.close()
    except IOError:
        f = open(file_path, 'w')
        f.close()
    wb.save(file_path)
    return fileName

def WirteSchoolABCSumRank():
    wb=xlwt.Workbook()
    sheet=wb.add_sheet('学校ABC三项队伍总分排名')
    sheet.write(0,0,'学校名称')    
    sheet.write(0,1,dict['A']+'学校队伍总得分')
    sheet.write(0,2,dict['B']+'学校队伍总得分')
    sheet.write(0,3,dict['C']+'学校队伍总得分')
    sheet.write(0,4,'学校队伍总分')

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
    x=1
    for sch in schools:
        sheet.write(x,0,sch.name)
        sheet.write(x,1,sch.sum1)
        sheet.write(x,2,sch.sum2)
        sheet.write(x,3,sch.sum3)
        sheet.write(x,4,sch.sum)
        x+=1
    now = datetime.datetime.now().time().strftime('%H时%M分')
    path='static'
    fileName = "学校ABC三项队伍总分排名" + now + ".xls"
    file_path =  os.path.join(os.path.dirname(app.instance_path),path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path,fileName)    
    try:
        f = open(file_path, 'r')
        f.close()
    except IOError:
        f = open(file_path, 'w')
        f.close()
    wb.save(file_path)
    return fileName

def WirteSchoolABCDMaxRank():
    wb=xlwt.Workbook()
    sheet=wb.add_sheet('学校ABC三项队伍总分排名')
    sheet.write(0,0,'学校名称')    
    sheet.write(0,1,dict['A']+'学校队伍最高得分')
    sheet.write(0,2,dict['B']+'学校队伍最高得分')
    sheet.write(0,3,dict['C']+'学校队伍最高得分')
    sheet.write(0,4,dict['D']+'学校队伍最高得分')
    sheet.write(0,5,'学校队伍总分')

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
    x=1
    for sch in schools:
        sheet.write(x,0,sch.name)
        sheet.write(x,1,sch.maxs1)
        sheet.write(x,2,sch.maxs2)
        sheet.write(x,3,sch.maxs3)
        sheet.write(x,4,sch.maxs4)
        sheet.write(x,5,sch.totalmax)
        x+=1
    now = datetime.datetime.now().time().strftime('%H时%M分')
    path='static'
    fileName = "学校ABCD三项队伍最高分排名" + now + ".xls"
    file_path =  os.path.join(os.path.dirname(app.instance_path),path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path,fileName)    
    try:
        f = open(file_path, 'r')
        f.close()
    except IOError:
        f = open(file_path, 'w')
        f.close()
    wb.save(file_path)
    return fileName