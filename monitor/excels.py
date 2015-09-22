#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import xlsxwriter

import logging
log = logging.getLogger(__name__)

def make_excel_file(obj_type, columns, rows, fail=0):
     num_col = len(columns)
     num_row = len(rows)

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
          if obj_type == 'ciu' or 'power' in obj_type:
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
               num_col = 9
               for title in columns:
                    if row == 0 and col == 0:
                         # 시간
                         worksheet.merge_range(row, col, row+1, col, title.encode('utf-8'), merge_format)
                    elif row == 0 and col != 0:
                         # 관정센서 1~4
                         worksheet.merge_range(row, col, row, col+1, title.encode('utf-8'), merge_format)
                         col += 1
                    else:
                         # 수위, 온도
                         worksheet.write(row, col, title.encode('utf-8'), title_format)
                    col += 1
                    if col == num_col:
                         col = 1; row += 1;




          # Start from the first cell below the headers.
          # 내용
          if obj_type == 'ciu' or 'power' in obj_type or 'cop' in obj_type:
               row = 1
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
     # maybe permission denied error
          log.debug(str(e))
          fail += 1
          make_excel_file(obj_type, columns, rows, fail)

          
