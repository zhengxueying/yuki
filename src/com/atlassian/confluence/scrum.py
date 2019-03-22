#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import xmlrpclib
import sys,os
import click

CONFLUENCE_URL = "https://confluence.netisdev.com/rpc/xmlrpc"
CONFLUENCE_USER_NAME = "Sherry.Zheng"  
CONFLUENCE_PASSWORD = "zxy@918"  
PAGE_ID = '43340279'   # https://confluence.netisdev.com/display/RD/2019+Sprint+P1+Complete


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

@click.command()
@click.option('-n','--num',type=int)
def getAllTeamsInfoByNum(num):
    infos = getContentTables(loadConfluencePage(PAGE_ID))
    teaminfos = {}
    for team, info in infos.iteritems():
        teaminfos[team] = list(getScrumSP(info,num))
    for team, info in teaminfos.iteritems():
        if info[2] == 'Scrum':
            print info
    return teaminfos


if __name__ == "__main__":
    print getAllTeamsInfoByNum(5)
