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
from .excels import make_excel_file, make_rows
import controller
from django.views.decorators.csrf import csrf_exempt
import os.path


import logging
log = logging.getLogger(__name__)

# 명령을 준 후에 잠시 page reload를 하지 않음
flag_command = 0
file_path = os.path.join(myproject.settings.BASE_DIR, 'share/')

date_format = "%Y-%m-%d"					# db search
datetime_format = "%Y-%m-%d %H:%M"			# check if error exist

@csrf_exempt
@login_required
def index(request):
	request.session.set_expiry(0)
	request.session['name'] = 'admin'
	# log.debug(str(request.session['name']))

	# log.debug("K-ATES program started.")

	# sub program start
	# AirconMonitor, DataSender
	# sub_path = myproject.settings.BASE_DIR
	# os.system("C:\Users\Admin\Documents\Django\myprojezct\AirconMonitor/AirconMonitor.exe")
	# log.debug("AirconMonitoring program started")
	# os.system("C:\Users\Admin\Documents\Django\myproject\LobbyDisplayer/DataSender.exe")
	# log.debug("DataSender program started")

	response_data = check_if_error_exist()

	# 실내기
	ciu_nav = request.POST.get('ciu_nav','total')
	response_data.update({'ciu_nav':ciu_nav})
	if ciu_nav[0] == "f":
		response_data.update(controller.get_CIU_from_json(ciu_nav[1]))
	elif ciu_nav[0] == "h":
		response_data.update(controller.get_CIU_on_HP_from_json(ciu_nav[1]))
	else: # total
		response_data.update(controller.get_CIU_total())
	# 읽기 실패할 경우 읽을때까지 반복
	while response_data["ciu_error"] != None:
		if ciu_nav[0] == "f":
			response_data.update(controller.get_CIU_from_json(ciu_nav[1]))
		elif ciu_nav[0] == "h":
			response_data.update(controller.get_CIU_on_HP_from_json(ciu_nav[1]))
		else: # total
			response_data.update(controller.get_CIU_total())
	rt = response_data["rt_total"]

	# 냉난방모드 확인
	temp_mode = response_data["temp_mode"]
	old_temp_mode = TemperatureModeLogger.objects.latest('id').tempMode
	if temp_mode != old_temp_mode:
		tm = TemperatureModeLogger(
			dateTime=timezone.now(), tempMode=temp_mode
			).save()

	# 처음 프로그램 실행시 모드는 수동
	response_data.update({"op_mode": "AT"})
	if OperationModeLogger.objects.latest('id').opMode != "AT":
		oml = OperationModeLogger(
			dateTime=timezone.now(), opMode="AT"
		).save()
	# init cmd
	controller.init_cmd()

	# 센서값 읽어오기
	response_data.update(controller.read_data_from_json(rt))
	while response_data["hmidata_error"] != None:
		response_data.update(controller.read_data_from_json(rt))

	response_data.update(csrf(request))
	url = 'monitor/index.html'
	return render(request, url, response_data)

# @login_required
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
		# log.debug("database updated")
		# save_time = timezone.now()


@csrf_exempt
@login_required
def reload_display(request):
	###########################################
	# 3초마다 갱신해서 왼쪽 상태창, 오른쪽 실내기 정보 갱신
	# 자동제어시, 자동제어 로직에 따라 hmi에 명령을 줌
	# 수동인 경우 데이터 값만 갱신함.
	###########################################

	# check if error exist
	response_data = check_if_error_exist()

	# 실내기 정보 읽어오기
	ciu_nav = request.POST.get('ciu_nav','f1')
	response_data.update({'ciu_nav':ciu_nav})
	if ciu_nav[0] == "f":
		response_data.update(controller.get_CIU_from_json(ciu_nav[1]))
	elif ciu_nav[0] == "h":
		response_data.update(controller.get_CIU_on_HP_from_json(ciu_nav[1]))
	else: # total
		response_data.update(controller.get_CIU_total())
	# 읽기 실패할 경우 읽을때까지 반복
	while response_data["ciu_error"] != None:
		if ciu_nav[0] == "f":
			response_data.update(controller.get_CIU_from_json(ciu_nav[1]))
		elif ciu_nav[0] == "h":
			response_data.update(controller.get_CIU_on_HP_from_json(ciu_nav[1]))
		else: # total
			response_data.update(controller.get_CIU_total())
	rt = response_data["rt_total"]

	# 냉난방모드 확인
	temp_mode = response_data["temp_mode"]
	old_temp_mode = TemperatureModeLogger.objects.latest('id').tempMode
	# log.debug("temp_mode: " +str(temp_mode))
	# log.debug("old_temp_mode: " +str(old_temp_mode))
	if temp_mode != old_temp_mode:
		tm = TemperatureModeLogger(
			dateTime=timezone.now(), tempMode=temp_mode
			).save()
		cmd = controller.read_cmd()
		now = str(timezone.now())[:-7]
		cmd.update({'datetime':now,'temp_mode':temp_mode})
		controller.write_cmd(cmd)


	global flag_command 
	if flag_command: # command를 준 후에 파일을 잠시 읽지 않는다.
		import time
		time.sleep(5)
		flag_command = 0

	# hmi에서 데이터 읽고 (자동)제어
	# 수동인 경우 데이터 값(디스플레이)만 갱신함.
	response_data.update(controller.read_data_from_json(rt))


	############### 통신 에러 처리 ############################
	try:
		timegap = response_data["datetime"] - timezone.now()
		# log.debug(str(timegap.total_seconds()))
		timegap_seconds = timegap.total_seconds()
	except:
		timegap_seconds = 15
	if timegap_seconds < 15: # 일반적으로 25~27초
		# log.debug("HMI not working or communication failed.")
		create_CHP_file()
	# 통신 에러 없는 경우	
	else: 
		# log.debug("HMI working")
		error_file_name = 'errorlog_chp.json'
		# 파일이 있다면
		if os.path.isfile(file_path + error_file_name):
			# log.debug("yes file")
			# 파일에 closed time 적어준다.
			with open(file_path + error_file_name) as data_file:
				_data = json.load(data_file)
			ct = dt.strftime(timezone.now(), datetime_format)
			_data.update({"CT": ct})
			with open(file_path + error_file_name, 'w') as fp:
				json.dump(_data, fp)
		# 없다면 그냥 pass
		# log.debug("no file")
	############### 통신 에러 처리 끝 #########################

	# log.debug(str(response_data["us"][5]["state"]))
	# log.debug(str(response_data["us"][6]["state"]))
	# log.debug(str(response_data["us"][8]["state"]))
	
	# 운전 모드 정보
	# op_mode = OperationModeLogger.objects.latest('id').opMode
	response_data.update({
		# "op_mode": op_mode,
		"temp_mode": temp_mode,
	})
	
	t = timezone.now()		
	# log.debug(str(response_data["error"]))

	# 읽기 실패할 경우 읽을때까지 반복
	while response_data["hmidata_error"] != None:
		response_data.update(controller.read_data_from_json(rt))

	# 데이터베이스 저장
	# 중복 저장 방지
	latest_data = DeepwellPump1Logger.objects.latest('id').dateTime
	if (timezone.now() - latest_data).seconds > 5:
		# 저장 주기마다 data save
		save_interval = SaveIntervalLogger.objects.latest('id').interval
		if save_interval == 10:
			if t.minute % 10 == 0 and t.second < 5: 
				save_data(response_data)
		elif save_interval == 30:
			if t.minute % 30 == 0 and t.second < 5:
				save_data(response_data)
		elif save_interval == 60:
			if t.minute == 0 and t.second < 5:
				save_data(response_data)
		else:
			if t.minute % 5 == 0 and t.second < 5:
				save_data(response_data)

	url = 'monitor/container.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

def create_CHP_file():
	error_file_name = 'errorlog_chp.json'
	# 이미 에러가 있다면 skip
	if os.path.isfile(file_path + error_file_name):
		return
	# 없다면 에러 파일 생성
	ot = dt.strftime(timezone.now(), datetime_format)
	error_text = {
		"CODE": "CHP",
		"OT": ot,
		"CT": ""
		}
	with open(file_path + error_file_name, 'w') as fp:
		json.dump(error_text, fp)
	return

@login_required
def specs(request):
	response_data = controller.get_device_specs()
	url = 'monitor/specs.html'
	return render(request, url, response_data)

@login_required
def setting_cp(request):
	# 순환펌프 설정을 눌렀을 때 뜨는 페이지
	response_data = {}
	response_data.update(controller.read_cp_operating())

	url = 'monitor/setting_cp.html'
	return render(request, url, response_data)

@login_required
def setting_cp_done(request):
	# 순환펌프 동작을 설정했을 때 적용
	response_data = {}

	cp_operating = int(request.POST.get('cpOperating',0))
	cp1switch = request.POST.get('cp1switch', 'error').encode('utf-8')
	cp1hz = int(request.POST.get('cp1hz', 0))
	cp1flux = int(request.POST.get('cp1flux', 0))
	cp2switch = request.POST.get('cp2switch', 'error').encode('utf-8')
	cp2hz = int(request.POST.get('cp2hz', 0))
	cp2flux = int(request.POST.get('cp2flux', 0))

	# op_mode = OperationModeLogger.objects.latest('id').opMode
	# temp_mode = TemperatureModeLogger.objects.latest('id').tempMode
	# 설정 값 db에 저장
	# controller.set_cp(1, op_mode, cp1switch, cp1hz, cp1flux)
	# controller.set_cp(2, op_mode, cp2switch, cp2hz, cp2flux)
	# cmdmain에 기록
	# ######## 	controller.write_cmd()
	# cp1 = CirculatingPump1Logger.objects.latest('id')
	# cp2 = CirculatingPump2Logger.objects.latest('id')
	# dwp1 = DeepwellPump1Logger.objects.latest('id')
	# dwp2 = DeepwellPump2Logger.objects.latest('id')
	# dwp3 = DeepwellPump3Logger.objects.latest('id')
	# dwp4 = DeepwellPump4Logger.objects.latest('id')
	# rt = RefrigerationTonLogger.objects.latest('id')
	cmd = controller.read_cmd()
	now = str(timezone.now())[:-7]
	if cp1switch == "OFF":
		cp1hz = 0
		cp1flux = 0
	if cp2switch == "OFF":
		cp2hz = 0
		cp2flux = 0
	cmd.update({
		'datetime':now,
		'cp_operating': cp_operating,
		'cp1': cp1switch,
		'cp1_hz': cp1hz,
		'cp1_flux': cp1flux,
		'cp2': cp2switch,
		'cp2_hz': cp2hz,
		'cp2_flux': cp2flux,
	})
	# log.debug("write_cmd from setting_cp_done")
	controller.write_cmd(cmd)

	# check if error exist
	response_data = check_if_error_exist()
	

	# 커맨드 후 hmidata를 잠시동안 읽지 않는다.
	global flag_command 
	flag_command = 1

	# 센서값 읽어오기
	# response_data.update(controller.read_data_from_json(rt))
	# if response_data == False:
	# 	response_data = {"error":"file read error"}
	# 	url = 'error/read.html'
	# 	html = render_to_string(url, response_data)
	# 	return HttpResponse(html)

	# html = render_to_string('monitor/container.html', response_data, RequestContext(request))
	return HttpResponse('')

@login_required
def set_db_save_interval(request):
	response_data = {}
	url = 'navbar/setting_db_save_interval.html'
	return render(request, url, response_data)

@login_required
def set_db_save_interval_confirm(request):
	new_save_interval = request.POST.get('savetime', '10')
	save_interval = SaveIntervalLogger.objects.latest('id').interval
	if save_interval != new_save_interval:
		sil = SaveIntervalLogger(
			dateTime=timezone.now(), interval=new_save_interval
		).save()
	# return reload_display(request)
	return HttpResponse('')



@login_required
def show_database(request):
	# 지금 안쓰임
	response_data = {}
	url = 'monitor/show_database.html'
	return render(request, url, response_data)

@login_required
def page_request(request):
	# 지금 안쓰임
	if not request.POST:
		return render_to_response('monitor/container.html',context_instance=RequestContext(request))

	# 기기 동작 내역
	selected = int(request.POST.get('page', 1))
	response_data = controller.get_operation_log(selected)

	html = render_to_string('monitor/right_bottom.html', response_data, RequestContext(request))
    	return HttpResponse(html)

@login_required
def toggle_switch(request):
	# 심정펌프 스위치 on/off 버튼 클릭시 제어
	if not request.POST:
		return render_to_response('monitor/container.html', context_instance=RequestContext(request))

	location = request.POST.get('id', 'error')
	loc = location.upper()
	switch = request.POST.get('switch', 'error').encode('utf-8').upper()
	if switch == 'error':
		# log.debug("toggle_switch, switch: error")
		pass

	# op_mode = OperationModeLogger.objects.latest('id').opMode
	# temp_mode = TemperatureModeLogger.objects.latest('id').tempMode

	cmd = controller.read_cmd()
	now = str(timezone.now())[:-7]
	cmd.update({'datetime':now})
	# 심정 펌프 갱신
	if loc == 'DWP1': 
		cmd.update({'dwp1':switch})
	elif loc == 'DWP2':
		cmd.update({'dwp2':switch})
	elif loc == 'DWP3':
		cmd.update({'dwp3':switch})
	elif loc == 'DWP4':
		cmd.update({'dwp4':switch})

	# 커맨드 파일 작성
	controller.write_cmd(cmd)
	# log.debug("write_cmd from toggle_switch")

	# 커맨드 후 hmidata를 잠시동안 읽지 않는다.
	global flag_command 
	flag_command = 1

	# html = render_to_string('monitor/right_top.html', response_data, RequestContext(request))
	# return HttpResponseBadRequest
	return HttpResponse('')


@login_required
def change_ciu(request):
	if not request.POST:
		return render_to_response('monitor/container.html', context_instance=RequestContext(request))

	response_data = {}
	# 실내기 정보 읽어오기
	ciu_nav = request.POST.get('ciu_nav','f1')
	response_data.update({'ciu_nav':ciu_nav})
	if ciu_nav[0] == "f":
		response_data.update(controller.get_CIU_from_json(ciu_nav[1]))
	elif ciu_nav[0] == "h":
		response_data.update(controller.get_CIU_on_HP_from_json(ciu_nav[1]))
	else: # total
		response_data.update(controller.get_CIU_total())
	
	html = render_to_string('monitor/right.html', response_data, RequestContext(request))
	return HttpResponse(html)


@login_required
def setting_mode(request, mode):
	# log.debug(str(mode))
	response_data = {"mode": mode}
	url = 'navbar/setting_mode.html'
	html = render_to_response(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def setting_mode_confirm(request):
	new_op_mode = request.POST.get('mode', 'error')
	if new_op_mode == 'error':
		log.debug("setting_mode_confirm, op_mode: error")
		pass

	# log.debug("setting_mode_confirm: " + new_op_mode)
	op_mode = OperationModeLogger.objects.latest('id').opMode
	temp_mode = TemperatureModeLogger.objects.latest('id').tempMode
	# op_mode가 변경된 경우 저장
	if op_mode != new_op_mode:
		oml = OperationModeLogger(
				dateTime=timezone.now(), opMode=new_op_mode
			).save()
	cmd = controller.read_cmd()
	now = str(timezone.now())[:-7]
	cmd.update({
		"datetime":now,
		"op_mode":new_op_mode,
		"temp_mode": temp_mode,
		})
	controller.write_cmd(cmd)
	# log.debug("write_cmd from settimg_mode_confirm")
	# log.debug(cmd)
	response_data = {
		"op_mode": new_op_mode,
		"temp_mode": temp_mode,
	}

	# return reload_display(request)	
	return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required	
def operation_control(request):
	# check if error exist
	response_data = check_if_error_exist()
	

	# RT 값을 받기 위해 get_ciu_from_json 필요
	response_data.update(controller.get_CIU_from_json(1))
	rt = response_data["cooling_rt"]

	response_data.update(controller.read_data_from_json(rt))
	while response_data["error"] != None:
		response_data.update(controller.read_data_from_json(rt))

	# COP
	try:
		COP = rt/response_data["power"]["currentPowerConsumption"]
	except ZeroDivisionError:
		COP = 0
	response_data.update({"COP": COP})

	url = 'monitor/operation_control.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)


def check_if_error_exist(error_count = 0):
	error_alarm = []
	# file = file_path + 'errorlog' + str(error_count) + '.json'

	# CHP error 처리
	if os.path.isfile(file_path + 'errorlog_chp.json' ):
		# log.debug("errorlog_chp exist")
		with open(file_path + 'errorlog_chp.json') as data_file:
			_data = json.load(data_file)
		# 변수에 각 내용 저장
		code = _data["CODE"]
		ot = _data["OT"]
		ct = _data["CT"]

		# 경보 상황 해제
		# database 저장
		if ct != "":
			# log.debug("ct in")

			# occurTime, closedTime
			occur_time = dt.strptime(ot, datetime_format)
			closed_time = dt.strptime(ct, datetime_format)

			classification = "COMM"
			location = "HMI"
			state = "CE"		# 통신 에러
			try:
				alarm = AlarmLogger(
					classification = classification, location = location, state = state,
					occurTime = occur_time, closedTime = closed_time
					).save()
			except Exception, e:
				log.error(str(e))
			
			# errorlog 파일 삭제
			os.remove(file_path + 'errorlog_chp.json')
		# 경보 띄우기
		else:
			error_alarm.append({
				"location": "HMI",
				"status": "HMI 통신 에러(HMI 동작 이상)",
				"OT": ot,
				"CT": ct,
			})

	
	# errorlog 파일이 있는지 확인한다.
	from glob import glob
	for file in glob(file_path + 'errorlog[0-9]*'):
		# 파일이 있으면 에러를 처리한다.
		with open(file) as data_file:
			_data = json.load(data_file)
		# log.error(str(_data))

		# 변수에 각 내용 저장
		code = _data["CODE"]
		ot = _data["OT"]
		ct = _data["CT"]

		# 경보 상황 해제
		# database 저장
		if ct != "":
			# occurTime, closedTime
			occur_time = dt.strptime(ot, datetime_format)
			closed_time = dt.strptime(ct, datetime_format)

			# classification, location, state
			if code[0] == "T":		# 온도 안전범위 이탈
				classification = "TP"
				location = "T" + code[1]
				if code[2] == "H":
					state = "HT"	# 고온
				else:
					state = "LT"	# 저온
			elif code[0] == "F":	# 유량 안전범위 이탈
				classification = "FX"
				location = "F" + code[1]
				if code[2] == "H":
					state = "HF" 	# 유량 과다
				else: 
					state = "LF"	# 유량 부족
			elif code[0] == "L":	# 수위 부족
				classification = "WL"
				location = "DWP" + code[1]
			elif code[0] == "P":	# 전력 안전범위 초과
				classification = "PO"
				location = "PO"
			else: 					# 통신 에러
				classification = "COMM"
				if code == "DAQ":	# DAQ
					location = "DAQ"
				elif code == "CIV":	# 인버터
					location = "IV"
				else: # code == "CFM":	# 유량계
					location = "FM"

			try:
				alarm = AlarmLogger(
					classification = classification, location = location, state = state,
					occurTime = occur_time, closedTime = closed_time
					).save()
			except Exception, e:
				log.error(str(e))
			
			# errorlog 파일 삭제
			os.remove(file)

		# 경보 띄우기
		# 에러 분석
		if code[0] == "T":			# 온도 안전범위 초과
			# 에러 상태 파악
			if code[2] == "H":		# 고온
				error_alarm.append({
					"location": "온도"+code[1],
					"status": "고온",
					"OT": ot,
					"CT": ct,
				})
			else: # "L"				# 저온
				error_alarm.append({
					"location": "온도"+code[1],
					"status": "저온",
					"OT": ot,
					"CT": ct,
				})
		elif code[0] == "F":		# 유량 안전범위 초과
			# 에러 상태 파악
			if code[1] == "1":		# 순환수 유량계
				if code[2] == "H":	# 유량 과다
					error_alarm.append({
						"location": "순환수",
						"status": "유량 과다",
						"OT": ot,
						"CT": ct,
					})
				else: # "L"			# 유량 부족
					error_alarm.append({
						"location": "순환수",
						"status": "유량 부족",
						"OT": ot,
						"CT": ct,
					})
			if code[1] == "2":		# 순환수 유량계
				if code[2] == "H":	# 유량 과다
					error_alarm.append({
						"location": "지하수",
						"status": "유량 과다",
						"OT": ot,
						"CT": ct,
					})
				else: # "L"			# 유량 부족
					error_alarm.append({
						"location": "지하수",
						"status": "유량 부족",
						"OT": ot,
						"CT": ct,
					})
		elif code[0] == "L":		# 수위 부족
			error_alarm.append({
					"location": "심정펌프"+code[1],
					"status": "수위 부족",
					"OT": ot,
					"CT": ct,
				})
		elif code[0] == "P":		# 전력 안전범위 초과
			error_alarm.append({
					"location": "전력량",
					"status": "안전범위 초과",
					"OT": ot,
					"CT": ct,
				})
		elif code == "DAQ":			# DAQ 장치 에러
			error_alarm.append({
					"location": "HMI",
					"status": "DAQ에러",
					"OT": ot,
					"CT": ct,
				})
		elif code == "CIV":			# 인버터 통신 에러
			error_alarm.append({
					"location": "HMI",
					"status": "인버터 통신 에러",
					"OT": ot,
					"CT": ct,
				})
		else: # code == "CFM":			# 유량계 통신 에러
			error_alarm.append({
					"location": "HMI",
					"status": "유량계 통신 에러",
					"OT": ot,
					"CT": ct,
				})



		# log.debug(code + ot + ct)
		# 여러개의 경보가 동시에 발생하는 경우인지 확인하여 처리.
		# error_count += 1
		# error_alarm.append(check_if_error_exist(error_count))

	return {"error_msg": error_alarm}

def alarm_status(request):
	response_data = check_if_error_exist()
	url = 'monitor/alarm_status.html'
	html = render_to_response(url, response_data, RequestContext(request))
	return HttpResponse(html)


###################### DB 검색 ######################

def search_db_excel(request):
	obj_type = request.POST.get('objType','error')
	# get table header
	columns = request.POST.get('columns', 'error').encode('utf-8')
	num_col = int(request.POST.get('numCol', 'error'))
	col_mat = columns.replace('"', '').replace('[', '').replace(']', '').split(",")

	# table content
	# rows = request.POST.get('rows', 'error').encode('utf-8')
	# num_row = int(request.POST.get('numRow', 'error'))
	# row_split = rows.replace('"', '').replace('[', '').replace(']', '').split(",")
	# row_mat = [[None for x in range(num_col)] for x in range(num_row)]



	# search db accord. to obj_type & start~end date
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	# date exception
	if start_date=='error' or end_date=='error':
		if 'cur' in obj_type:
			url = 'monitor/search_db_'+obj_type+'_cur_result.html'
		elif 'int' in obj_type:
			url = 'monitor/search_db_'+obj_type+'_int_result.html'
		else:
			url = 'monitor/search_db_'+obj_type+'_result.html'
		search_db_error(url, request)

	floor = request.POST.get('floor', '0')
	name = request.POST.get('name', '0')
	data = controller.search_database(obj_type, start_date, end_date, count=0, floor=floor, name=name, excel=True)

	if 'database' in data.keys():
		# most of ciu cases
		row_mat = make_rows(obj_type, num_col, data["count"], data["database"])
	else:
		# all cases except ciu, and 'ciu all' cases
		row_mat = make_rows(obj_type, num_col, data["count"], data["database_list"])
	


		# if '.' in r:
		# 	# type = float
		# 	row_mat[i][j] = float(r)
		# elif r.isdigit():
		# 	row_mat[i][j] = int(r)
		# else:
		# 	row_mat[i][j] = r
		# j += 1
		# if j == num_col:
		# 	j = 0; i += 1;
		# 	if i == num_row: break;

	# create excel file
	make_excel_file(obj_type, col_mat, row_mat)

	response_data = {"obj_type":obj_type}
	return HttpResponse(json.dumps(response_data), content_type="application/json")


import mimetypes
@login_required
def download_result(request, o):
	obj_type = o
	# obj_type = request.GET['o']
	if obj_type:
		filename = os.path.join(myproject.settings.BASE_DIR, 'database/' + obj_type + '.xlsx')

		if os.path.exists(filename) and os.path.isfile(filename):
			with open(filename, 'rb') as fp:
				response = HttpResponse(fp.read())
			content_type, encoding = mimetypes.guess_type(filename)
			if content_type is None:
				content_type = 'application/octet-stream'
			response['Content-Type'] = content_type
			response['Content-Length'] = str(os.stat(filename).st_size)
		else:
			response = HttpResponse("올바른 접근이 아닙니다.", content_type="text/plain")
		if encoding is not None:
			response['Content-Encoding'] = encoding
		# if u'WebKit'in request.META.get('HTTP_USER_AGENT', u'Webkit'):
		# 	filename_header = 'filename="%s"' % filename.encode('utf-8')
		# elif u'MSIE' in request.META.get('HTTP_USER_AGENT', u'MSIE'):
		# 	filename_header = ''
		# else:
		# 	filename_header = "filename*=UTF-8''%s" % urllib.quote(filename.encode('utf-8'))
		filename_header = ''
		
		response['Content-Disposition'] = 'attachment; ' + filename_header

	else:	# obj_type ??
		# log.debug('obj_type:' + obj_type)
		response = HttpResponse("obj_type ??", content_type="text/plain")
	return response


def search_db_error(url, request):
	response_data = {'error': 'Error! 다시 검색해 주세요.'}
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

# @login_required
def search_db_ciu(request):
	response_data = {}
	url = 'monitor/search_db_ciu.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

# @login_required
def search_db_ciu_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_ciu_result.html'
		search_db_error(url, request)

	floor = request.POST.get('floor', '0')
	name = request.POST.get('name', '0')
	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('ciu', start_date, end_date, count=count, floor=floor, name=name)
	url = 'monitor/search_db_ciu_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_hp(request):
	response_data = {}
	url = 'monitor/search_db_hp.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_hp_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_hp_result.html'
		search_db_error(url, request)

# <<<<<<< HEAD
	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('hp', start_date, end_date, count)
# =======
# 	log.debug("start")
# 	hp1 = HeatPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
# 	hp2 = HeatPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
# 	hp3 = HeatPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
# 	hp4 = HeatPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
# 	hp5 = HeatPump5Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
# 	hp6 = HeatPump6Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime') 
# 	count += hp1.count()
# 	log.debug("search done")

# 	database_list = zip(list(hp1), list(hp2), list(hp3), list(hp4), list(hp5), list(hp6))
# 	log.debug("zip done")

# 	response_data = {
# 		'database_list':database_list,
# 		'count': count,
# 	}
	
# >>>>>>> hp45
	url = 'monitor/search_db_hp_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)
	# return HttpResponse(json.dumps(response_data), mimetype='application/json')

@login_required
def search_db_cp(request):
	response_data = {}
	url = 'monitor/search_db_cp.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_cp_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_cp_result.html'
		search_db_error(url, request)

# <<<<<<< HEAD
	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0
# =======
# 	log.debug(start_date)
# 	cp1 = CirculatingPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	cp2 = CirculatingPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
# 	count += cp1.count()

# 	database_list = zip(list(cp1), list(cp2))
# 	response_data = {
# 		'database_list':database_list,
# 		'count': count,
# 	}
# >>>>>>> hp45

	response_data = controller.search_database('cp', start_date, end_date, count)
	url = 'monitor/search_db_cp_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_dwp(request):
	response_data = {}
	url = 'monitor/search_db_dwp.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_dwp_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_dwp_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('dwp', start_date, end_date, count)
	url = 'monitor/search_db_dwp_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_fm(request):
	response_data = {}
	url = 'monitor/search_db_fm.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_fm_cur_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_fm_cur_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('fm-cur', start_date, end_date, count)
	url = 'monitor/search_db_fm_cur_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_fm_int_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_fm_int_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('fm-int', start_date, end_date, count)
	url = 'monitor/search_db_fm_int_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_power(request):
	response_data = {}
	url = 'monitor/search_db_power.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_power_cur_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_power_cur_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('power-cur', start_date, end_date, count)
	url = 'monitor/search_db_power_cur_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_power_int_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_power_int_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('power-int', start_date, end_date, count)
	url = 'monitor/search_db_power_int_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_cop(request):
	response_data = {}
	url = 'monitor/search_db_cop.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_cop_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_cop_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('cop', start_date, end_date, count)
	url = 'monitor/search_db_cop_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_tw(request):
	response_data = {}
	url = 'monitor/search_db_tw.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_tw_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')
	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_tw_result.html'
		search_db_error(url, request)

	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	response_data = controller.search_database('tw', start_date, end_date, count)
	url = 'monitor/search_db_tw_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_alarm(request):
	response_data = {}
	url = 'monitor/search_db_alarm.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)

@login_required
def search_db_alarm_result(request):
	start_date = request.POST.get('startDate', 'error')
	end_date = request.POST.get('endDate', 'error')

	if start_date=='error' or end_date=='error':
		url = 'monitor/search_db_alarm_result.html'
		search_db_error(url, request)

	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)
	count = request.POST.get('count', 0)
	try:
		count = int(count)
	except:
		count = 0

	al = AlarmLogger.objects.filter(Q(occurTime__gte=start_date), Q(closedTime__lte=end_date)).order_by('-occurTime')
	count += al.count()

	database_list = list(al)
	response_data = {
		'database_list':database_list,
		'count': count,
	}

	url = 'monitor/search_db_alarm_result.html'
	html = render_to_string(url, response_data, RequestContext(request))
	return HttpResponse(html)


