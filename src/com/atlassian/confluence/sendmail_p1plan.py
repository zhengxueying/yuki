#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import os
import ConfigParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from bs4 import BeautifulSoup
import xmlrpclib
import sys

CONFLUENCE_URL = "https://confluence.netisdev.com/rpc/xmlrpc"
CONFLUENCE_USER_NAME = "Sherry.Zheng"  
CONFLUENCE_PASSWORD = "zxy@918"  
PAGE_ID = '43340279'   # https://confluence.netisdev.com/display/RD/2019+Sprint+P1+Complete

A_TEAM_MailAddr = 'timmy.yuan@netis.com'
L_TEAM_MailAddr = 'jacob.du@netis.com'
M_TEAM_MailAddr = 'ethan.zhou@netis.com'
N_TEAM_MailAddr = 'felix.zhu@netis.com'
W_TEAM_MailAddr = 'vincent.ye@netis.com'

def loadConfluencePage(pageID):
    
    client = xmlrpclib.Server(CONFLUENCE_URL,verbose=0)
    auth_token = client.confluence2.login(CONFLUENCE_USER_NAME,CONFLUENCE_PASSWORD)
    page = client.confluence2.getPage(auth_token,pageID)

    htmlContent = page['content']
    client.confluence2.logout(auth_token)
    # print htmlContent
    return htmlContent

def makeTableContentList(table):
     result = []
     allrows = table.findAll('tr')
     rowIndex = 0
     for row in allrows:
         result.append([])
         #exclude the strike one
         if row.findAll('s'):
             continue
 
         allcols = row.findAll('td')
         for col in allcols:
             #print "col",col
             thestrings = [unicode(s) for s in col.findAll(text=True)]
             thetext = ''.join(thestrings)
             result[-1].append(thetext)
         rowIndex += 1
     return result

def setDefaultEncodingUTF8():
     reload(sys)
     sys.setdefaultencoding('utf-8')

def getContentTables(content):
    setDefaultEncodingUTF8()
    soup = BeautifulSoup(content, 'html.parser')
    # print soup.prettify()
    tables = soup.findAll('table')
    team_infos = {
    'a_team' : makeTableContentList(tables[4]),
    'b_team' : makeTableContentList(tables[5]),
    'c_team' : makeTableContentList(tables[6]),
    'n_team' : makeTableContentList(tables[7]),
    'm_team' : makeTableContentList(tables[8]),
    'l_team' : makeTableContentList(tables[9]),
    'w_team' : makeTableContentList(tables[10]),
    # 'v_team' : makeTableContentList(tables[11])
    }
    return team_infos

def getScrumSP(team, sprint):
    sprint_info = team[sprint]
    start_date = sprint_info[4]
    sprint_name = sprint_info[8]
    sprint_mode = sprint_info[9]
    sprint_P1 = sprint_info[10]
    return start_date, sprint_name, sprint_mode, sprint_P1

def getAllTeamsInfoByNum(num):
    infos = getContentTables(loadConfluencePage(PAGE_ID))
    teaminfos = {}
    for team, info in infos.iteritems():
        teaminfos[team] = list(getScrumSP(info,num))
    # print teaminfos
    return teaminfos

def parse_sprint_date(sprint_date):
    filedir = os.path.split(os.path.realpath(__file__))[0]
    configPath = os.path.join(filedir, 'sprint_date_map.ini')
    config = ConfigParser.ConfigParser()
    config.read(configPath)
    if sprint_date in config.options('sprint_2019'):
        sprint_num = config.get('sprint_2019', sprint_date)
        return sprint_num   
    else:
        return None

def get_team_sprint_info(day):
    num = int(parse_sprint_date(day))
    return getAllTeamsInfoByNum(num)

def get_mail_addr(day):
    team_infos = get_team_sprint_info(day)
    blank_teams = []
    for team, info in team_infos.iteritems():
	if info[2] == 'Kanban':
	    pass
        if info[2] == '' or info[3] == '':
            blank_teams.append(team)
    # print blank_teams
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
    msg['From'] = 'sherry.zheng@netis.com'
    msg['To'] = COMMASPACE.join(mail_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = '请更新Sprint P1 Plan'

    text = """
        <html>
            <body>
                <p>请各位更新本Sprint的工作模式和P1 Plan，谢谢！
                <a href="https://confluence.netisdev.com/pages/viewpage.action?spaceKey=RD&title=2019+Sprint+P1+Complete">2019 Sprint P1 Complete</a></p>
            </body>
        </html>
    """
    msg.attach(MIMEText(text, _subtype='html', _charset='utf-8'))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.close()

if __name__ == "__main__":
    today = time.strftime("%y/%m/%d")
    if parse_sprint_date(today):
        mailto = get_mail_addr(today)
	# mailto.append('sherry.zheng@netis.com')
        send_mail(mailto,['sherry.zheng@netis.com'])
    else:
	pass
    # mailto = get_mail_addr(today)
    # mailto.append('sherry.zheng@netis.com')
    
    
