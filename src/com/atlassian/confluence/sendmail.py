#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import time
import os
import ConfigParser
from src.com.atlassian.confluence.scrum import getAllTeamsInfoByNum
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

A_TEAM_MailAddr = 'timmy.yuan@netis.com'
L_TEAM_MailAddr = 'jacob.du@netis.com'
M_TEAM_MailAddr = 'ethan.zhou@netis.com'
N_TEAM_MailAddr = 'felix.zhu@netis.com'
W_TEAM_MailAddr = 'vincent.ye@netis.com'


def parse_sprint_date(sprint_date):
    filedir = os.path.split(os.path.realpath(__file__))[0]
    configPath = os.path.join(filedir, 'sprint_date_map.ini')
    config = ConfigParser.ConfigParser()
    config.read(configPath)
    # print config.options('sprint_2019')
    sprint_num = config.get('sprint_2019', sprint_date)
    return sprint_num   

def get_team_sprint_info():
    today = time.strftime("%y/%m/%d")
    num = int(parse_sprint_date(today))
    return getAllTeamsInfoByNum(num)

def get_mail_addr():
    team_infos = get_team_sprint_info()
    blank_teams = []
    for team, info in team_infos.iteritems():
        if info[2] == 'Kanban':
            pass
        if info[2] == '' or info[3] == '':
            blank_teams.append(team)
    print blank_teams
    send_mail_addr = []
    if blank_teams:
        for team in blank_teams:
            if team in ['a_team','b_team','c_team']:
                send_mail_addr.append(A_TEAM_MailAddr)
            elif team == 'l_team':
                send_mail_addr.append(L_TEAM_MailAddr)
            elif team == 'm_team':
                send_mail_addr.append(M_TEAM_MailAddr)
            elif team == 'n_team':
                send_mail_addr.append(N_TEAM_MailAddr)
            elif team == 'w_team':
                send_mail_addr.append(W_TEAM_MailAddr)
            else:
                print 'Error team'
    return list(set(send_mail_addr))

def send_mail(mail_to, mail_from,server="localhost"):
    assert type(mail_to) == list
    msg = MIMEMultipart()
    msg['From'] = 'dev.robot@netis.com'
    msg['To'] = COMMASPACE.join(mail_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = '请更新Sprint P1 Plan'

    # 如果 text 是html，则需要设置 _subtype='html'
    # 默认情况下 _subtype='plain'，即纯文本
    # msg.attach(MIMEText(text, _subtype='html', _charset='utf-8'))
    text = """
        <html>
            <body>
                <p>请各位更新本Sprint的工作模式和P1 Plan'</br>
                <a href="https://confluence.netisdev.com/pages/viewpage.action?spaceKey=RD&title=2019+Sprint+P1+Complete">2019 Sprint P1 Complete</a></p>
            </body>
        </html>
    """
    msg.attach(MIMEText(text,  _subtype='html',_charset='utf-8'))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    send_mail(['sherry.zheng@netis.com'],['dev.robot@netis.com'])