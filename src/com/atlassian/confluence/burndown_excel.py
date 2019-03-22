#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlsxwriter
import os
import xlrd

filedir = os.path.split(os.path.realpath(__file__))[0]
excel_file = os.path.join(filedir, '../../../../data/excel/burndown.xlsx')

def edit_burndown_chart():
    # workbook = xlsxwriter.Workbook(excel_file)
    # sheet_bhor = workbook.get_worksheet_by_name('DP')
    # # sheet_bhor.set_landscape()  #设置为横向
    # print sheet_bhor
    # # sheet_bhor.set_paper(8)   #设置为A3

    xls = xlrd.open_workbook(excel_file,on_demand=True)
    teams = xls.sheet_names()
    for team in teams:
        team_sheet = xls.sheet_by_name(team)
        print team_sheet.nrows, team_sheet.ncols

if __name__ == "__main__":
    edit_burndown_chart()
