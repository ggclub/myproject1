#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
import simplejson as json
from django.core import serializers, management
from django.utils import timezone
from datetime import datetime as dt
import os, myproject.settings
from os.path import isfile
from django.db.models import Q
from .models import *
from .excels import make_excel_file
import controller
from django.views.decorators.csrf import csrf_exempt


import logging
log = logging.getLogger(__name__)

op_mode = 'MN'
temp_mode = 'CL'
flag_command = 0
flag_reload_display = False
file_path = os.path.join(myproject.settings.BASE_DIR, 'share/')
save_time = timezone.now()
# 저장 주기
save_interval = 10	# minutes
is_saved = False
total_rt = 0.0

date_format = "%Y-%m-%d"

@csrf_exempt
@login_required
def index(request):
	request.session.set_expiry(0)
	request.session['name'] = 'admin'
	# log.debug(str(request.session['name']))

	log.debug("index: program started.")
	check_if_error_exist(request)
	global op_mode, temp_mode
	op_mode = 'MN'
	temp_mode = 'CL'

	response_data = {}
	
	# 실내기 db
	floor = request.POST.get('floor','1')
	response_data.update(controller.get_CIU_from_json(floor))
	response_data.update({'floor':floor})
	check_rt = response_data["cooling_rt"]

	# ciu - hp
	no_hp = request.POST.get('no_hp','1')
	# response_data.update(controller.get_CIU_on_HP(no_hp))
	response_data.update(controller.get_CIU_on_HP_from_json(no_hp))

	# 센서값 읽어오기
	response_data.update(controller.read_data_from_json(op_mode, temp_mode, total_rt))
	# if response_data == False:
	# 	response_data = {"error":"file read error"}
	# 	url = 'error/read.html'
	# 	return render(request, url, response_data)


	# 기기 동작 내역
	selected = int(request.POST.get('page', 1))
	response_data.update(controller.get_operation_log(selected))

	# csrf token
	response_data.update(csrf(request))
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/index.html'
	return render(request, url, response_data)


def check_if_error_exist(request):
	file = file_path + 'errorlog.json'
	if isfile(file):
		with open(file) as data_file:
			response_data = json.load(data_file)
		os.remove(file)
		log.error(str(response_data))
		# url = 'error/errorlog.html'
		# html = render_to_string(url, response_data, RequestContext(request))
		# return HttpResponse(html)

def save_data(response_data):
	if not controller.save_data(response_data):
		# DB save 에러
		log.error("DB save error.")
	else :
		response_data.update(controller.get_CIU_from_json('1'))
		controller.save_ciu1(response_data)
		response_data.update(controller.get_CIU_from_json('2'))
		controller.save_ciu2(response_data)
		response_data.update(controller.get_CIU_from_json('3'))
		controller.save_ciu3(response_data)
		log.debug("database updated")
		save_time = timezone.now()


@csrf_exempt
@login_required
def reload_display(request):
	# 5초마다 갱신해서 왼쪽 상태창, 오른쪽 실내기 정보 갱신
	# 자동제어시, 자동제어 로직에 따라 hmi에 명령을 줌
	# 수동인 경우 데이터 값만 갱신함.
	response_data = {}
	# check if error exist
	check_if_error_exist(request)
	

	# 실내기 정보 읽어오기
	floor = request.POST.get('floor','1')
	response_data.update(controller.get_CIU_from_json(floor))
	response_data.update({'floor':floor})
	total_rt = response_data["cooling_rt"]
	# log.debug("total_rt: " + str(total_rt))

	# ciu - hp
	no_hp = request.POST.get('no_hp','1')
	response_data.update(controller.get_CIU_on_HP_from_json(no_hp))
	
	global flag_command 
	if flag_command: # command를 준 후에 파일을 잠시 읽지 않는다.
		import time
		time.sleep(3)
		flag_command = 0

	# 센서값 읽어오기
	global op_mode, temp_mode, flag_reload_display
	# log.debug("reload_display: " + op_mode + ", " + temp_mode)
	if flag_reload_display:
		op_mode = request.POST.get('opMode', 'error').encode('utf-8')
		temp_mode = request.POST.get('tempMode','error').encode('utf-8')
		# log.debug(op_mode + ", " + temp_mode)
		flag_reload_display = False
	# 데이터 읽고, (자동)제어, 수동인 경우 데이터 값만 갱신함.
	response_data.update(controller.read_data_from_json(op_mode, temp_mode, total_rt))
	if response_data.has_key("error"):
		log.debug("read_data_from_json error")
	# 	response_data = {"error":"file read error"}
	# 	url = 'error/read.html'
	# 	html = render_to_string(url, response_data)
	# 	return HttpResponse(html)

	# 기기 동작 내역
	# selected = int(request.POST.get('page', 1))
	# response_data.update(controller.get_operation_log(selected))


	# save time 주기마다 DB에 저장
	global save_time
	# log.debug("save_time: " + str(save_time))
	# if (timezone.now() - save_time) > timezone.timedelta(minutes=save_interval):
		# log.debug(timezone.now() - save_time)
	global is_saved
	t = timezone.now()
	# log.debug(str(t))	
	if save_interval == 10:
		if t.minute % 10 == 0 and t.second < 6: 
			save_data(response_data)
	elif save_interval == 30:
		if t.minute % 30 == 0 and t.second < 6:
			save_data(response_data)
	elif save_interval == 60:
		if t.minute == 0 and t.second < 6:
			save_data(response_data)
	else:
		if t.minute % 5 == 0 and t.second < 6:
			save_data(response_data)



	# log.debug(response_data)
	page = request.POST.get('page','error')
	if page == 'fullscreen':
		url = 'monitor/container.html'
	elif page == 'control':
		url = 'monitor/content_control.html'
	else:
		url = 'monitor/container.html'

	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def specs(request):
	response_data = controller.get_device_specs()
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/specs.html'
	return render(request, url, response_data)

@login_required
def setting_cp(request):
	# 순환펌프 설정을 눌렀을 때 뜨는 페이지
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	response_data.update(controller.read_cp_operating())

	url = 'monitor/setting_cp.html'
	return render(request, url, response_data)

@login_required
def setting_cp_done(request):
	# 순환펌프 동작을 설정했을 때 적용
	response_data = {}

	global op_mode, temp_mode
	op_mode = request.POST.get('opMode', 'error').encode('utf-8')
	if op_mode == 'error':
		log.debug("setting_cp_done, op_mode: error")
	temp_mode = request.POST.get('tempMode', 'error').encode('utf-8')
	if temp_mode == 'error':
		log.debug("setting_cp_done, temp_mode: error")

	cp_operating = int(request.POST.get('cpOperating',0))
	cp1switch = request.POST.get('cp1switch', 'error').encode('utf-8')
	cp1hz = int(request.POST.get('cp1hz', 0))
	cp1flux = int(request.POST.get('cp1flux', 0))
	cp2switch = request.POST.get('cp2switch', 'error').encode('utf-8')
	cp2hz = int(request.POST.get('cp2hz', 0))
	cp2flux = int(request.POST.get('cp2flux', 0))

	# 설정 값 db에 저장
	controller.set_cp(1, op_mode, cp1switch, cp1hz, cp1flux)
	controller.set_cp(2, op_mode, cp2switch, cp2hz, cp2flux)
	# cmdmain에 기록
	# ######## 	controller.write_cmd(temp_mode, op_mode)
	cp1 = CirculatingPump1Logger.objects.latest('id')
	cp2 = CirculatingPump2Logger.objects.latest('id')
	dwp1 = DeepwellPump1Logger.objects.latest('id')
	dwp2 = DeepwellPump2Logger.objects.latest('id')
	dwp3 = DeepwellPump3Logger.objects.latest('id')
	dwp4 = DeepwellPump4Logger.objects.latest('id')
	rt = RefrigerationTonLogger.objects.latest('id')
	datetime = str(timezone.now())[:-7]
	if cp1.switch == "OFF":
		cp1.Hz = 0
		cp1.flux = 0
	if cp2.switch == "OFF":
		cp2.Hz = 0
		cp2.flux = 0
	cmd_text = {
		'temp_mode': temp_mode,
		'op_mode': op_mode,
		'cp_operating': cp_operating,
		'cp1': cp1.switch,
		'cp1_hz': cp1.Hz,
		'cp1_flux': cp1.flux,
		'cp2': cp2.switch,
		'cp2_hz': cp2.Hz,
		'cp2_flux': cp2.flux,
		'dwp1': dwp1.switch,
		'dwp2': dwp2.switch,
		'dwp3': dwp3.switch,
		'dwp4': dwp4.switch,
		'datetime':datetime,
		'rt': rt.RT,
	}
	log.debug("command written")
	log.debug(cmd_text)
	log.debug("write_cmd from setting_cp_done")
	try:
		with open(file_path + 'cmdmain.json', 'w') as fp:
			json.dump(cmd_text, fp)
	except Exception, e:
		log.error(str(e))

	# check if error exist
	check_if_error_exist(request)

	global flag_command 
	if flag_command: # command를 준 후에 파일을 잠시 읽지 않는다.
		import time
		time.sleep(2)
		flag_command = 0

	# 센서값 읽어오기
	response_data = controller.read_data_from_json(op_mode, temp_mode, total_rt)
	# if response_data == False:
	# 	response_data = {"error":"file read error"}
	# 	url = 'error/read.html'
	# 	html = render_to_string(url, response_data)
	# 	return HttpResponse(html)

	# 기기 동작 내역
	selected = int(request.POST.get('page', 1))
	response_data.update(controller.get_operation_log(selected))
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})

	html = render_to_string('monitor/container.html', response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def show_database(request):
	# 지금 안쓰임
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/show_database.html'
	return render(request, url, response_data)

@login_required
def page_request(request):
	if not request.POST:
		return render_to_response('monitor/container.html',context_instance=RequestContext(request))

	# 기기 동작 내역
	selected = int(request.POST.get('page', 1))
	response_data = controller.get_operation_log(selected)

	html = render_to_string('monitor/right_bottom.html', response_data, RequestContext(request))
    	return HttpResponse(html)

@login_required
def toggle_switch(request):
	# 동작제어에서 심정펌프 스위치 on/off 버튼 클릭시 제어
	if not request.POST:
		return render_to_response('monitor/container.html', context_instance=RequestContext(request))

	location = request.POST.get('id', 'error').split('-')[0]
	loc = location.upper()
	switch_status = request.POST.get('status', 'error').encode('utf-8').upper()
	if switch_status == 'error':
		log.debug("toggle_switch, switch_status: error")

	global op_mode, temp_mode
	op_mode = request.POST.get('opMode', 'error').encode('utf-8')
	if op_mode == 'error':
		log.debug("toggle_switch, op_mode: error")
	temp_mode = request.POST.get('tempMode', 'error').encode('utf-8')
	if temp_mode == 'error':
		log.debug("toggle_switch, temp_mode: error")

	# 심정 펌프 갱신
	dwp = ''
	if loc == 'DWP1': 
		dwp = DeepwellPump1Logger(
			dateTime=timezone.now(), opMode=op_mode, switch=switch_status
		)
	elif loc == 'DWP2':
		dwp = DeepwellPump2Logger(
			dateTime=timezone.now(), opMode=op_mode, switch=switch_status
		)
	elif loc == 'DWP3':
		dwp = DeepwellPump3Logger(
			dateTime=timezone.now(), opMode=op_mode, switch=switch_status
		)
	elif loc == 'DWP4':
		dwp = DeepwellPump4Logger(
			dateTime=timezone.now(), opMode=op_mode, switch=switch_status
		)
	if dwp != '':
		dwp.save()


	# 기기 동작 내역 갱신
	try:
		new_cmd = OperationSwitchControl(
				dateTime=timezone.now(), location=loc, switch=switch_status
			)
		new_cmd.save()
	except Exception, e:
		log.error(str(e))

	# 커맨드 파일 작성
	controller.write_cmd(temp_mode, op_mode)
	log.debug("write_cmd from toggle_switch")
	# 커맨드 후 hmidata를 잠시동안 읽지 않는다.
	global flag_command 
	flag_command = int(request.POST.get('flag_command', '0'))

	# 기기 동작 내역
	response_data = controller.get_operation_log(1)

	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	html = render_to_string('monitor/right_top.html', response_data, RequestContext(request))
	return HttpResponse(html)


def floor_change(request):
	if not request.POST:
		return render_to_response('monitor/container.html', context_instance=RequestContext(request))

	response_data = {}
	# 실내기 정보 읽어오기
	floor = request.POST.get('floor', '1')
	response_data.update(controller.get_CIU_from_json(floor))
	response_data.update({'floor':floor})
	total_rt = response_data["cooling_rt"]
	
	html = render_to_string('monitor/right_bottom.html', response_data, RequestContext(request))
	return HttpResponse(html)


def change_ciuonhp(request):
	if not request.POST:
		return render_to_response('monitor/container.html', context_instance=RequestContext(request))

	response_data = {}
	# ciu - hp 정보
	no_hp = request.POST.get('no_hp','1')
	response_data.update(controller.get_CIU_on_HP_from_json(no_hp))

	html = render_to_string('monitor/right_top.html', response_data, RequestContext(request))
	return HttpResponse(html)


@login_required
def setting_mode(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/setting_mode.html'
	html = render_to_response(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def setting_mode_confirm(request):
	global op_mode, temp_mode
	op_mode_local = request.POST.get('opMode', 'error')
	if op_mode_local == 'error':
		log.debug("setting_mode_confirm, op_mode: error")
	temp_mode = request.POST.get('tempMode', 'error')
	if temp_mode == 'error':
		log.debug("setting_mode_confirm, temp_mode: error")

	# log.debug("setting_mode_confirm: " + op_mode + ", " + temp_mode)
	if op_mode != op_mode_local:
		op_mode = op_mode_local
		controller.write_cmd(temp_mode,op_mode)
		log.debug("write_cmd from settimg_mode_confirm")

	# check if error exist
	check_if_error_exist(request)

	if op_mode == 'AT':
		# log.debug("setting_mode_confirm: " + op_mode + ", " + temp_mode)
		global	flag_reload_display
		flag_reload_display = True
		# 전체화면
		return reload_display(request)
	else :# op_mode == 'MN'
		# 동작제어화면
		return operation_control(request)

@login_required	
def operation_control(request):
	response_data = {}
	# RT 값을 받기 위해 get_ciu_from_json 필요
	response_data.update(controller.get_CIU_from_json(1))
	total_rt = response_data["cooling_rt"]

	response_data.update(controller.read_data_from_json(op_mode, temp_mode, total_rt))
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)

	if response_data.has_key("error"):
		log.debug("read_data_from_json error")
	# 	log.debug("error")
	# 	response_data = {"error":"file read error"}
	# 	url = 'error/read.html'
	# 	html = render_to_string(url, response_data)
	# 	return HttpResponse(html)

	url = 'monitor/operation_control.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)


###################### DB 검색 ######################

def search_db_excel(request):
	obj_type = request.POST.get('objType','error')
	columns = request.POST.get('columns', 'error').encode('utf-8')
	rows = request.POST.get('rows', 'error').encode('utf-8')
	num_row = int(request.POST.get('numRow', 'error'))
	num_col = int(request.POST.get('numCol', 'error'))

	col_mat = columns.replace('"', '').replace('[', '').replace(']', '').split(",")
	row_split = rows.replace('"', '').replace('[', '').replace(']', '').split(",")
	row_mat = [[None for x in range(num_col)] for x in range(num_row)]

	i=0;j=0;
	for r in row_split:
		if '.' in r:
			# type = float
			row_mat[i][j] = float(r)
		elif r.isdigit():
			row_mat[i][j] = int(r)
		else:
			row_mat[i][j] = r
		j += 1
		if j == num_col:
			j = 0; i += 1;


	make_excel_file(obj_type, col_mat, row_mat)


	# log.debug(col)
	# log.debug(rows)
	# log.debug(row_mat)
	# log.debug(row_list)

	response_data = {	}

	# return download_file(request, 'ciu')
	return HttpResponse(json.dumps(response_data), content_type="application/json")


import mimetypes
from django.core.servers.basehttp import FileWrapper
def download_file(request, name='database'):
	file_dir = os.path.join(myproject.settings.BASE_DIR, 'database\\')
	filename = file_dir + name + '.xlsx'
	wrapper = FileWrapper(file(filename))

	fp = open(filename, 'rb')
	response = HttpResponse(fp.read())
	fp.close()

	type, encoding = mimetypes.guess_type(name+'.xlsx')
	if type is None:
		type = 'application/octet-stream'
	response['Content-Type'] = type
	# response['Content-Length'] = str(os.stat(file_path).st_size)
	if encoding is not None:
		response['Content-Encoding'] = encoding


	if u'WebKit' in request.META['HTTP_USER_AGENT']:
		# Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
		filename_header = 'filename=%s' % name+'.xlsx'.encode('utf-8')
	elif u'MSIE' in request.META['HTTP_USER_AGENT']:
		# IE does not support internationalized filename at all.
		# It can only recognize internationalized URL, so we do the trick via routing rules.
		filename_header = ''
	else:
		# For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
		filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(name+'.xlsx'.encode('utf-8'))


	# response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=' + filename_header
	# response['Content-Length'] = str(os.stat(file_path).st_size)
	response['Content-Length'] = os.path.getsize(filename)
	# log.debug(str(response['Content-Length']))

	return response


def search_db_ciu(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/search_db_ciu.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_ciu_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)

	floor = request.POST.get('floor', '0')
	name = request.POST.get('name', '0')
	count = 0

	if floor == '1':
		if name == '1':
			database = Floor1CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		elif name == '2':
			database = Floor1CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		elif name == '3':
			database = Floor1CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '4':
			database = Floor1CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '5':
			database = Floor1CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '6':
			database = Floor1CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '7':
			database = Floor1CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '8':
			database = Floor1CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '9':
			database = Floor1CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '10':
			database = Floor1CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '11':
			database = Floor1CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '12':
			database = Floor1CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '13':
			database = Floor1CIU13.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '14':
			database = Floor1CIU14.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		else: # (전체)
			d1 = Floor1CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
			d2 = Floor1CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
			d3 = Floor1CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d4 = Floor1CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d5 = Floor1CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d6 = Floor1CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d7 = Floor1CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d8 = Floor1CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d9 = Floor1CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d10 = Floor1CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d11 = Floor1CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d12 = Floor1CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d13 = Floor1CIU13.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d14 = Floor1CIU14.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			database1 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14]
			for d in database1:
				count += d.count()
			response_data = {
				"database":database1,
				"count":count,
			}

	elif floor == '2':
		if name == '1':
			database = Floor2CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		elif name == '2':
			database = Floor2CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		elif name == '3':
			database = Floor2CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '4':
			database = Floor2CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '5':
			database = Floor2CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '6':
			database = Floor2CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '7':
			database = Floor2CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '8':
			database = Floor2CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '9':
			database = Floor2CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '10':
			database = Floor2CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '11':
			database = Floor2CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '12':
			database = Floor2CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		else: # (전체)
			d1 = Floor2CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
			d2 = Floor2CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
			d3 = Floor2CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d4 = Floor2CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d5 = Floor2CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d6 = Floor2CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d7 = Floor2CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d8 = Floor2CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d9 = Floor2CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d10 = Floor2CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d11 = Floor2CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d12 = Floor2CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			database2 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
			for d in database2:
				count += d.count()
			response_data = {
				"database":database2,
				"count":count,
			}
	elif floor == '3':
		if name == '1':
			database = Floor3CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		elif name == '2':
			database = Floor3CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		elif name == '3':
			database = Floor3CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '4':
			database = Floor3CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '5':
			database = Floor3CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '6':
			database = Floor3CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '7':
			database = Floor3CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '8':
			database = Floor3CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '9':
			database = Floor3CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '10':
			database = Floor3CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '11':
			database = Floor3CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		elif name == '12':
			database = Floor3CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		else: # (전체)
			d1 = Floor3CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
			d2 = Floor3CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
			d3 = Floor3CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d4 = Floor3CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d5 = Floor3CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d6 = Floor3CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d7 = Floor3CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d8 = Floor3CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d9 = Floor3CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d10 = Floor3CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d11 = Floor3CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			d12 = Floor3CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
			database3 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
			for d in database3:
				count += d.count()
			response_data = {
				"database":database3,
				"count":count,
			}
	else: # (전체)
		d1 = Floor1CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		d2 = Floor1CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		d3 = Floor1CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d4 = Floor1CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d5 = Floor1CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d6 = Floor1CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d7 = Floor1CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d8 = Floor1CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d9 = Floor1CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d10 = Floor1CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d11 = Floor1CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d12 = Floor1CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d13 = Floor1CIU13.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d14 = Floor1CIU14.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		database1 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14]
		d1 = Floor2CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		d2 = Floor2CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		d3 = Floor2CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d4 = Floor2CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d5 = Floor2CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d6 = Floor2CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d7 = Floor2CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d8 = Floor2CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d9 = Floor2CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d10 = Floor2CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d11 = Floor2CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d12 = Floor2CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		database2 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
		d1 = Floor3CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		d2 = Floor3CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
		d3 = Floor3CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d4 = Floor3CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d5 = Floor3CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d6 = Floor3CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d7 = Floor3CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d8 = Floor3CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d9 = Floor3CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d10 = Floor3CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d11 = Floor3CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		d12 = Floor3CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		database3 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
		database_list = [database1,database2,database3]
		for d in database1:
			count += d.count()
		for d in database2:
			count += d.count()
		for d in database3:
			count += d.count()
		response_data = {
			"database_list":database_list,
			"count":count,
		}

	if 'response_data' not in locals():
		count += database.count()
		response_data = {
			"database":[database],
			"count":count,
		}

	# log.debug("found: " + str(count))
	url = 'monitor/search_db_ciu_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_hp(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/search_db_hp.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_hp_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)
	name = request.POST.get('name', '0')
	count = 0

	hp1 = HeatPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
	hp2 = HeatPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
	hp3 = HeatPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
	hp4 = HeatPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
	hp5 = HeatPump5Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
	hp6 = HeatPump6Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
	count += hp1.count()

	database_list = zip(list(hp1), list(hp2), list(hp3), list(hp4), list(hp5), list(hp6))
	response_data = {
		'database_list':database_list,
		'count': count,
	}

	url = 'monitor/search_db_hp_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_cp(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/search_db_cp.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_cp_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)
	name = request.POST.get('name', '0')
	count = 0

	cp1 = CirculatingPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	cp2 = CirculatingPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	count += cp1.count()

	database_list = zip(list(cp1), list(cp2))
	response_data = {
		'database_list':database_list,
		'count': count,
	}

	url = 'monitor/search_db_cp_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_dwp(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/search_db_dwp.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_dwp_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)
	name = request.POST.get('name', '0')
	count = 0

	dwp1 = DeepwellPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	dwp2 = DeepwellPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	dwp3 = DeepwellPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	dwp4 = DeepwellPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	temp = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	count += dwp1.count()

	database_list = zip(list(dwp1), list(dwp2), list(dwp3), list(dwp4), list(temp))
	response_data = {
		'database_list':database_list,
		'count': count,
	}

	url = 'monitor/search_db_dwp_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_fm(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/search_db_fm.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_fm_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)
	name = request.POST.get('name', '0')
	count = 0

	cpfm = CPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	dwpfm = DWPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	hein1 = TempHEIn1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	hein2 = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	heout1 = TempHEOut1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	heout2 = TempHEOut2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	count += cpfm.count()
	database_list = zip(list(cpfm), list(dwpfm), list(hein1), list(hein2), list(heout1), list(heout2))

	# 적산유량
	cpfm2 = []; dwpfm2 = [];
	count_int = 0
	
	# 검색할 날짜 리스트
	start = dt.strptime(start_date, date_format)
	end = dt.strptime(end_date, date_format) - timezone.timedelta(days=1)
	num_date = end - start
	date_list = [end - timezone.timedelta(days=x) for x in range(num_date.days+1)]
	# log.debug(str(date_list))
	for date in date_list:
		d = dt.strftime(date, date_format)
		try:
			cpfm2.append(CPFlowmeterLogger.objects.filter(Q(dateTime__day=date.day)).latest('dateTime'))
			dwpfm2.append(DWPFlowmeterLogger.objects.filter(Q(dateTime__day=date.day)).latest('dateTime'))
		except:
			pass
	count_int = len(cpfm2)
	database_list_int = zip(cpfm2, dwpfm2)

	response_data = {
		'database_list': database_list,
		'database_list_int': database_list_int,
		'count': count,
		'count_int': count_int,
	}

	url = 'monitor/search_db_fm_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_power(request):
	response_data = {}
	global op_mode, temp_mode
	response_data.update({"op_mode":op_mode, "temp_mode":temp_mode})
	# log.debug(op_mode + ", " + temp_mode)
	url = 'monitor/search_db_power.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def search_db_power_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)
	name = request.POST.get('name', '0')
	count = 0

	power = PowerConsumptionLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	count += power.count()
	database_list = list(power)

	# 적산유량
	power2 = [];
	count_int = 0
	
	# 검색할 날짜 리스트
	start = dt.strptime(start_date, date_format)
	end = dt.strptime(end_date, date_format) - timezone.timedelta(days=1)
	num_date = end - start
	date_list = [end - timezone.timedelta(days=x) for x in range(num_date.days+1)]
	# log.debug(str(date_list))
	for date in date_list:
		d = dt.strftime(date, date_format)
		log.debug(str(date.day))
		try:
			power2.append(PowerConsumptionLogger.objects.filter(Q(dateTime__day=date.day)).latest('dateTime'))
		except:
			pass
	count_int = len(power2)
	database_list_int = power2

	response_data = {
		'database_list': database_list,
		'database_list_int': database_list_int,
		'count': count,
		'count_int': count_int,
	}
	# log.debug(response_data)
	url = 'monitor/search_db_power_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)







# @login_required
# def show_database(request):
# 	if not request.POST:
# 		return render_to_response('monitor/container.html', context_instance=RequestContext(request))

# 	response_data = {}
# 	id = request.POST.get('id', 'None')
# 	start_date = timezone.now() - datetime.timedelta(days=7)
# 	end_date = timezone.now()

# 	# 온도 센서
# 	if id == 'TempHEIn1':
# 		database = TempHEIn1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHEIn2':
# 		database = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHEOut1'\
# 	or id == 'TempHPIn1' or id == 'TempHPIn2' or id == 'TempHPIn3'\
# 	or id == 'TempHPIn4' or id == 'TempHPIn5' or id == 'TempHPIn6':
# 		database = TempHEOut1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHEOut2':
# 		database = TempHEOut2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHPOut1':
# 		database = TempHPOut1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHPOut2':
# 		database = TempHPOut2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHPOut3':
# 		database = TempHPOut3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHPOut4':
# 		database = TempHPOut4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHPOut5':
# 		database = TempHPOut5Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'TempHPOut6':
# 		database = TempHPOut6Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	# 순환 펌프
# 	elif id == 'CirculatingPump':
# 		database = CirculatingPumpLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	# 순환 유량계
# 	elif id == 'CPFlowmeter':
# 		database = CPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	# 심정 유량계
# 	elif id == 'DWPFlowmeter':
# 		database = DWPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	# 심정 펌프
# 	elif id == 'DeepwellPump1':
# 		database = DeepwellPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'DeepwellPump2':
# 		database = DeepwellPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'DeepwellPump3':
# 		database = DeepwellPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	elif id == 'DeepwellPump4':
# 		database = DeepwellPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	# rt
# 	elif id == 'RefrigerationTon':
# 		database = RefrigerationTonLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	# 전력량
# 	elif id == 'PowerConsumption':
# 		database = PowerConsumptionLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	else:
# 		database = 'None'
# 	response_data.update({'id': id})
# 	response_data.update({'database': database})
# 	# csrf token
# 	response_data.update(csrf(request))
# 	html = render_to_string('monitor/sensor_data.html', response_data, RequestContext(request))
# 	# log.debug(html)
# 	return HttpResponse(html)
