#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import xlsxwriter

import logging
log = logging.getLogger(__name__)

def make_excel_file(obj_type, columns, rows, fail=0):
     # html 화면에서 받아온 정보들
     num_col = len(columns)
     num_row = len(rows)

     # log.debug(rows)
     try:
          # Create a workbook and add a worksheet.
          # file_dir = u'C:/Users/hsinh_000/Desktop/지열 냉난방 시스템/'.encode('utf-8')
          import os, myproject.settings
          file_dir = os.path.join(myproject.settings.BASE_DIR, 'database/')

          if fail:
               filename = file_dir + obj_type + str(fail) + '.xlsx'
          else:
               # if obj_type == 'ciu':
               #      filename = file_dir + 'ciu실내기.xlsx'
               # elif obj_type == 'hp':
               #      filename = file_dir + '' + '히트펌프.xlsx'
               # elif obj_type == 'cp':
               #      filename = file_dir + '' + '순환펌프.xlsx'
               # elif obj_type == 'dwp':
               #      filename = file_dir + '' + '심정펌프.xlsx'
               # elif obj_type == 'fm-cur':
               #      filename = file_dir + '' + '유량계(순시).xlsx'
               # elif obj_type == 'fm-int':
               #      filename = file_dir + '' + '유량계(적산).xlsx'
               # elif obj_type == 'power-cur':
               #      filename = file_dir + '' + '전력량계(순시).xlsx'
               # elif obj_type == 'power-int':
               #      filename = file_dir + '' + '전력량계(적산).xlsx'
               # else:
               #      filename = file_dir + obj_type + '.xlsx'
               filename = file_dir + obj_type + '.xlsx'
          workbook = xlsxwriter.Workbook(filename)
          worksheet = workbook.add_worksheet()

          # Add a bold format to use to highlight cells.
          bold = workbook.add_format({'bold': 1})
          center = workbook.add_format({'align': 'center'})

          # Add Excel formats.
          title_format = workbook.add_format({
               'bold': True,
               'align': 'center',     
          })

          merge_format = workbook.add_format({
               'bold': True,
               'align': 'center',
               'valign': 'vcenter',
          })
          date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm'})
          # money_format = workbook.add_format({'num_format': '$#,##0'})

          # Adjust the column width.
          # set_column(start, end, width_pixel)
          worksheet.set_column(0, 0, 16)
          if obj_type == 'ciu':
               worksheet.set_column(2, 2, 13.5)
               worksheet.set_column(3, 8, 10)
          elif obj_type == 'hp':
               worksheet.set_column(1, 19, 8)
          elif obj_type == 'cp':
               worksheet.set_column(1, 9, 10.5)
          elif obj_type == 'dwp' or obj_type == 'fm-cur':
               worksheet.set_column(1, 13, 9.5)
          elif obj_type == 'fm-int':
               worksheet.set_column(1, 6, 17)
          elif 'power' in obj_type or obj_type == 'cop':
               worksheet.set_column(1, 1, 16.5)
          else: # 관측센서
               # worksheet.set_column()
               pass


          # Write some data headers.
          col = 0
          row = 0
          if obj_type == 'ciu' or 'power' in obj_type or 'cop' in obj_type:
               # 실내기 제목 / 전력량계 제목
               for title in columns:
                    worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1; 
          elif obj_type == 'hp':
               # 히트펌프 제목
               num_col = 19
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and col != 0:
                         # 히트펌프 1,2,3,4,5,6
                         worksheet.merge_range(row, col, row, col+2, title.encode('utf-8'), merge_format)
                         col += 2
                    else: 
                         # 동작상태, IN, OUT
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1
                    if col == num_col:
                         col = 1; row += 1;
          elif obj_type == 'cp':
               # 순환펌프 제목
               num_col = 9
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and col != 0:
                         # 순환펌프 1, 2
                         worksheet.merge_range(row, col, row, col+3, title.encode('utf-8'), merge_format)
                         col += 3
                    else: 
                         # 동작상태, 운전모드, 유량, 회전수
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1
                    if col == num_col:
                         col = 1; row += 1;
          elif obj_type == 'dwp':
               # 심정펌프 제목
               num_col = 13
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and col != 0:
                         # 심정펌프 1, 2, 3, 4
                         worksheet.merge_range(row, col, row, col+2, title.encode('utf-8'), merge_format)
                         col += 2
                    else: 
                         # 동작상태, 온도, 운전모드
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1
                    if col == num_col:
                         col = 1; row += 1;
          elif obj_type == 'fm-cur':
               # 유량계 제목
               num_col = 13
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and col != 0:
                         # 순환수(열교환 전/후), 지하수(양수/주입)
                         worksheet.merge_range(row, col, row, col+2, title.encode('utf-8'), merge_format)
                         col += 2
                    else: 
                         # 유량(ton/hr, lpm), 온도
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1
                    if col == num_col:
                         col = 1; row += 1;
          elif obj_type == 'fm-int':
               # 유량계 제목
               num_col = 5
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and col != 0:
                         # 순환수(열교환 전/후), 지하수(양수/주입)
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    else: 
                         # 유량
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1
                    if col == num_col:
                         col = 1; row += 1;
          elif obj_type == 'tw':
               # 관측센서
               num_col = 28
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+2, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and (col==1 or col==5 or col==14):
                         # ab, ij
                         worksheet.merge_range(row, col, row, col+3, title.encode('utf-8'), merge_format)
                         col += 3
                    elif row == 0 and (col==9 or col==18 or col==23):
                         # ib, sb
                         worksheet.merge_range(row, col, row, col+4, title.encode('utf-8'), merge_format)
                         col += 4
                    elif row == 1 and (col==1 or col==5 or col==9 or col==14 or col==18 or col==23):
                         # 수위
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 1:
                         # 수심
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    elif row == 2 and (col==1 or col==5 or col==9 or col==14 or col==18 or col==23):
                         # 온도
                         col += 1
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    else:
                         # 온도
                         worksheet.write(row, col, title.encode('utf-8'), title_format)

                    col += 1
                    if col == num_col:
                         col = 1; row += 1;




          # Start from the first cell below the headers.
          # 내용
          if obj_type == 'ciu' or 'power' in obj_type or 'cop' in obj_type:
               row = 1
          elif obj_type == 'tw':
               row = 3
          else:
               row = 2
          col = 0

          # write data
          for r in rows:
               for x in r:
                    # Convert the date string into a datetime object.
                    if col == 0:
                         worksheet.write(row,col,x,date_format)
                    if type(x) is 'str':
                         worksheet.write(row,col,''.join(x), center)
                    else:
                         worksheet.write(row,col,x, center)     
                    # worksheet.write(row,col+1,y)
                    # worksheet.write(row,col+2,z.encode('utf-8'))
                    col += 1
                    if col == num_col:
                         col = 0; row += 1;

               # worksheet.write_number  (row, col + 2, cost, money_format)
               # row += 1

          # Write a total using a formula.
          # worksheet.write(row, 0, 'Total', bold)
          # worksheet.write(row, 2, '=SUM(C2:C5)', money_format)

          workbook.close()
     except Exception, e:
          # if permission denied error
          # 지금은 일어나지 않음
          # log.debug(str(e))
          fail += 1
          # make_excel_file(obj_type, columns, rows, fail)

          
def rows_hp(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x[0].dateTime)[:-3]; j+=1
          # hp1
          row_mat[i][j] = str(x[0].switch); j+=1
          row_mat[i][j] = float(x[0].tempIn.temperature); j+=1
          row_mat[i][j] = float(x[0].tempOut.temperature); j+=1
          # hp2
          row_mat[i][j] = str(x[1].switch); j+=1
          row_mat[i][j] = float(x[1].tempIn.temperature); j+=1
          row_mat[i][j] = float(x[1].tempOut.temperature); j+=1
          # hp3
          row_mat[i][j] = str(x[2].switch); j+=1
          row_mat[i][j] = float(x[2].tempIn.temperature); j+=1
          row_mat[i][j] = float(x[2].tempOut.temperature); j+=1
          # hp4
          row_mat[i][j] = str(x[3].switch); j+=1
          row_mat[i][j] = float(x[3].tempIn.temperature); j+=1
          row_mat[i][j] = float(x[3].tempOut.temperature); j+=1
          # hp5
          row_mat[i][j] = str(x[4].switch); j+=1
          row_mat[i][j] = float(x[4].tempIn.temperature); j+=1
          row_mat[i][j] = float(x[4].tempOut.temperature); j+=1
          # hp6
          row_mat[i][j] = str(x[5].switch); j+=1
          row_mat[i][j] = float(x[5].tempIn.temperature); j+=1
          row_mat[i][j] = float(x[5].tempOut.temperature); j+=1
          i+=1;j=0;
     return row_mat
def rows_cp(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x[0].dateTime)[:-3]; j+=1
          # cp1
          row_mat[i][j] = str(x[0].switch); j+=1
          row_mat[i][j] = str(x[0].opMode); j+=1
          row_mat[i][j] = float(x[0].flux); j+=1
          row_mat[i][j] = float(x[0].Hz); j+=1
          # cp2
          row_mat[i][j] = str(x[1].switch); j+=1
          row_mat[i][j] = str(x[1].opMode); j+=1
          row_mat[i][j] = float(x[1].flux); j+=1
          row_mat[i][j] = float(x[1].Hz); j+=1
          i+=1;j=0;
     return row_mat
def rows_dwp(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x[0].dateTime)[:-3]; j+=1
          # dwp1
          row_mat[i][j] = str(x[0].switch); j+=1
          row_mat[i][j] = float(x[4].temperature); j+=1
          row_mat[i][j] = str(x[0].opMode); j+=1
          # dwp2
          row_mat[i][j] = str(x[1].switch); j+=1
          row_mat[i][j] = float(x[4].temperature); j+=1
          row_mat[i][j] = str(x[1].opMode); j+=1
          # dwp3
          row_mat[i][j] = str(x[2].switch); j+=1
          row_mat[i][j] = float(x[4].temperature); j+=1
          row_mat[i][j] = str(x[2].opMode); j+=1
          # dwp4
          row_mat[i][j] = str(x[3].switch); j+=1
          row_mat[i][j] = float(x[4].temperature); j+=1
          row_mat[i][j] = str(x[3].opMode); j+=1
          i+=1;j=0;
     return row_mat
def rows_fm_cur(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x[0].dateTime)[:-3]; j+=1
          # 순환수 열교환 후
          row_mat[i][j] = float(x[0].currentFlux/16.67); j+=1
          row_mat[i][j] = int(x[0].currentFlux); j+=1
          row_mat[i][j] = float(x[4].temperature); j+=1
          # 순환수 열교환 전
          row_mat[i][j] = float(x[0].currentFlux/16.67); j+=1
          row_mat[i][j] = int(x[0].currentFlux); j+=1
          row_mat[i][j] = float(x[2].temperature); j+=1
          # 지하수 공급(양수)
          row_mat[i][j] = float(x[1].currentFlux); j+=1
          row_mat[i][j] = float(x[1].currentFlux*16.67); j+=1
          row_mat[i][j] = float(x[3].temperature); j+=1
          # 지하수 환수(주입)
          row_mat[i][j] = float(x[1].currentFlux); j+=1
          row_mat[i][j] = float(x[1].currentFlux*16.67); j+=1
          row_mat[i][j] = float(x[5].temperature); j+=1
          i+=1;j=0;
     return row_mat
def rows_fm_int(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x[0].dateTime)[:-3]; j+=1
          # 순환수 열교환 후
          row_mat[i][j] = float(x[0].integralFlux/1000); j+=1
          # 순환수 열교환 전
          row_mat[i][j] = float(x[0].integralFlux/1000); j+=1
          # 지하수 공급(양수)
          row_mat[i][j] = float(x[1].integralFlux); j+=1
          # 지하수 환수(주입)
          row_mat[i][j] = float(x[1].integralFlux); j+=1
          i+=1;j=0;
     return row_mat
def rows_tw(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x[0].dateTime)[:-3]; j+=1
          # ab1
          row_mat[i][j] = float(x[0].level); j+=1
          row_mat[i][j] = float(x[0].temp10); j+=1
          row_mat[i][j] = float(x[0].temp20); j+=1
          row_mat[i][j] = float(x[0].temp30); j+=1
          # ab2
          row_mat[i][j] = float(x[1].level); j+=1
          row_mat[i][j] = float(x[1].temp10); j+=1
          row_mat[i][j] = float(x[1].temp20); j+=1
          row_mat[i][j] = float(x[1].temp30); j+=1
          # ib1
          row_mat[i][j] = float(x[2].level); j+=1
          row_mat[i][j] = float(x[2].temp10); j+=1
          row_mat[i][j] = float(x[2].temp30); j+=1
          row_mat[i][j] = float(x[2].temp50); j+=1
          row_mat[i][j] = float(x[2].temp70); j+=1
          # ij1
          row_mat[i][j] = float(x[3].level); j+=1
          row_mat[i][j] = float(x[3].temp10); j+=1
          row_mat[i][j] = float(x[3].temp30); j+=1
          row_mat[i][j] = float(x[3].temp50); j+=1
          # sb1
          row_mat[i][j] = float(x[4].level); j+=1
          row_mat[i][j] = float(x[4].temp10); j+=1
          row_mat[i][j] = float(x[4].temp15); j+=1
          row_mat[i][j] = float(x[4].temp20); j+=1
          row_mat[i][j] = float(x[4].temp25); j+=1
          # sb2
          row_mat[i][j] = float(x[5].level); j+=1
          row_mat[i][j] = float(x[5].temp10); j+=1
          row_mat[i][j] = float(x[5].temp15); j+=1
          row_mat[i][j] = float(x[5].temp20); j+=1
          row_mat[i][j] = float(x[5].temp25); j+=1
          i+=1;j=0;
     return row_mat
def rows_power_cur(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
          # 순시전력
          row_mat[i][j] = float(x.currentPowerConsumption); j+=1
          i+=1;j=0;
     return row_mat
def rows_power_int(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
          # 적산전력
          row_mat[i][j] = float(x.integralPowerConsumption); j+=1
          i+=1;j=0;
     return row_mat
def rows_cop(n_col, n_row, data):
     row_mat = [[None for x in range(n_col)] for x in range(n_row)]
     i=0;j=0;
     for x in data:
          if j == 0:
               row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
          # COP
          row_mat[i][j] = float(x.COP); j+=1
          i+=1;j=0;
     return row_mat
def rows_ciu(n_col, n_row, data):
     # log.debug(n_row)
     # log.debug(len(data))
     # log.debug(len(data[0]))
     # log.debug(len(data[0][0]))


     i=0;j=0;
     if len(data) == 1:
          # 단일 실내기 검색 결과
          row_mat = [[None for x in range(n_col)] for x in range(n_row+1)]
          try:
               for x in data[0]:
                    if j == 0:
                         row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
                    # 층 수
                    row_mat[i][j] = int(x.floor); j+=1
                    row_mat[i][j] = str(x.get_location_display()); j+=1
                    row_mat[i][j] = str(x.switch); j+=1
                    row_mat[i][j] = float(x.setTemp); j+=1
                    row_mat[i][j] = float(x.temperature); j+=1
                    row_mat[i][j] = str(x.opMode); j+=1
                    i+=1;j=0;
          except:
               # log.debug(str(i) +', ' + str(j))
               pass
     elif len(data) == 14:
          # 층 별 실내기 검색 결과 - 1층
          # log.debug("1floor")
          row_mat = [[None for x in range(n_col)] for x in range((n_row+1)*14)]
          try:
               for d in data:
                    for x in d:
                         if j == 0:
                              row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
                         row_mat[i][j] = int(x.floor); j+=1
                         row_mat[i][j] = str(x.get_location_display()); j+=1
                         row_mat[i][j] = str(x.switch); j+=1
                         row_mat[i][j] = float(x.setTemp); j+=1
                         row_mat[i][j] = float(x.temperature); j+=1
                         row_mat[i][j] = str(x.opMode); j+=1
                         i+=1;j=0;
          except:
               # log.debug(str(i) +', ' + str(j))
               pass
     elif len(data) == 12:
          # 층 별 실내기 검색 결과 - 2,3층
          # log.debug("2-3floor")
          row_mat = [[None for x in range(n_col)] for x in range((n_row+1)*12)]
          try:
               for d in data:
                    for x in d:
                         if j == 0:
                              row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
                         row_mat[i][j] = int(x.floor); j+=1
                         row_mat[i][j] = str(x.get_location_display()); j+=1
                         row_mat[i][j] = str(x.switch); j+=1
                         row_mat[i][j] = float(x.setTemp); j+=1
                         row_mat[i][j] = float(x.temperature); j+=1
                         row_mat[i][j] = str(x.opMode); j+=1
                         i+=1;j=0;
          except:
               # log.debug(str(i) +', ' + str(j))
               pass
     elif len(data) == 3:
          # 전체 실내기 검색 결과
          # log.debug("all")
          row_mat = [[None for x in range(n_col)] for x in range((n_row+1)*(14+12+12))]
          try:
               for floor in data:
                    for d in floor:
                         for x in d:
                              if j == 0:
                                   row_mat[i][j] = str(x.dateTime)[:-3]; j+=1
                              row_mat[i][j] = int(x.floor); j+=1
                              row_mat[i][j] = str(x.get_location_display()); j+=1
                              row_mat[i][j] = str(x.switch); j+=1
                              row_mat[i][j] = float(x.setTemp); j+=1
                              row_mat[i][j] = float(x.temperature); j+=1
                              row_mat[i][j] = str(x.opMode); j+=1
                              i+=1;j=0;
          except:
               # log.debug(str(i) +', ' + str(j))
               pass
     else:
          # log.debug("??")
          pass
     return row_mat

def make_rows(obj, n_col, n_row, data):
     if obj == 'hp':
          return rows_hp(n_col, n_row, data)
     elif obj == 'cp':
          return rows_cp(n_col, n_row, data)
     elif obj == 'dwp':
          return rows_dwp(n_col, n_row, data)
     elif obj == 'fm-cur':
          return rows_fm_cur(n_col, n_row, data)
     elif obj == 'fm-int':
          return rows_fm_int(n_col, n_row, data)
     elif obj == 'tw':
          return rows_tw(n_col, n_row, data)
     elif obj == 'power-cur':
          return rows_power_cur(n_col, n_row, data)
     elif obj == 'power-int':
          return rows_power_int(n_col, n_row, data)
     elif obj == 'cop':
          return rows_cop(n_col, n_row, data)
     else: # ciu
          return rows_ciu(n_col, n_row, data)

