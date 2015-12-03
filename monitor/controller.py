#-*- coding: utf-8 -*-
from .models import *

from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
import simplejson as json
from datetime import datetime as dt
from django.db.models import Q

import logging
log = logging.getLogger(__name__)

import os, myproject.settings
file_path = os.path.join(myproject.settings.BASE_DIR, 'share/')

# rt = 0.0

# rt값 다운될 때 버퍼 (껏다켰다 반복되지 않게)
# a~e, rt 구분에 따른 5구간
prev_section = 'a' 	

# rt 다운될 때 구간별 버퍼
buf_a = 0; buf_b = 0; buf_c = 0; buf_d = 0;	

# rt값 다운될 때 완충값 (껏다켰다 반복되지 않게)
pump_buffer = 2 		

# 심정펌프가 꺼질 때 다른 펌프가 풀가동 될 때까지 기다렸다 꺼짐
pump_off_delay = 30 # seconds

datetime_format = "%Y-%m-%d %H:%M:%S"
date_format = "%Y-%m-%d"					# db search

def get_operation_log(page):
	# 사용하지 않음
	# 기기 동작 내역
	logs_per_page = 10
	page_no = 5

	switch_list = OperationSwitchControl.objects.order_by('-dateTime')
	paginator = Paginator(switch_list, logs_per_page)
	
	# 선택된 페이지가 범위를 초과된 경우 (prev, next 선택)
	selected = page
	if (selected <= 1):
		selected = 1
	elif (selected > paginator.num_pages):
		selected = paginator.num_pages

	try:
		switch_logs = paginator.page(selected)
	except EmptyPage:
		# if page is out of range, deliver last page of results.
		switch_logs = paginator.page(paginator.num_pages)

	if (selected-page_no < 0):
		page_range = range(1,10)
	elif (selected + page_no > paginator.num_pages):
		page_range = paginator.page_range[paginator.num_pages-10:]
	else :
		page_range = paginator.page_range[selected-page_no:selected+page_no-1]


	data = {
		"switch_logs": switch_logs,
		"page_range": page_range,
		"selected": selected,
	}
	return data

def get_sensors():
	# 사용하지 않음
	# db에 저장된 값을 읽어옴
	heat_pump_1 = HeatPump1Logger.objects.latest('id')
	heat_pump_2 = HeatPump2Logger.objects.latest('id')
	heat_pump_3 = HeatPump3Logger.objects.latest('id')
	heat_pump_4 = HeatPump4Logger.objects.latest('id')
	heat_pump_5 = HeatPump5Logger.objects.latest('id')
	heat_pump_6 = HeatPump6Logger.objects.latest('id')
	heat_pump = [
		heat_pump_1,
		heat_pump_2,
		heat_pump_3,
		heat_pump_4,
		heat_pump_5,
		heat_pump_6,
	]

	deepwell_pump_1 = DeepwellPump1Logger.objects.latest('dateTime')
	deepwell_pump_2 = DeepwellPump2Logger.objects.latest('dateTime')
	deepwell_pump_3 = DeepwellPump3Logger.objects.latest('dateTime')
	deepwell_pump_4 = DeepwellPump4Logger.objects.latest('dateTime')
	DWP = [
		deepwell_pump_1,
		deepwell_pump_2,
		deepwell_pump_3,
		deepwell_pump_4,
	]

	circulating_pump1 = CirculatingPump1Logger.objects.latest('dateTime')
	circulating_pump2 = CirculatingPump2Logger.objects.latest('dateTime')
	CP = [
		circulating_pump1,
		circulating_pump2
	]

	DWPFM = DWPFlowmeterLogger.objects.latest('dateTime')
	CPFM = CPFlowmeterLogger.objects.latest('dateTime')

	temp_HEIn1 = TempHEIn1Logger.objects.latest('id')
	temp_HEIn2 = TempHEIn2Logger.objects.latest('id')
	temp_HEOut1 = TempHEOut1Logger.objects.latest('id')
	temp_HEOut2 = TempHEOut2Logger.objects.latest('id')
	temp_HPIn1 = TempHPIn1Logger.objects.latest('id')
	temp_HPIn2 = TempHPIn2Logger.objects.latest('id')
	temp_HPIn3 = TempHPIn3Logger.objects.latest('id')
	temp_HPIn4 = TempHPIn4Logger.objects.latest('id')
	temp_HPIn5 = TempHPIn5Logger.objects.latest('id')
	temp_HPIn6 = TempHPIn6Logger.objects.latest('id')
	temp_HPOut1 = TempHPOut1Logger.objects.latest('id')
	temp_HPOut2 = TempHPOut2Logger.objects.latest('id')
	temp_HPOut3 = TempHPOut3Logger.objects.latest('id')
	temp_HPOut4 = TempHPOut4Logger.objects.latest('id')
	temp_HPOut5 = TempHPOut5Logger.objects.latest('id')
	temp_HPOut6 = TempHPOut6Logger.objects.latest('id')
	temp_HE = [
		temp_HEIn1,
		temp_HEOut1,
		temp_HEIn2,
		temp_HEOut2,
	]
	temp_HP = [
		temp_HPIn1,
		temp_HPIn2,
		temp_HPIn3,
		temp_HPIn4,
		temp_HPIn5,
		temp_HPIn6,
		temp_HPOut1,
		temp_HPOut2,
		temp_HPOut3,
		temp_HPOut4,
		temp_HPOut5,
		temp_HPOut6,
	]

	power = PowerConsumptionLogger.objects.latest('dateTime')
	rt = RefrigerationTonLogger.objects.latest('dateTime')
	switch_log = OperationSwitchControl.objects.latest('dateTime')

	data = {
		"heat_pump": heat_pump,
		"DWP": DWP,
		"CP": CP,
		"DWPFM": DWPFM,
		"CPFM": CPFM,
		"temp_HE": temp_HE,
		# "temp_HP": temp_HP,
		"temp_HEIn1": temp_HEIn1,
		"temp_HEOut1": temp_HEOut1,
		"temp_HEIn2": temp_HEIn2,
		"temp_HEOut2": temp_HEOut2,
		"temp_HPIn1": temp_HPIn1,
		"temp_HPIn2": temp_HPIn2,
		"temp_HPIn3": temp_HPIn3,
		"temp_HPIn4": temp_HPIn4,
		"temp_HPIn5": temp_HPIn5,
		"temp_HPIn6": temp_HPIn6,
		"temp_HPOut1": temp_HPOut1,
		"temp_HPOut2": temp_HPOut2,
		"temp_HPOut3": temp_HPOut3,
		"temp_HPOut4": temp_HPOut4,
		"temp_HPOut5": temp_HPOut5,
		"temp_HPOut6": temp_HPOut6,
		"power": power, 
		"switch_log": switch_log,
		"rt": rt,
	}
	return data


def get_device_specs():
	# 사용하지 않음
	######## Device Info ################
	flowmeter_info = FlowmeterInfo.objects.all()
	Inverter_info = InverterInfo.objects.all()
	watthourmeter_info = WattHourMeterInfo.objects.all()
	heatexchanger_info = HeatExchangerInfo.objects.all()
	heatpump_info = HeatPumpInfo.objects.all()
	circulatingpump_info = CirculatingPumpInfo.objects.all()
	deepwellpump_info = DeepwellPumpInfo.objects.all()
	data = {
		"flowmeter_info": flowmeter_info,
		"Inverter_info": Inverter_info,
		"watthourmeter_info": watthourmeter_info,
		"heatexchanger_info": heatexchanger_info,
		"heatpump_info": heatpump_info,
		"circulatingpump_info": circulatingpump_info,
		"deepwellpump_info": deepwellpump_info,
	}
	return data

def read_cp_operating():
	# 순환펌프 동작 상태를 읽는다.
	try:
		with open(file_path + 'hmidata.json') as data_file:
			_data = json.load(data_file)
	except Exception, e:
		log.error(str(e))
		with open(file_path + 'hmidata.json') as data_file:
			_data = json.load(data_file)

	temp_mode = TemperatureModeLogger.objects.latest('id').tempMode

	data = {
		"temp_mode": temp_mode,
		"cp_operating":_data["cp_operating"],
		"switch1": _data["cp1"],
		"hz1":_data["cp1_hz"],
		"flux1":_data["cp1_flux"],
		"switch2":_data["cp2"],
		"hz2":_data["cp2_hz"],
		"flux2":_data["cp2_flux"],
	}
	return data

def write_cmd():
	# hmi에 줄 명령을 파일에 적는다.
	####### create json file
	op_mode = OperationModeLogger.objects.latest('id').opMode
	temp_mode = TemperatureModeLogger.objects.latest('id').tempMode
	cp1 = CirculatingPump1Logger.objects.latest('id')
	cp2 = CirculatingPump2Logger.objects.latest('id')
	dwp1 = DeepwellPump1Logger.objects.latest('id')
	dwp2 = DeepwellPump2Logger.objects.latest('id')
	dwp3 = DeepwellPump3Logger.objects.latest('id')
	dwp4 = DeepwellPump4Logger.objects.latest('id')
	# rt = RefrigerationTonLogger.objects.latest('id')
	datetime = str(timezone.now())[:-7]
	if cp1.switch == "OFF":
		cp1.Hz = 0
		cp1.flux = 0
	if cp2.switch == "OFF":
		cp2.Hz = 0
		cp2.flux = 0
	cmd_text = {
		'op_mode': op_mode,
		'temp_mode': temp_mode,
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
		# 'rt': rt.RT,
	}
	cmd_text.update(read_cp_operating())
	# log.debug("command written")
	# log.debug(cmd_text)
	try:
		with open(file_path + 'cmdmain.json', 'w') as fp:
			json.dump(cmd_text, fp)
	except Exception, e:
		log.error(str(e))
	return 


def read_data_from_json(rt):
	# hmi에서 데이터를 읽어 온다.
	data = {}
	try:
		with open(file_path + 'hmidata.json') as data_file:
			_data = json.load(data_file)

	except Exception, e:
		# log.error(str(e))
		return { "hmidata_error": e }

	datetime = dt.strptime(_data["datetime"], datetime_format)
	op_mode = OperationModeLogger.objects.latest('id').opMode
	if op_mode != _data["op_mode"]:
		write_cmd()

	# temp_mode = TemperatureModeLogger.objects.latest('id').tempMode
	# 작동중인 순환펌프; id 1: 0, id 2: 1
	cp_operating = int(_data["cp_operating"]) - 1

	# 임시 COP
	# try:
	# 	COP = rt*3.49 / _data["pow_int"]
	# except ZeroDivisionError:
	# 	COP = 0

	# 관측센서 DB
	try:
		level1 = TWSB1Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
		level2 = TWAB1Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
		level3 = TWAB2Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
		level4 = TWSB2Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
	except:
		level1 = TWSB1Logger.objects.latest('id').level
		level2 = TWAB1Logger.objects.latest('id').level
		level3 = TWAB2Logger.objects.latest('id').level
		level4 = TWSB2Logger.objects.latest('id').level


	data = {
		# hmi와의 통신 에러를 확인하기 위해 필요함.
		"datetime": datetime,
		# 히트 펌프 6개 list
		"heat_pump": [
			{
				"switch":_data["hp1"],
				"tempIn":_data["heo1"],
				"tempOut":_data["hpo1"],
			},
			{
				"switch":_data["hp2"],
				"tempIn":_data["heo1"],
				"tempOut":_data["hpo2"],
			},
			{
				"switch":_data["hp3"],
				"tempIn":_data["heo1"],
				"tempOut":_data["hpo3"],
			},
			{
				"switch":_data["hp4"],
				"tempIn":_data["heo1"],
				"tempOut":_data["hpo4"],
			},
			{
				"switch":_data["hp5"],
				"tempIn":_data["heo1"],
				"tempOut":_data["hpo5"],
			},
			{
				"switch":_data["hp6"],
				"tempIn":_data["heo1"],
				"tempOut":_data["hpo6"],
			}
		],
		# 심정 펌프 4개 list
		"DWP": [
			{
				"switch":_data["dwp1"],
				"get_waterLevel_display":_data["dwp1_lv"],
				"level" : level1,

			},
			{
				"switch":_data["dwp2"],
				"get_waterLevel_display":_data["dwp2_lv"],
				"level" : level2,
			},
			{
				"switch":_data["dwp3"],
				"get_waterLevel_display":_data["dwp3_lv"],
				"level" : level3,
			},
			{
				"switch":_data["dwp4"],
				"get_waterLevel_display":_data["dwp4_lv"],
				"level" : level4,
			}
		],
		# 순환 펌프 2개 list
		"CP": [
			{
				"get_CPID_display": 1,
				"switch":_data["cp1"],
				"Hz":_data["cp1_hz"],
				"flux":_data["cp1_flux"],
			},
			{
				"get_CPID_display": 2,
				"switch":_data["cp2"],
				"Hz":_data["cp2_hz"],
				"flux":_data["cp2_flux"],
			}
		],
		# 실제 작동중인 순환 펌프 번호
		"cp_operating": cp_operating+1,
		# 지하수 쪽 유량계
		"DWPFM": {
			"temperature":_data["dwpfm_temp"],
			"currentFlux":_data["dwpfm_cur"],
			"integralFlux":_data["dwpfm_int"],
			"velocity":_data["dwpfm_vel"],
		},
		# 순환수 쪽 유량계
		"CPFM": {
			"temperature":_data["cpfm_temp"],
			"currentFlux":_data["cpfm_cur"],
			"integralFlux":_data["cpfm_int"],
			"velocity":_data["cpfm_vel"],
		},
		# 온도 센서 10개
		"temp_HEIn1": {
			"temperature":_data["hei1"],
		},
		"temp_HEOut1": {
			"temperature": _data["heo1"],
		},
		"temp_HEIn2": {
			"temperature":_data["hei2"],
		},
		"temp_HEOut2": {
			"temperature":_data["heo2"],
		},
		"temp_HPIn1": _data["heo1"],
		"temp_HPIn2": _data["heo1"],
		"temp_HPIn3": _data["heo1"],
		"temp_HPIn4": _data["heo1"],
		"temp_HPIn5": _data["heo1"],
		"temp_HPIn6": _data["heo1"],
		"temp_HPOut1": _data["hpo1"],
		"temp_HPOut2": _data["hpo2"],
		"temp_HPOut3": _data["hpo3"],
		"temp_HPOut4": _data["hpo4"],
		"temp_HPOut5": _data["hpo5"],
		"temp_HPOut6": _data["hpo6"],
		# 전력량계
		"power": {
			"currentPowerConsumption":_data["pow_cur"],
			"integralPowerConsumption":_data["pow_int"],
		}, 
		# "dateTime":_data["datetime"],
		# hmi에 보내준 rt값을 받음.
		"rt": {
			"RT":_data["rt"],
			# "RT":rt,
		},
		# COP
		"COP": _data["cop"],
		# "COP": COP,
		"op_mode": op_mode,
		"temp_mode": _data["temp_mode"],
		###### error 처리 #####
		# 정상적으로 받은 경우 error:none. 
		# 읽기를 실패한 경우 위의 try except에서 error msg를 return하고
		# hmidata_error가 none이 될 때가지 계속 다시 읽는다.
		# hmidata.json 읽기 실패의 경우는 
		# 1. key-value error
		# 2. hmi pc에서 파일을 쓰고있어 main pc에서 파일을 읽지 못한 경우 뿐이다.
		######################
		"hmidata_error": None,
	}
	# log.debug("controller, temp_mode:" + str(data["temp_mode"]))
	# log.debug(str(data))
	# buf_a, buf_b, buf_c, buf_d = set_section_buffer()
	# data["rt"]["RT"] = rt
	
	# rt값이 전과 다르다면 저장한다.
	# log.debug("rt: " + str(float(rt)) + ", data[rt]: " + str(float(data["rt"]["RT"])))
	if str(float(rt)) != str(float(data["rt"]["RT"])): # data["rt"]["RT"] == 0 or
		try:
			rtl = RefrigerationTonLogger(
				dateTime=datetime, RT=rt
				).save()
		except Exception, e:
			log.error(str(e))

	# hmi에 rt값 전달
	write_rt(rt)


	# 자동 모드인 경우 자동제어
	# log.debug(op_mode)
	if op_mode == 'AT':	
		# ##########################################
		# # ver_2015.09.22
		# # 현장 주차장에 주입정 물이 아스팔트 위로 넘쳤음
		# # 기존의 자동운전모드 로직은 지우지 말것.
		# # 이번에 적용하게 되는 자동 운전모드 로직 변경 내용
		# #
		# # ~45rt 
		# # 냉방: 심정1, 난방: 심정4, 순환: 50
		# # 45rt~
		# # 냉방: 심정 1+2, 난방: 심정 3+4, 순환 50
		# ##########################################

		# if rt == 0:
		# 	# 심정펌프 정지
		# 	if data["DWP"][0]["switch"] != "OFF":
		# 		try:
		# 			dwp = DeepwellPump1Logger(
		# 			    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 			    )
		# 			new_cmd = OperationSwitchControl(
		# 				dateTime=datetime, location="DWP1", switch="OFF"
		# 			)
		# 			dwp.save(); new_cmd.save();
		# 		except Exception, e:
		# 			log.error(str(e))
		# 		write_cmd()
		# 		log.debug("write_cmd from hmidata(dwp1, off)")
		# 		# 끌 때는 순차적으로 끈다.
		# 		return data
		# 	if data["DWP"][1]["switch"] != "OFF":
		# 		try:
		# 			dwp = DeepwellPump2Logger(
		# 			    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 			    )
		# 			new_cmd = OperationSwitchControl(
		# 				dateTime=datetime, location="DWP2", switch="OFF"
		# 			)
		# 			dwp.save(); new_cmd.save();
		# 		except Exception, e:
		# 			log.error(str(e))
		# 		write_cmd()
		# 		log.debug("write_cmd from hmidata(dwp2, off)")
		# 		# 끌 때는 순차적으로 끈다.
		# 		return data
		# 	if data["DWP"][2]["switch"] != "OFF":
		# 		try:
		# 			dwp = DeepwellPump3Logger(
		# 			    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 			    )
		# 			new_cmd = OperationSwitchControl(
		# 				dateTime=datetime, location="DWP3", switch="OFF"
		# 			)
		# 			dwp.save(); new_cmd.save();
		# 		except Exception, e:
		# 			log.error(str(e))
		# 		write_cmd()
		# 		log.debug("write_cmd from hmidata(dwp3, off)")
		# 		# 끌 때는 순차적으로 끈다.
		# 		return data
		# 	if data["DWP"][3]["switch"] != "OFF":
		# 		try:
		# 			dwp = DeepwellPump4Logger(
		# 			    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 			    )
		# 			new_cmd = OperationSwitchControl(
		# 				dateTime=datetime, location="DWP4", switch="OFF"
		# 			)
		# 			dwp.save(); new_cmd.save();
		# 		except Exception, e:
		# 			log.error(str(e))
		# 		write_cmd()
		# 		log.debug("write_cmd from hmidata(dwp4, off)")
		# 		# 끌 때는 순차적으로 끈다.
		# 		return data


		# 	# 순환펌프 정지
		# 	if data["CP"][cp_operating]["switch"] != "OFF":
		# 		try:
		# 			data["CP"][cp_operating]["switch"] = "OFF"
		# 			data["CP"][cp_operating]["Hz"] = 0
		# 			data["CP"][cp_operating]["flux"] = 0
		# 			if cp_operating == 0:
		# 				cp = CirculatingPump1Logger(
		# 					dateTime=datetime, 
		# 					CPID=cp_operating+1, 
		# 					opMode=op_mode, 
		# 					switch="OFF", 
		# 					Hz=0, 
		# 					flux=0
		# 					).save()
		# 			else:
		# 				cp = CirculatingPump2Logger(
		# 					dateTime=datetime, 
		# 					CPID=cp_operating+1, 
		# 					opMode=op_mode, 
		# 					switch="OFF", 
		# 					Hz=0, 
		# 					flux=0
		# 					).save()
		# 			new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="CP"+str(cp_operating+1), switch="OFF"
		# 				).save()
		# 		except Exception, e:
		# 			log.error(str(e))
		# 		write_cmd()
		# 		log.debug("write_cmd from hmidata(cp, off)")


		# elif rt < 45:
		# 	if temp_mode == "CL":
		# 		# 심정펌프 1
		# 		if data["DWP"][0]["switch"] != "ON":
		# 			try:
		# 				dwp = DeepwellPump1Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="ON"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP1", switch="ON"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp1, on)")

		# 		# 혹시 다른 심정펌프가 켜져있다면 끈다
		# 		if data["DWP"][1]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump2Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP2", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp2, off)")
		# 		if data["DWP"][2]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump3Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP3", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp3, off)")
		# 		if data["DWP"][3]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump4Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP4", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp4, off)")
		# 	else: # 난방
		# 		# 심정펌프 4
		# 		if data["DWP"][3]["switch"] != "ON":
		# 			try:
		# 				dwp = DeepwellPump4Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="ON"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP4", switch="ON"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp4, on)")

		# 		# 혹시 다른 심정펌프가 켜져있다면 끈다
		# 		if data["DWP"][0]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump1Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP1", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp1, off)")
		# 		if data["DWP"][1]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump2Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP2", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp2, off)")
		# 		if data["DWP"][2]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump3Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP3", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp3, off)")
				
		# 	# 순환펌프 50
		# 	if data["CP"][cp_operating]["Hz"] != 50:
		# 		try:
		# 			if cp_operating == 0:
		# 				cp = CirculatingPump1Logger(
		# 					dateTime=datetime, 
		# 					CPID=cp_operating+1, 
		# 					opMode=op_mode, 
		# 					switch="ON", 
		# 					Hz=50, 
		# 					flux=834
		# 					).save()
		# 			else:
		# 				cp = CirculatingPump2Logger(
		# 					dateTime=datetime, 
		# 					CPID=cp_operating+1, 
		# 					opMode=op_mode, 
		# 					switch="ON", 
		# 					Hz=50, 
		# 					flux=834
		# 					).save()
		# 			new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="CP"+str(cp_operating+1), switch="OFF"
		# 				).save()
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(cp, off)")
		# 		except Exception, e:
		# 			log.error(str(e))
		# else: # rt > 45
		# 	if temp_mode == "CL":
		# 		# 심정펌프 1+2
		# 		if data["DWP"][0]["switch"] != "ON":
		# 			try:
		# 				dwp = DeepwellPump1Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="ON"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP1", switch="ON"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp1, on)")
		# 		if data["DWP"][1]["switch"] != "ON":
		# 			try:
		# 				dwp = DeepwellPump2Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="ON"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP2", switch="ON"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp2, on)")


		# 		# 혹시 다른 심정펌프가 켜져 있다면 끈다
		# 		if data["DWP"][2]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump3Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP3", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp3, off)")
		# 		if data["DWP"][3]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump4Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP4", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp4, off)")


		# 	else: # 난방
		# 		# 심정펌프 3+4
		# 		if data["DWP"][2]["switch"] != "ON":
		# 			try:
		# 				dwp = DeepwellPump3Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="ON"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP3", switch="ON"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp, on)")
		# 		if data["DWP"][3]["switch"] != "ON":
		# 			try:
		# 				dwp = DeepwellPump4Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="ON"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP4", switch="ON"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp4, on)")

		# 		# 혹시 다른 심정펌프가 켜져있다면 끈다
		# 		if data["DWP"][0]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump1Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP1", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp1, off)")
		# 		if data["DWP"][1]["switch"] != "OFF":
		# 			try:
		# 				dwp = DeepwellPump2Logger(
		# 				    dateTime=datetime, opMode=op_mode, switch="OFF"
		# 				    )
		# 				new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="DWP2", switch="OFF"
		# 				)
		# 				dwp.save(); new_cmd.save();
		# 			except Exception, e:
		# 				log.error(str(e))
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(dwp2, off)")

		# 	# 순환펌프 50
		# 	if data["CP"][cp_operating]["Hz"] != 50:
		# 		try:
		# 			if cp_operating == 0:
		# 				cp = CirculatingPump1Logger(
		# 					dateTime=datetime, 
		# 					CPID=cp_operating+1, 
		# 					opMode=op_mode, 
		# 					switch="ON", 
		# 					Hz=50, 
		# 					flux=834
		# 					).save()
		# 			else:
		# 				cp = CirculatingPump2Logger(
		# 					dateTime=datetime, 
		# 					CPID=cp_operating+1, 
		# 					opMode=op_mode, 
		# 					switch="ON", 
		# 					Hz=50, 
		# 					flux=834
		# 					).save()
		# 			new_cmd = OperationSwitchControl(
		# 					dateTime=datetime, location="CP"+str(cp_operating+1), switch="OFF"
		# 				).save()
		# 			write_cmd()
		# 			log.debug("write_cmd from hmidata(cp, off)")
		# 		except Exception, e:
		# 			log.error(str(e))
		# #
		# #
		# #
		# #
		# ##################### end of ver_2015.09.22 #####################		


		#################### ver 1.1
		#################### 히트펌프에 따른 인버터(순환펌프) 출력 제어
		flux_need = 0
		if data["heat_pump"][0]["switch"] == "ON":
			flux_need = flux_need + 178
			data["CP"][cp_operating]["switch"] = "ON"
		if data["heat_pump"][1]["switch"] == "ON":
			flux_need = flux_need + 192
			data["CP"][cp_operating]["switch"] = "ON"
		if data["heat_pump"][2]["switch"] == "ON":
			flux_need = flux_need + 178
			data["CP"][cp_operating]["switch"] = "ON"
		if data["heat_pump"][3]["switch"] == "ON":
			flux_need = flux_need + 96
			data["CP"][cp_operating]["switch"] = "ON"
		if data["heat_pump"][4]["switch"] == "ON":
			flux_need = flux_need + 192
			data["CP"][cp_operating]["switch"] = "ON"
		if data["heat_pump"][5]["switch"] == "ON":
			flux_need = flux_need + 96
			data["CP"][cp_operating]["switch"] = "ON"

		# 필요 유량
		flux_need = int(flux_need + flux_need*0.1)
		# log.debug("flux_need_complement: " + str(flux_need));

		# 최소유량
		if flux_need != 0 and data["CP"][cp_operating]["flux"] <= 1000:
			# flux_need = int(30*16.67)
			# 임시.. 최대로(테스트용)
			flux_need = 1000
			hz_need = 60

		hz_need = int((flux_need/16.67))+1
		if hz_need == 1 and flux_need == 0:
			hz_need = 0
			flux_need = 0

		# log.debug("hz_need: " + str(hz_need));
		if data["CP"][cp_operating]["flux"] > 1000:
			hz_need = 60

		if hz_need > 60:
			# log.debug("if hz_need > 60: " + str(hz_need) + ", make it to 60.")
			hz_need = 60

		# log.debug("flux_need: " + str(int(flux_need)));
		# log.debug("hz_need finalllllllllllllll: " + str(hz_need));
		# log.debug("data[cp][Hz]: " + str(data["circulating_pump"]["Hz"]));
		# log.debug("rt: " + str(rt))


		# log.debug("flux_need: " + str(int(flux_need)) + ", hmi flux: " + str(data["CP"][cp_operating]["flux"]));
		# log.debug(int(data["CP"][cp_operating]["flux"]) != int(flux_need))
		if int(data["CP"][cp_operating]["flux"]) != int(flux_need):
			# log.debug(flux_need==0)
			if flux_need == 0:
				# 히트펌프 모두 꺼져있는 경우 순환펌프 OFF
				if data["CP"][cp_operating]["switch"] != "OFF":
					try:
						data["CP"][cp_operating]["switch"] = "OFF"
						data["CP"][cp_operating]["Hz"] = 0
						data["CP"][cp_operating]["flux"] = 0
						if cp_operating == 0:
							# 순환 펌프 1번
							cp = CirculatingPump1Logger(
								dateTime=datetime, 
								CPID=cp_operating+1, 
								opMode=data['op_mode'], 
								switch="OFF", 
								Hz=0, 
								flux=0
								).save()
						else:
							# 순환 펌프 2번
							cp = CirculatingPump2Logger(
								dateTime=datetime, 
								CPID=cp_operating+1, 
								opMode=data['op_mode'], 
								switch="OFF", 
								Hz=0, 
								flux=0
								).save()
						# new_cmd = OperationSwitchControl(
						# 		dateTime=datetime, location="CP"+str(cp_operating+1), switch="OFF"
						# 	).save()
						write_cmd()
						# log.debug("write_cmd from hmidata(cp, off)")
					except Exception, e:
						log.error(str(e))
			else: # flux_need > 0 히트펌프 켜져있는 경우 순환펌프 Hz 조절
				# log.debug(int(data["CP"][cp_operating]["Hz"]))
				# log.debug(int(hz_need))
				# log.debug(int(data["CP"][cp_operating]["Hz"]) != int(hz_need))
				if int(data["CP"][cp_operating]["Hz"]) != int(hz_need):
					try:
						data["CP"][cp_operating]["switch"] = "ON"
						
						data["CP"][cp_operating]["Hz"] = hz_need
						# log.debug("hz: " + str(hz_need))
						data["CP"][cp_operating]["flux"] = flux_need
						if cp_operating == 0:
							# 순환 펌프 1번
							cp = CirculatingPump1Logger(
								dateTime=datetime, 
								CPID=cp_operating+1, 
								opMode=data['op_mode'], 
								switch="ON", 
								Hz=hz_need, 
								flux=flux_need
								).save()
							# log.debug("cp1 save")
						else:
							# 순환 펌프 2번
							cp = CirculatingPump2Logger(
								dateTime=datetime, 
								CPID=cp_operating+1, 
								opMode=data['op_mode'], 
								switch="ON", 
								Hz=hz_need, 
								flux=flux_need
								).save()
							# log.debug("cp2 save")

						# new_cmd = OperationSwitchControl(
						# 		dateTime=datetime, location="CP"+str(cp_operating+1), switch="OFF"
						# 	).save()
						write_cmd()
						# log.debug("write_cmd from hmidata(cp, on)")
					except Exception, e:
						log.error(str(e))
						# log.debug(str(e))



		############## 임시: 히트펌프 켜져 있으면 순환펌프 무조건 풀가동 #############
		# if data["CP"][cp_operating]["switch"] == "ON" and data["CP"][cp_operating]["Hz"] != 60:
		# 	try:
		# 		cp = CirculatingPumpLogger(
		# 			dateTime=datetime, 
		# 			CPID=data["CP"][cp_operating]["get_CPID_display"], 
		# 			opMode=data['op_mode'], 
		# 			switch=data["CP"][cp_operating]["switch"], 
		# 			Hz=60, 
		# 			flux=1000
		# 			).save()
		# 		new_cmd = OperationSwitchControl(
		# 				dateTime=datetime, location="CP"+str(data["CP"][cp_operating]["get_CPID_display"]), switch="ON"
		# 			).save()
		# 	except Exception, e:
		# 		log.error(str(e))
		# 	log.debug("write_cmd from hmidata")
		# 	write_cmd()

		##################### end of 히트펌프에 따른 인버터(순환펌프) 출력 제어 #############


		##################### rt값에 따른 심정펌프 출력 제어 #############
		# global rt
		# if rt == None:
		# 	log.debug("rt if: " + str(rt))
		# 	rt = 0.0
		# if data["rt"]["RT"] == None:
		# 	data["rt"]["RT"] = 0.0



		##################### rt에 따른 심정펌프 #############
		apply_rt_to_dwp(data, rt)

		###############################################
		# DWP 제어: 스위치 바뀌어야 하는 것만 바꾸고 db 저장
		# on으로 바뀌어야 하는 경우
		# 	dwp.json 에 dwp#: 0 으로 초기화
		# 	스위치 변경 및 db 저장 
		# off로 바뀌어야 하는 경우
		# 	dwp.json 에 dwp#: time 으로 저장
		# 	dwp.json 값이 이미 0이 아닌 시간이면 그냥 pass
		# 	후에 now-time > 5min 일 때 스위치 변경
		###############################################

		# try:
		# 	with open(file_path + 'dwp.json', 'r') as fp:
		# 		dwp = json.load(fp)
		# except Exception, e:
		# 	log.error(str(e))
		timenow = str(datetime)[:-7] #milisecond 제외

		if _data["dwp1"] != data["DWP"][0]["switch"]:
			if data["DWP"][0]["switch"] == "ON": # OFF >> ON
				# command가 on인 경우 off 예정이었더라도 시간 삭제
				# dwp.update({'dwp1': 0})
				try:
					dwp1 = DeepwellPump1Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][0]["switch"]
					    )
					# new_cmd1 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP1", switch=data["DWP"][0]["switch"]
					# )
					dwp1.save(); 
					# new_cmd1.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp1, on)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			else: # ON >> OFF
				try:
					dwp1 = DeepwellPump1Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][0]["switch"]
					    )
					# new_cmd1 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP1", switch=data["DWP"][0]["switch"]
					# )
					dwp1.save(); 
					# new_cmd1.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp1, off)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
				# dwp.json 파일에 on으로 명시되어있었던 경우만 시간 적음
				# if dwp["dwp1"] == 0:
				# 	dwp.update({'dwp1':timenow})
				# 	# data["DWP"][0]["switch"] = "ON"
				# else: 
				# 	check_off_delay1(dwp, data)

		if _data["dwp2"] != data["DWP"][1]["switch"]:
			if data["DWP"][1]["switch"] == "ON": # OFF >> ON
				# command가 on인 경우 off 예정이었더라도 시간 삭제
				# dwp.update({'dwp2': 0})
				try:
					dwp2 = DeepwellPump2Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][1]["switch"]
					    )
					# new_cmd2 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP2", switch=data["DWP"][1]["switch"]
					# )
					dwp2.save(); 
					# new_cmd2.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp2, on)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			else: # ON >> OFF
				try:
					dwp2 = DeepwellPump2Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][1]["switch"]
					    )
					# new_cmd2 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP2", switch=data["DWP"][1]["switch"]
					# )
					dwp2.save();
					 # new_cmd2.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp2, off)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			# dwp.json 파일에 on으로 명시되어있었던 경우만 시간 적음
				# if dwp["dwp2"] == 0:
				# 	dwp.update({'dwp2':timenow})
				# 	# data["DWP"][1]["switch"] = "ON"
				# else: 
				# 	check_off_delay2(dwp, data)

		if _data["dwp3"] != data["DWP"][2]["switch"]:
			if data["DWP"][2]["switch"] == "ON": # OFF >> ON
				# command가 on인 경우 off 예정이었더라도 시간 삭제
				# dwp.update({'dwp3': 0})
				try:
					dwp3 = DeepwellPump3Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][2]["switch"]
					    )
					# new_cmd3 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP3", switch=data["DWP"][2]["switch"]
					# )
					dwp3.save(); 
					# new_cmd3.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp3, on)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			else: # ON >> OFF
				try:
					dwp3 = DeepwellPump3Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][2]["switch"]
					    )
					# new_cmd3 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP3", switch=data["DWP"][2]["switch"]
					# )
					dwp3.save(); 
					# new_cmd3.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp3, off)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			# dwp.json 파일에 on으로 명시되어있었던 경우만 시간 적음
				# if dwp["dwp3"] == 0:
				# 	dwp.update({'dwp3':timenow})
				# 	# data["DWP"][2]["switch"] = "ON"
				# else: 
				# 	check_off_delay3(dwp, data)

		if _data["dwp4"] != data["DWP"][3]["switch"]:
			if data["DWP"][3]["switch"] == "ON": # OFF >> ON
				# command가 on인 경우 off 예정이었더라도 시간 삭제
				# dwp.update({'dwp4': 0})
				try:
					dwp4 = DeepwellPump4Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][3]["switch"]
					    )
					# new_cmd4 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP4", switch=data["DWP"][3]["switch"]
					# )
					dwp4.save(); 
					# new_cmd4.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp4, on)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			else: # ON >> OFF
				try:
					dwp4 = DeepwellPump4Logger(
					    dateTime=datetime, opMode=data['op_mode'], switch=data["DWP"][3]["switch"]
					    )
					# new_cmd4 = OperationSwitchControl(
					# 	dateTime=datetime, location="DWP4", switch=data["DWP"][3]["switch"]
					# )
					dwp4.save(); 
					# new_cmd4.save();
				except Exception, e:
					log.error(str(e))
				write_cmd()
				# log.debug("write_cmd from hmidata(dwp4, off)")
				return data # 심정펌프 제어시 delay를 위해 (mc noise)
			# dwp.json 파일에 on으로 명시되어있었던 경우만 시간 적음
				# if dwp["dwp4"] == 0:
				# 	dwp.update({'dwp4':timenow})
				# 	# data["DWP"][3]["switch"] = "ON"
				# else: 
				# 	check_off_delay4(dwp, data)

		# try:
		# 	with open(file_path + 'dwp.json', 'w') as fp:
		# 		 json.dump(dwp, fp)
		# except Exception, e:
		# 	log.error(str(e))

		# end: rt 에 따른 dwp 제어

		# cmd가 바뀔 때마다 (새로운 DB를 저장할 때) cmdmain.json command 전달
		

	return data



def set_section_buffer():
	# rt값 다운될 때 버퍼 적용 구간 설정
	global prev_section
	global buf_a, buf_b, buf_c, buf_d

	# set buffer 
	if prev_section == 'a':
		buf_a = buf_b = buf_c = buf_d = 0
	elif prev_section == 'b':
		buf_a = pump_buffer
		buf_b = buf_c = buf_d = 0
	elif prev_section == 'c':
		buf_b = pump_buffer
		buf_a = buf_c = buf_d = 0
	elif prev_section == 'd':
		buf_c = pump_buffer
		buf_a = buf_b = buf_d = 0
	elif prev_section == 'e':
		buf_d = pump_buffer
		buf_a = buf_b = buf_c = 0

	return buf_a, buf_b, buf_c, buf_d

def apply_rt_to_dwp(data, rt):
	global buf_a, buf_b, buf_c, buf_d
	# RT값에 따라 심정펌프 제어
	# log.debug(str(data["rt"]["RT"]))
	if data["temp_mode"] == 'CL': # 냉방 모드
		if rt == 0:
			data["DWP"][0]["switch"] = "OFF"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "OFF"
		elif rt < 20 - buf_a:
			data["DWP"][0]["switch"] = "OFF"
			data["DWP"][1]["switch"] = "ON"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "OFF"
			prev_section = 'a'
		elif rt < 30 - buf_b:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "OFF"
			prev_section = 'b'
		elif rt < 50 - buf_c:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "ON"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "OFF"
			prev_section = 'c'
		elif rt < 70 - buf_d:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "ON"
			prev_section = 'd'
		else:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "ON"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "ON"
			prev_section = 'e'
	else:	# 난방 모드
		if rt == 0:
			data["DWP"][0]["switch"] = "OFF"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "OFF"
		elif rt < 20 - buf_a:
			data["DWP"][0]["switch"] = "OFF"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "ON"
			data["DWP"][3]["switch"] = "OFF"
			prev_section = 'a'
		elif rt < 30 - buf_b:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "OFF"
			prev_section = 'b'
		elif rt < 50 - buf_c:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "ON"
			data["DWP"][3]["switch"] = "OFF"
			prev_section = 'c'
		elif rt < 70 - buf_d:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "OFF"
			data["DWP"][3]["switch"] = "ON"
			prev_section = 'd'
		else:
			data["DWP"][0]["switch"] = "ON"
			data["DWP"][1]["switch"] = "OFF"
			data["DWP"][2]["switch"] = "ON"
			data["DWP"][3]["switch"] = "ON"
			prev_section = 'e'


# 심정펌프 전원 off시 delay
def check_off_delay1(dwp, data):
	# 사용하지 않음
	off1 = str(dwp["dwp1"])
	if off1 != "0":
		offtime = dt.strptime(off1, "%Y-%m-%d %H:%M:%S")
		if (datetime - offtime) > timezone.timedelta(seconds=pump_off_delay):
			try:
				dwp1 = DeepwellPump1Logger(
				    dateTime=timezone.now(), opMode=data["op_mode"], switch="OFF"
				    )
				# new_cmd = OperationSwitchControl(
				# 	dateTime=timezone.now(), location="DWP1", switch="OFF"
				# )
				dwp1.save(); 
				# new_cmd.save();
			except Exception, e:
				log.error(str(e))
			write_cmd()
			# dwp["dwp1"] = 0
		else :	# 5분이 아직 안지났으면 상태는 on
			data["DWP"][0]["switch"] = "ON"

def check_off_delay2(dwp, data):
	# 사용하지 않음
	off2 = str(dwp["dwp2"])
	# log.debug("off2: " + off2)
	if off2 != "0":
		offtime = dt.strptime(off2, "%Y-%m-%d %H:%M:%S")
		if(timezone.now() - offtime > timezone.timedelta(seconds=(pump_off_delay))):
			try:
				dwp2 = DeepwellPump2Logger(
				    dateTime=timezone.now(), opMode=data["op_mode"], switch="OFF"
				    )
				# new_cmd = OperationSwitchControl(
				# 	dateTime=timezone.now(), location="DWP2", switch="OFF"
				# )
				dwp2.save();
				 # new_cmd.save();
			except Exception, e:
				log.error(str(e))
			write_cmd()
			# dwp["dwp2"] = 0
		else :	# 5분이 아직 안지났으면 상태는 on
			data["DWP"][1]["switch"] = "ON"

def check_off_delay3(dwp, data):
	# 사용하지 않음
	off3 = str(dwp["dwp3"])
	if off3 != "0":
		offtime = dt.strptime(off3, "%Y-%m-%d %H:%M:%S")
		if(timezone.now() - offtime > timezone.timedelta(seconds=(pump_off_delay))):
			try:
				dwp3 = DeepwellPump3Logger(
				    dateTime=timezone.now(), opMode=data["op_mode"], switch="OFF"
				    )
				# new_cmd = OperationSwitchControl(
				# 	dateTime=timezone.now(), location="DWP3", switch="OFF"
				# )
				dwp3.save(); 
				# new_cmd.save();
			except Exception, e:
				log.error(str(e))
			write_cmd()
			# dwp["dwp3"] = 0
		else :	# 5분이 아직 안지났으면 상태는 on
			data["DWP"][2]["switch"] = "ON"

def check_off_delay4(dwp, data):
	# 사용하지 않음
	off4 = str(dwp["dwp4"])
	if off4 != "0":
		offtime = dt.strptime(off4, "%Y-%m-%d %H:%M:%S")
		if(timezone.now() - offtime > timezone.timedelta(seconds=(pump_off_delay))):
			try:
				dwp4 = DeepwellPump4Logger(
				    dateTime=timezone.now(), opMode=data["op_mode"], switch="OFF"
				    )
				# new_cmd = OperationSwitchControl(
				# 	dateTime=timezone.now(), location="DWP4", switch="OFF"
				# )
				dwp4.save(); 
				# new_cmd.save();
			except Exception, e:
				log.error(str(e))
			write_cmd()
			# dwp["dwp4"] = 0
		else :	# 5분이 아직 안지났으면 상태는 on
			data["DWP"][3]["switch"] = "ON"



def save_data(data):
	# hmidata (+자동 제어 보정) 내용대로 DB에 저장
	op_mode = data["op_mode"]

	###### save models
	try:
		# HE temperature
		hei1 = TempHEIn1Logger(dateTime=timezone.now(),temperature=data["temp_HEIn1"]["temperature"])
		heo1 = TempHEOut1Logger(dateTime=timezone.now(),temperature=data["temp_HEOut1"]["temperature"])
		hei2 = TempHEIn2Logger(dateTime=timezone.now(),temperature=data["temp_HEIn2"]["temperature"])
		heo2 = TempHEOut2Logger(dateTime=timezone.now(),temperature=data["temp_HEOut2"]["temperature"])
		hei1.save(); hei2.save(); heo1.save(); heo2.save();

		# HP in temperature
		hpi1 = TempHPIn1Logger(dateTime=timezone.now(),temperature=data["temp_HPIn1"])
		hpi2 = TempHPIn2Logger(dateTime=timezone.now(),temperature=data["temp_HPIn2"])
		hpi3 = TempHPIn3Logger(dateTime=timezone.now(),temperature=data["temp_HPIn3"])
		hpi4 = TempHPIn4Logger(dateTime=timezone.now(),temperature=data["temp_HPIn4"])
		hpi5 = TempHPIn5Logger(dateTime=timezone.now(),temperature=data["temp_HPIn5"])
		hpi6 = TempHPIn6Logger(dateTime=timezone.now(),temperature=data["temp_HPIn6"])
		hpi1.save();hpi2.save();hpi3.save();hpi4.save();hpi5.save();hpi6.save();

		# HP out temperature
		hpo1 = TempHPOut1Logger(dateTime=timezone.now(),temperature=data["temp_HPOut1"])
		hpo2 = TempHPOut2Logger(dateTime=timezone.now(),temperature=data["temp_HPOut2"])
		hpo3 = TempHPOut3Logger(dateTime=timezone.now(),temperature=data["temp_HPOut3"])
		hpo4 = TempHPOut4Logger(dateTime=timezone.now(),temperature=data["temp_HPOut4"])
		hpo5 = TempHPOut5Logger(dateTime=timezone.now(),temperature=data["temp_HPOut5"])
		hpo6 = TempHPOut6Logger(dateTime=timezone.now(),temperature=data["temp_HPOut6"])
		hpo1.save();hpo2.save();hpo3.save();hpo4.save();hpo5.save();hpo6.save();

		# Heat pump
		# 히트 펌프
		hp1 = HeatPump1Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], switch=data["heat_pump"][0]["switch"], 
		    tempIn=hpi1, tempOut=hpo1
		    )
		hp2 = HeatPump2Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], switch=data["heat_pump"][1]["switch"], 
		    tempIn=hpi2, tempOut=hpo2
		    )
		hp3 = HeatPump3Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], switch=data["heat_pump"][2]["switch"], 
			tempIn=hpi3, tempOut=hpo3
			)
		hp4 = HeatPump4Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], switch=data["heat_pump"][3]["switch"], 
		    tempIn=hpi4, tempOut=hpo4
		    )
		hp5 = HeatPump5Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], switch=data["heat_pump"][4]["switch"], 
		    tempIn=hpi5, tempOut=hpo5
		    )
		hp6 = HeatPump6Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], switch=data["heat_pump"][5]["switch"], 
		    tempIn=hpi6, tempOut=hpo6
		    )
		hp1.save();hp2.save();hp3.save();hp4.save();hp5.save();hp6.save()

		# Deep well pump
		# 심정 펌프
		dwp1 = DeepwellPump1Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], 
		    switch=data["DWP"][0]["switch"],
		    waterLevel=data["DWP"][0]["get_waterLevel_display"]
		    )
		dwp2 = DeepwellPump2Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], 
		    switch=data["DWP"][1]["switch"],
		    waterLevel=data["DWP"][1]["get_waterLevel_display"]
		    )
		dwp3 = DeepwellPump3Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], 
		    switch=data["DWP"][2]["switch"],
		    waterLevel=data["DWP"][2]["get_waterLevel_display"]
		    )
		dwp4 = DeepwellPump4Logger(
		    dateTime=timezone.now(), opMode=data['op_mode'], 
		    switch=data["DWP"][3]["switch"],
		    waterLevel=data["DWP"][3]["get_waterLevel_display"]
		    )
		dwp1.save();dwp2.save();dwp3.save();dwp4.save();

		# 순환 펌프
		cp1 = CirculatingPump1Logger(
			dateTime=timezone.now(), 
			CPID=data["CP"][0]["get_CPID_display"], 
			opMode=data['op_mode'], 
			switch=data["CP"][0]["switch"], 
			Hz=data["CP"][0]["Hz"], 
			flux=data["CP"][0]["flux"]
			)
		cp2 = CirculatingPump2Logger(
			dateTime=timezone.now(), 
			CPID=data["CP"][1]["get_CPID_display"], 
			opMode=data['op_mode'], 
			switch=data["CP"][1]["switch"], 
			Hz=data["CP"][1]["Hz"], 
			flux=data["CP"][1]["flux"]
			)
		cp1.save(); cp2.save();

		# 지하수 유량계
		dwpfm = DWPFlowmeterLogger(
			dateTime=timezone.now(), 
			temperature=data["DWPFM"]["temperature"], 
			currentFlux=data["DWPFM"]["currentFlux"], 
			integralFlux=data["DWPFM"]["integralFlux"],
			velocity=data["DWPFM"]["velocity"]
			).save()
		# 순환수 유량계
		cpfm = CPFlowmeterLogger(
	    		dateTime=timezone.now(), 
			temperature=data["CPFM"]["temperature"], 
			currentFlux=data["CPFM"]["currentFlux"], 
			integralFlux=data["CPFM"]["integralFlux"],
			velocity=data["CPFM"]["velocity"]
			).save()
		# 전력량계
		power = PowerConsumptionLogger(
			dateTime=timezone.now(), 
			currentPowerConsumption=data["power"]["currentPowerConsumption"], 
			integralPowerConsumption=data["power"]["integralPowerConsumption"]
			).save()
		# COP
		cop = CoefficientOfPerformanceLogger(
			dateTime=timezone.now(), COP=data["COP"]
			).save()

		# tw = TubewellLogger(
		# 	dateTime=timezone.now(),
		# 	T1level = , T1temp = ,
		# 	T2level = , T2temp = ,
		# 	T3level = , T3temp = ,
		# 	T4level = , T4temp = ,
		# 	)
		# tw.save()

		# RT
		rtl = RefrigerationTonLogger(
			dateTime=timezone.now(), RT=data["rt"]["RT"]
			).save()
	except Exception, e:
		log.error(str(e))
	
	return True


def set_cp(id, opMode, switch, hz, flux):
	# 인버터 설정
	try:
		if id == 1:
			cp = CirculatingPump1Logger(
				dateTime=timezone.now(), CPID=id, opMode=opMode, switch=switch, Hz=hz, flux=flux
				).save()
		else: # id == 2
			cp = CirculatingPump2Logger(
				dateTime=timezone.now(), CPID=id, opMode=opMode, switch=switch, Hz=hz, flux=flux
				).save()
		# new_cmd = OperationSwitchControl(
		# 		dateTime=timezone.now(), location="CP"+str(id), switch=switch
		# 	).save()
	except Exception, e:
		log.error(str(e))
	return


def get_CIU_from_json(floor):
	# 층별 실내기 정보
	# ciu_dict = {}
	ciu_list = []
	count = 0
	file1 = file_path +'ciu1.json'
	file2 = file_path +'ciu2.json'
	file3 = file_path +'ciu3.json'
	# log.debug("floor: " + str(floor) + ", type: " + str(type(floor)))

	# 실내기 정보 파일에서 읽어옴
	# 1층
	if floor == "1":
		try: 
			with open(file1, 'r') as data_file:
				ciu_dict = json.load(data_file)
			# 순서 재정의
			# 방재실 ~ 저소득상담실
			ciu_list = ciu_dict["us"][:5]
			# 민원실 1,2,3
			for i in range(6, 9):
				ciu_list.append(ciu_dict["us"][i])
			# 민원실4
			ciu_list.append(ciu_dict["us"][5])
			# MDF ~ 사무대기실
			for i in range(9,14):
				ciu_list.append(ciu_dict["us"][i])
			ciu_dict.update({"us": ciu_list})
		except Exception, e:
			ciu_dict = {"ciu_error" : e}
			return ciu_dict
	
	# 2층
	elif floor == "2":
		try:
			with open(file2, 'r') as data_file:
				ciu_dict = json.load(data_file)
			# 순서 재정의
			# 조정실 ~ 면장실
			ciu_list = ciu_dict["us"][:4]
			# 교육실 1,2,3
			for i in range(6, 3, -1):
				ciu_list.append(ciu_dict["us"][i])
			# 서고 ~ 면대2
			for i in range(7,12):
				ciu_list.append(ciu_dict["us"][i])
			ciu_dict.update({"us": ciu_list})
		except Exception, e:
			ciu_dict = {"ciu_error" : e}
			return ciu_dict
	
	# 3층
	else: # floor == "3":
		try:
			with open(file3, 'r') as data_file:
				ciu_dict = json.load(data_file)
			# 순서 재정의
			# 강당1 ~ 다목적홀1
			ciu_list = ciu_dict["us"][:4]
			# 다목적홀2
			ciu_list.append(ciu_dict["us"][6])
			# 다목적홀3
			ciu_list.append(ciu_dict["us"][4])
			# 홀공간1
			ciu_list.append(ciu_dict["us"][5])
			# 홀공간2 ~ ㅍㅇ생학습실 2-2
			for i in range(7,12):
				ciu_list.append(ciu_dict["us"][i])
			ciu_dict.update({"us": ciu_list})
		except Exception, e:
			ciu_dict = {"ciu_error" : e}
			return ciu_dict




	ciu_dict.update({"ciu_error": None})
	return ciu_dict


def get_CIU_on_HP_from_json(no):
	# 히트 펌프별 실내기 정보
	ciu_dict = {}
	ciu_on_hp = []
	file1 = file_path +'ciu1.json'
	file2 = file_path +'ciu2.json'
	file3 = file_path +'ciu3.json'
	
	try:
		# ciu1.json
		if no == "5":
			with open(file1, 'r') as data_file:
				data = json.load(data_file)
			# 민원대기실1~3
			for i in range(6, 9):
				ciu_on_hp.append(data["us"][i])
			# 민원대기실4
			ciu_on_hp.append(data["us"][5])
			# MDF ~ 사무대기실
			for i in range(9, 14):
				ciu_on_hp.append(data["us"][i])
		# ciu2.json
		elif no == "2":
			with open(file2, 'r') as data_file:
				data = json.load(data_file)
			ciu_on_hp = data["us"][7:12]
		elif no == "3":
			with open(file2, 'r') as data_file:
				data = json.load(data_file)
			ciu_on_hp = data["us"][:2]
			for i in data["us"][3:7]:
				ciu_on_hp.append(i)

		# ciu3.json
		elif no == "1":
			with open(file3, 'r') as data_file:
				data = json.load(data_file)
			ciu_on_hp = data["us"][8:12]
		elif no == "6":
			with open(file3, 'r') as data_file:
				data = json.load(data_file)
			ciu_on_hp = data["us"][:2]
			for i in data["us"][3:8]:
				ciu_on_hp.append(i)
			
		# ciu1+2+3
		else: # no == 4
			with open(file1, 'r') as data_file:
				data = json.load(data_file)
			# 방재실 ~ 저소득상담실
			ciu_on_hp = data["us"][:5]
			# # 수유실
			# ciu_on_hp.append(data["us"][3])
			# # 저소득 상담실
			# ciu_on_hp.append(data["us"][4])
			with open(file2, 'r') as data_file:
				data = json.load(data_file)
			# 2층 홀
			ciu_on_hp.append(data["us"][2])
			with open(file3, 'r') as data_file:
				data = json.load(data_file)
			# 3층 홀
			ciu_on_hp.append(data["us"][2])
	except Exception, e:
		ciu_dict = {"ciu_error" : e}
		return ciu_dict

	ciu_dict.update({
		"us": ciu_on_hp,
		"temp_mode": data["temp_mode"],
		"on_total": data["on_total"],
		"rt_total": data["rt_total"],
		})
	ciu_dict.update({"ciu_error": None})

	return ciu_dict

def get_CIU_total():
	# 실내기 전체 정보
	# total information
	file1 = file_path +'ciu1.json'
	file2 = file_path +'ciu2.json'
	file3 = file_path +'ciu3.json'

	try:
		with open(file1, 'r') as data_file:
			ciu_dict1 = json.load(data_file)
		with open(file2, 'r') as data_file:
			ciu_dict2 = json.load(data_file)
		with open(file3, 'r') as data_file:
			ciu_dict3 = json.load(data_file)
	except Exception, e:
		ciu_dict = {"ciu_error" : e}
		return ciu_dict

	ciu_dict = {
		"temp_mode": ciu_dict1["temp_mode"],
		# total
		"on_total": ciu_dict1["on_total"],
		"off_total": 38-int(ciu_dict1["on_total"]),
		"rt_total": ciu_dict1["rt_total"],
		# f1
		"on_f1": ciu_dict1["on_f1"],
		"off_f1": 14-int(ciu_dict1["on_f1"]),
		"rt_f1": ciu_dict1["rt_f1"],
		# f2
		"on_f2": ciu_dict2["on_f2"],
		"off_f2": 12-int(ciu_dict2["on_f2"]),
		"rt_f2": ciu_dict2["rt_f2"],
		# f3
		"on_f3": ciu_dict3["on_f3"],
		"off_f3": 12-int(ciu_dict3["on_f3"]),
		"rt_f3": ciu_dict3["rt_f3"],
		"ciu_error": None,
	}
	return ciu_dict

def write_rt(rt):
	# rt 파일 작성
	# rt값과 관측센서 값을 보내준다.
	n = timezone.now()
	datetime = str(n)[:-7]
	# 관측센서 DB
	try:
		level1 = TWSB1Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
		level2 = TWAB1Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
		level3 = TWAB2Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
		level4 = TWSB2Logger.objects.filter(Q(dateTime__gte=n))[:1].get().level
	except:
		level1 = TWSB1Logger.objects.latest('id').level
		level2 = TWAB1Logger.objects.latest('id').level
		level3 = TWAB2Logger.objects.latest('id').level
		level4 = TWSB2Logger.objects.latest('id').level
	content = {
		"datetime" : datetime,
		"rt" : rt,
		"level1" : level1,
		"level2" : level2,
		"level3" : level3,
		"level4" : level4,
	}
	filename = file_path + 'rt.json'
	try:
		with open(filename, 'w') as fp:
			json.dump(content, fp)
	except Exception, e:
		# log.debug(str(e))
		pass
	return

def get_CIU_on_HP(no):
	# 사용하지 않음
	if no == "1":
		ret = CiuOnHeatPump1.objects.latest('id')
	elif no == "2":
		ret = CiuOnHeatPump2.objects.latest('id')
	elif no == "3":
		ret = CiuOnHeatPump3.objects.latest('id')
	elif no == "4":
		ret = CiuOnHeatPump4.objects.latest('id')
	elif no == "5":
		ret = CiuOnHeatPump5.objects.latest('id')
	else: # no == 6
		ret = CiuOnHeatPump6.objects.latest('id')

	# log.debug(str(ret.to_dict()))
	# ciu_dict = ret.to_dict()
	return {"ciu_on_hp": ret.items()}


def get_CIU(floor):
	# 사용하지 않음
	# 실내기 정보 db에서 읽어옴
	if floor == 1:
		us = Floor1CIUs.objects.latest('id')

		data = {
			"us": [
				{ 
					"switch":us.u1.switch,
					"temperature":us.u1.temperature,
					"set_temp":us.u1.setTemp,
					"op_mode":us.u1.get_opMode_display,
					"air_flow":us.u1.get_airFlow_display,
					"state":us.u1.get_state_display,
				},
				{ 
					"switch":us.u2.switch,
					"temperature":us.u2.temperature,
					"set_temp":us.u2.setTemp,
					"op_mode":us.u2.get_opMode_display,
					"air_flow":us.u2.get_airFlow_display,
					"state":us.u2.get_state_display,
				},
				{ 
					"switch":us.u3.switch,
					"temperature":us.u3.temperature,
					"set_temp":us.u3.setTemp,
					"op_mode":us.u3.get_opMode_display,
					"air_flow":us.u3.get_airFlow_display,
					"state":us.u3.get_state_display,
				},
				{ 
					"switch":us.u4.switch,
					"temperature":us.u4.temperature,
					"set_temp":us.u4.setTemp,
					"op_mode":us.u4.get_opMode_display,
					"air_flow":us.u4.get_airFlow_display,
					"state":us.u4.get_state_display,
				},
				{ 
					"switch":us.u5.switch,
					"temperature":us.u5.temperature,
					"set_temp":us.u5.setTemp,
					"op_mode":us.u5.get_opMode_display,
					"air_flow":us.u5.get_airFlow_display,
					"state":us.u5.get_state_display,
				},
				{ 
					"switch":us.u6.switch,
					"temperature":us.u6.temperature,
					"set_temp":us.u6.setTemp,
					"op_mode":us.u6.get_opMode_display,
					"air_flow":us.u6.get_airFlow_display,
					"state":us.u6.get_state_display,
				},
				{ 
					"switch":us.u7.switch,
					"temperature":us.u7.temperature,
					"set_temp":us.u7.setTemp,
					"op_mode":us.u7.get_opMode_display,
					"air_flow":us.u7.get_airFlow_display,
					"state":us.u7.get_state_display,
				},
				{ 
					"switch":us.u8.switch,
					"temperature":us.u8.temperature,
					"set_temp":us.u8.setTemp,
					"op_mode":us.u8.get_opMode_display,
					"air_flow":us.u8.get_airFlow_display,
					"state":us.u8.get_state_display,
				},
				{ 
					"switch":us.u9.switch,
					"temperature":us.u9.temperature,
					"set_temp":us.u9.setTemp,
					"op_mode":us.u9.get_opMode_display,
					"air_flow":us.u9.get_airFlow_display,
					"state":us.u9.get_state_display,
				},
				{ 
					"switch":us.u10.switch,
					"temperature":us.u10.temperature,
					"set_temp":us.u10.setTemp,
					"op_mode":us.u10.get_opMode_display,
					"air_flow":us.u10.get_airFlow_display,
					"state":us.u10.get_state_display,
				},
				{ 
					"switch":us.u11.switch,
					"temperature":us.u11.temperature,
					"set_temp":us.u11.setTemp,
					"op_mode":us.u11.get_opMode_display,
					"air_flow":us.u11.get_airFlow_display,
					"state":us.u11.get_state_display,
				},
				{ 
					"switch":us.u12.switch,
					"temperature":us.u12.temperature,
					"set_temp":us.u12.setTemp,
					"op_mode":us.u12.get_opMode_display,
					"air_flow":us.u12.get_airFlow_display,
					"state":us.u12.get_state_display,
				},
				{ 
					"switch":us.u13.switch,
					"temperature":us.u13.temperature,
					"set_temp":us.u13.setTemp,
					"op_mode":us.u13.get_opMode_display,
					"air_flow":us.u13.get_airFlow_display,
					"state":us.u13.get_state_display,
				},
				{ 
					"switch":us.u14.switch,
					"temperature":us.u14.temperature,
					"set_temp":us.u14.setTemp,
					"op_mode":us.u14.get_opMode_display,
					"air_flow":us.u14.get_airFlow_display,
					"state":us.u14.get_state_display,
				}
			]
		}
		return data

	elif floor == 2:
		us= Floor2CIUs.objects.latest('id')
	else: 
		us = Floor3CIUs.objects.latest('id')
	
	data = {
		"us": [
			{ 
				"switch":us.u1.switch,
				"temperature":us.u1.temperature,
				"set_temp":us.u1.setTemp,
				"op_mode":us.u1.get_opMode_display,
				"air_flow":us.u1.get_airFlow_display,
				"state":us.u1.get_state_display,
			},
			{ 
				"switch":us.u2.switch,
				"temperature":us.u2.temperature,
				"set_temp":us.u2.setTemp,
				"op_mode":us.u2.get_opMode_display,
				"air_flow":us.u2.get_airFlow_display,
				"state":us.u2.get_state_display,
			},
			{ 
				"switch":us.u3.switch,
				"temperature":us.u3.temperature,
				"set_temp":us.u3.setTemp,
				"op_mode":us.u3.get_opMode_display,
				"air_flow":us.u3.get_airFlow_display,
				"state":us.u3.get_state_display,
			},
			{ 
				"switch":us.u4.switch,
				"temperature":us.u4.temperature,
				"set_temp":us.u4.setTemp,
				"op_mode":us.u4.get_opMode_display,
				"air_flow":us.u4.get_airFlow_display,
				"state":us.u4.get_state_display,
			},
			{ 
				"switch":us.u5.switch,
				"temperature":us.u5.temperature,
				"set_temp":us.u5.setTemp,
				"op_mode":us.u5.get_opMode_display,
				"air_flow":us.u5.get_airFlow_display,
				"state":us.u5.get_state_display,
			},
			{ 
				"switch":us.u6.switch,
				"temperature":us.u6.temperature,
				"set_temp":us.u6.setTemp,
				"op_mode":us.u6.get_opMode_display,
				"air_flow":us.u6.get_airFlow_display,
				"state":us.u6.get_state_display,
			},
			{ 
				"switch":us.u7.switch,
				"temperature":us.u7.temperature,
				"set_temp":us.u7.setTemp,
				"op_mode":us.u7.get_opMode_display,
				"air_flow":us.u7.get_airFlow_display,
				"state":us.u7.get_state_display,
			},
			{ 
				"switch":us.u8.switch,
				"temperature":us.u8.temperature,
				"set_temp":us.u8.setTemp,
				"op_mode":us.u8.get_opMode_display,
				"air_flow":us.u8.get_airFlow_display,
				"state":us.u8.get_state_display,
			},
			{ 
				"switch":us.u9.switch,
				"temperature":us.u9.temperature,
				"set_temp":us.u9.setTemp,
				"op_mode":us.u9.get_opMode_display,
				"air_flow":us.u9.get_airFlow_display,
				"state":us.u9.get_state_display,
			},
			{ 
				"switch":us.u10.switch,
				"temperature":us.u10.temperature,
				"set_temp":us.u10.setTemp,
				"op_mode":us.u10.get_opMode_display,
				"air_flow":us.u10.get_airFlow_display,
				"state":us.u10.get_state_display,
			},
			{ 
				"switch":us.u11.switch,
				"temperature":us.u11.temperature,
				"set_temp":us.u11.setTemp,
				"op_mode":us.u11.get_opMode_display,
				"air_flow":us.u11.get_airFlow_display,
				"state":us.u11.get_state_display,
			},
			{ 
				"switch":us.u12.switch,
				"temperature":us.u12.temperature,
				"set_temp":us.u12.setTemp,
				"op_mode":us.u12.get_opMode_display,
				"air_flow":us.u12.get_airFlow_display,
				"state":us.u12.get_state_display,
			}
		]
	}
	return data

def save_ciu1(data):
	# 1층 실내기 상태 저장
	f1 = [None]*14
	try:
		f1[0] = Floor1CIU1(
			dateTime=timezone.now(), switch=data["us"][0]["switch"],temperature=data["us"][0]["temperature"], setTemp=data["us"][0]["set_temp"],
			opMode=data["us"][0]["op_mode"],airFlow=data["us"][0]["air_flow"],state=data["us"][0]["state"],
			)
		f1[1] = Floor1CIU2(
			dateTime=timezone.now(), switch=data["us"][1]["switch"],temperature=data["us"][1]["temperature"], setTemp=data["us"][1]["set_temp"],
			opMode=data["us"][1]["op_mode"],airFlow=data["us"][1]["air_flow"],state=data["us"][1]["state"],
			)
		f1[2] = Floor1CIU3(
			dateTime=timezone.now(), switch=data["us"][2]["switch"],temperature=data["us"][2]["temperature"], setTemp=data["us"][2]["set_temp"],
			opMode=data["us"][2]["op_mode"],airFlow=data["us"][2]["air_flow"],state=data["us"][2]["state"],
			)
		f1[3] = Floor1CIU4(
			dateTime=timezone.now(), switch=data["us"][3]["switch"],temperature=data["us"][3]["temperature"], setTemp=data["us"][3]["set_temp"],
			opMode=data["us"][3]["op_mode"],airFlow=data["us"][3]["air_flow"],state=data["us"][3]["state"],
			)
		f1[4] = Floor1CIU5(
			dateTime=timezone.now(), switch=data["us"][4]["switch"],temperature=data["us"][4]["temperature"], setTemp=data["us"][4]["set_temp"],
			opMode=data["us"][4]["op_mode"],airFlow=data["us"][4]["air_flow"],state=data["us"][4]["state"],
			)
		f1[5] = Floor1CIU6(
			dateTime=timezone.now(), switch=data["us"][5]["switch"],temperature=data["us"][5]["temperature"], setTemp=data["us"][5]["set_temp"],
			opMode=data["us"][5]["op_mode"],airFlow=data["us"][5]["air_flow"],state=data["us"][5]["state"],
			)
		f1[6] = Floor1CIU7(
			dateTime=timezone.now(), switch=data["us"][6]["switch"],temperature=data["us"][6]["temperature"], setTemp=data["us"][6]["set_temp"],
			opMode=data["us"][6]["op_mode"],airFlow=data["us"][6]["air_flow"],state=data["us"][6]["state"],
			)
		f1[7] = Floor1CIU8(
			dateTime=timezone.now(), switch=data["us"][7]["switch"],temperature=data["us"][7]["temperature"], setTemp=data["us"][7]["set_temp"],
			opMode=data["us"][7]["op_mode"],airFlow=data["us"][7]["air_flow"],state=data["us"][7]["state"],
			)
		f1[8] = Floor1CIU9(
			dateTime=timezone.now(), switch=data["us"][8]["switch"],temperature=data["us"][8]["temperature"], setTemp=data["us"][8]["set_temp"],
			opMode=data["us"][8]["op_mode"],airFlow=data["us"][8]["air_flow"],state=data["us"][8]["state"],
			)
		f1[9] = Floor1CIU10(
			dateTime=timezone.now(), switch=data["us"][9]["switch"],temperature=data["us"][9]["temperature"], setTemp=data["us"][9]["set_temp"],
			opMode=data["us"][9]["op_mode"],airFlow=data["us"][9]["air_flow"],state=data["us"][9]["state"],
			)
		f1[10] = Floor1CIU11(
			dateTime=timezone.now(), switch=data["us"][10]["switch"],temperature=data["us"][10]["temperature"], setTemp=data["us"][10]["set_temp"],
			opMode=data["us"][10]["op_mode"],airFlow=data["us"][10]["air_flow"],state=data["us"][10]["state"],
			)
		f1[11] = Floor1CIU12(
			dateTime=timezone.now(), switch=data["us"][11]["switch"],temperature=data["us"][11]["temperature"], setTemp=data["us"][11]["set_temp"],
			opMode=data["us"][11]["op_mode"],airFlow=data["us"][11]["air_flow"],state=data["us"][11]["state"],
			)
		f1[12] = Floor1CIU13(
			dateTime=timezone.now(), switch=data["us"][12]["switch"],temperature=data["us"][12]["temperature"], setTemp=data["us"][12]["set_temp"],
			opMode=data["us"][12]["op_mode"],airFlow=data["us"][12]["air_flow"],state=data["us"][12]["state"],
			)
		f1[13] = Floor1CIU14(
			dateTime=timezone.now(), switch=data["us"][13]["switch"],temperature=data["us"][13]["temperature"], setTemp=data["us"][13]["set_temp"],
			opMode=data["us"][13]["op_mode"],airFlow=data["us"][13]["air_flow"],state=data["us"][13]["state"],
			)
		for f in f1:
			f.save()
	except Exception, e:
		log.error(str(e))
	try:
		f1s = Floor1CIUs (
				u1=f1[0],
				u2=f1[1],
				u3=f1[2],
				u4=f1[3],
				u5=f1[4],
				u6=f1[5],
				u7=f1[6],
				u8=f1[7],
				u9=f1[8],
				u10=f1[9],
				u11=f1[10],
				u12=f1[11],
				u13=f1[12],
				u14=f1[13]
			).save()
	except Exception, e:
		log.error(str(e))
	return True

def save_ciu2(data):
	# 2층 실내기 상태 저장
	f2 = [None]*12
	try:
		f2[0] = Floor2CIU1(
			dateTime=timezone.now(), switch=data["us"][0]["switch"],temperature=data["us"][0]["temperature"], setTemp=data["us"][0]["set_temp"],
			opMode=data["us"][0]["op_mode"],airFlow=data["us"][0]["air_flow"],state=data["us"][0]["state"],
			)
		f2[1] = Floor2CIU2(
			dateTime=timezone.now(), switch=data["us"][1]["switch"],temperature=data["us"][1]["temperature"], setTemp=data["us"][1]["set_temp"],
			opMode=data["us"][1]["op_mode"],airFlow=data["us"][1]["air_flow"],state=data["us"][1]["state"],
			)
		f2[2] = Floor2CIU3(
			dateTime=timezone.now(), switch=data["us"][2]["switch"],temperature=data["us"][2]["temperature"], setTemp=data["us"][2]["set_temp"],
			opMode=data["us"][2]["op_mode"],airFlow=data["us"][2]["air_flow"],state=data["us"][2]["state"],
			)
		f2[3] = Floor2CIU4(
			dateTime=timezone.now(), switch=data["us"][3]["switch"],temperature=data["us"][3]["temperature"], setTemp=data["us"][3]["set_temp"],
			opMode=data["us"][3]["op_mode"],airFlow=data["us"][3]["air_flow"],state=data["us"][3]["state"],
			)
		f2[4] = Floor2CIU5(
			dateTime=timezone.now(), switch=data["us"][4]["switch"],temperature=data["us"][4]["temperature"], setTemp=data["us"][4]["set_temp"],
			opMode=data["us"][4]["op_mode"],airFlow=data["us"][4]["air_flow"],state=data["us"][4]["state"],
			)
		f2[5] = Floor2CIU6(
			dateTime=timezone.now(), switch=data["us"][5]["switch"],temperature=data["us"][5]["temperature"], setTemp=data["us"][5]["set_temp"],
			opMode=data["us"][5]["op_mode"],airFlow=data["us"][5]["air_flow"],state=data["us"][5]["state"],
			)
		f2[6] = Floor2CIU7(
			dateTime=timezone.now(), switch=data["us"][6]["switch"],temperature=data["us"][6]["temperature"], setTemp=data["us"][6]["set_temp"],
			opMode=data["us"][6]["op_mode"],airFlow=data["us"][6]["air_flow"],state=data["us"][6]["state"],
			)
		f2[7] = Floor2CIU8(
			dateTime=timezone.now(), switch=data["us"][7]["switch"],temperature=data["us"][7]["temperature"], setTemp=data["us"][7]["set_temp"],
			opMode=data["us"][7]["op_mode"],airFlow=data["us"][7]["air_flow"],state=data["us"][7]["state"],
			)
		f2[8] = Floor2CIU9(
			dateTime=timezone.now(), switch=data["us"][8]["switch"],temperature=data["us"][8]["temperature"], setTemp=data["us"][8]["set_temp"],
			opMode=data["us"][8]["op_mode"],airFlow=data["us"][8]["air_flow"],state=data["us"][8]["state"],
			)
		f2[9] = Floor2CIU10(
			dateTime=timezone.now(), switch=data["us"][9]["switch"],temperature=data["us"][9]["temperature"], setTemp=data["us"][9]["set_temp"],
			opMode=data["us"][9]["op_mode"],airFlow=data["us"][9]["air_flow"],state=data["us"][9]["state"],
			)
		f2[10] = Floor2CIU11(
			dateTime=timezone.now(), switch=data["us"][10]["switch"],temperature=data["us"][10]["temperature"], setTemp=data["us"][10]["set_temp"],
			opMode=data["us"][10]["op_mode"],airFlow=data["us"][10]["air_flow"],state=data["us"][10]["state"],
			)
		f2[11] = Floor2CIU12(
			dateTime=timezone.now(), switch=data["us"][11]["switch"],temperature=data["us"][11]["temperature"], setTemp=data["us"][11]["set_temp"],
			opMode=data["us"][11]["op_mode"],airFlow=data["us"][11]["air_flow"],state=data["us"][11]["state"],
			)

		for f in f2:
			f.save()
		f2s = Floor2CIUs (
				u1=f2[0],
				u2=f2[1],
				u3=f2[2],
				u4=f2[3],
				u5=f2[4],
				u6=f2[5],
				u7=f2[6],
				u8=f2[7],
				u9=f2[8],
				u10=f2[9],
				u11=f2[10],
				u12=f2[11]
			).save()
	except Exception, e:
		log.error(str(e))
	return True

def save_ciu3(data):
	# 3층 실내기 상태 저장
	f3 = [None]*12
	try:
		f3[0] = Floor3CIU1(
			dateTime=timezone.now(), switch=data["us"][0]["switch"],temperature=data["us"][0]["temperature"], setTemp=data["us"][0]["set_temp"],
			opMode=data["us"][0]["op_mode"],airFlow=data["us"][0]["air_flow"],state=data["us"][0]["state"],
			)
		f3[1] = Floor3CIU2(
			dateTime=timezone.now(), switch=data["us"][1]["switch"],temperature=data["us"][1]["temperature"], setTemp=data["us"][1]["set_temp"],
			opMode=data["us"][1]["op_mode"],airFlow=data["us"][1]["air_flow"],state=data["us"][1]["state"],
			)
		f3[2] = Floor3CIU3(
			dateTime=timezone.now(), switch=data["us"][2]["switch"],temperature=data["us"][2]["temperature"], setTemp=data["us"][2]["set_temp"],
			opMode=data["us"][2]["op_mode"],airFlow=data["us"][2]["air_flow"],state=data["us"][2]["state"],
			)
		f3[3] = Floor3CIU4(
			dateTime=timezone.now(), switch=data["us"][3]["switch"],temperature=data["us"][3]["temperature"], setTemp=data["us"][3]["set_temp"],
			opMode=data["us"][3]["op_mode"],airFlow=data["us"][3]["air_flow"],state=data["us"][3]["state"],
			)
		f3[4] = Floor3CIU5(
			dateTime=timezone.now(), switch=data["us"][4]["switch"],temperature=data["us"][4]["temperature"], setTemp=data["us"][4]["set_temp"],
			opMode=data["us"][4]["op_mode"],airFlow=data["us"][4]["air_flow"],state=data["us"][4]["state"],
			)
		f3[5] = Floor3CIU6(
			dateTime=timezone.now(), switch=data["us"][5]["switch"],temperature=data["us"][5]["temperature"], setTemp=data["us"][5]["set_temp"],
			opMode=data["us"][5]["op_mode"],airFlow=data["us"][5]["air_flow"],state=data["us"][5]["state"],
			)
		f3[6] = Floor3CIU7(
			dateTime=timezone.now(), switch=data["us"][6]["switch"],temperature=data["us"][6]["temperature"], setTemp=data["us"][6]["set_temp"],
			opMode=data["us"][6]["op_mode"],airFlow=data["us"][6]["air_flow"],state=data["us"][6]["state"],
			)
		f3[7] = Floor3CIU8(
			dateTime=timezone.now(), switch=data["us"][7]["switch"],temperature=data["us"][7]["temperature"], setTemp=data["us"][7]["set_temp"],
			opMode=data["us"][7]["op_mode"],airFlow=data["us"][7]["air_flow"],state=data["us"][7]["state"],
			)
		f3[8] = Floor3CIU9(
			dateTime=timezone.now(), switch=data["us"][8]["switch"],temperature=data["us"][8]["temperature"], setTemp=data["us"][8]["set_temp"],
			opMode=data["us"][8]["op_mode"],airFlow=data["us"][8]["air_flow"],state=data["us"][8]["state"],
			)
		f3[9] = Floor3CIU10(
			dateTime=timezone.now(), switch=data["us"][9]["switch"],temperature=data["us"][9]["temperature"], setTemp=data["us"][9]["set_temp"],
			opMode=data["us"][9]["op_mode"],airFlow=data["us"][9]["air_flow"],state=data["us"][9]["state"],
			)
		f3[10] = Floor3CIU11(
			dateTime=timezone.now(), switch=data["us"][10]["switch"],temperature=data["us"][10]["temperature"], setTemp=data["us"][10]["set_temp"],
			opMode=data["us"][10]["op_mode"],airFlow=data["us"][10]["air_flow"],state=data["us"][10]["state"],
			)
		f3[11] = Floor3CIU12(
			dateTime=timezone.now(), switch=data["us"][11]["switch"],temperature=data["us"][11]["temperature"], setTemp=data["us"][11]["set_temp"],
			opMode=data["us"][11]["op_mode"],airFlow=data["us"][11]["air_flow"],state=data["us"][11]["state"],
			)

		for f in f3:
			f.save()
		f3s = Floor3CIUs (
				u1=f3[0],
				u2=f3[1],
				u3=f3[2],
				u4=f3[3],
				u5=f3[4],
				u6=f3[5],
				u7=f3[6],
				u8=f3[7],
				u9=f3[8],
				u10=f3[9],
				u11=f3[10],
				u12=f3[11]
			).save()
	except Exception, e:
		log.error(str(e))
	return True


def search_hp(start_date, end_date, count, excel):
	if excel:
		hp1 = HeatPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hp2 = HeatPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hp3 = HeatPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hp4 = HeatPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hp5 = HeatPump5Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hp6 = HeatPump6Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		hp1 = HeatPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hp2 = HeatPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hp3 = HeatPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hp4 = HeatPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hp5 = HeatPump5Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hp6 = HeatPump6Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += hp1.count()

	database_list = zip(list(hp1), list(hp2), list(hp3), list(hp4), list(hp5), list(hp6))
	data = {
		'database_list':database_list,
		'count': count,
	}
	return data
def search_cp(start_date, end_date, count, excel):
	if excel:
		cp1 = CirculatingPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		cp2 = CirculatingPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		cp1 = CirculatingPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		cp2 = CirculatingPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += cp1.count()

	database_list = zip(list(cp1), list(cp2))
	data = {
		'database_list':database_list,
		'count': count,
	}
	return data
def search_dwp(start_date, end_date, count, excel):
	if excel:
		dwp1 = DeepwellPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		dwp2 = DeepwellPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		dwp3 = DeepwellPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		dwp4 = DeepwellPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		temp = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		dwp1 = DeepwellPump1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		dwp2 = DeepwellPump2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		dwp3 = DeepwellPump3Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		dwp4 = DeepwellPump4Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		temp = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += dwp1.count()

	database_list = zip(list(dwp1), list(dwp2), list(dwp3), list(dwp4), list(temp))
	data = {
		'database_list':database_list,
		'count': count,
	}
	return data
def search_fm_cur(start_date, end_date, count, excel):
	if excel:
		cpfm = CPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		dwpfm = DWPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hein1 = TempHEIn1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		hein2 = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		heout1 = TempHEOut1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		heout2 = TempHEOut2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		cpfm = CPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		dwpfm = DWPFlowmeterLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hein1 = TempHEIn1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		hein2 = TempHEIn2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		heout1 = TempHEOut1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		heout2 = TempHEOut2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += cpfm.count()
	database_list = zip(list(cpfm), list(dwpfm), list(hein1), list(hein2), list(heout1), list(heout2))

	data = {
		'database_list': database_list,
		'count': count,
	}
	return data
def search_fm_int(start_date, end_date, count):
	# 적산유량
	cpfm2 = []; dwpfm2 = [];
	count = 0
	
	# 검색할 날짜 리스트
	start = dt.strptime(start_date, date_format)
	end = dt.strptime(end_date, date_format) - timezone.timedelta(days=1)
	num_date = end - start
	date_list = [end - timezone.timedelta(days=x) for x in range(num_date.days+1)]
	# log.debug(str(date_list))
	for date in date_list:
		d = dt.strftime(date, date_format)
		try:
			cpfm2.append(CPFlowmeterLogger.objects.filter(Q(dateTime__year=date.year), Q(dateTime__month=date.month), Q(dateTime__day=date.day)).latest('dateTime'))
			dwpfm2.append(DWPFlowmeterLogger.objects.filter(Q(dateTime__year=date.year), Q(dateTime__month=date.month), Q(dateTime__day=date.day)).latest('dateTime'))
		except:
			pass
	count = len(cpfm2)
	database_list = zip(cpfm2, dwpfm2)

	data = {
		'database_list': database_list,
		'count': count,
	}
	return data
def search_tw(start_date, end_date, count, excel):
	if excel:
		ab1 = TWAB1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		ab2 = TWAB2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		ib1 = TWIB1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		ij1 = TWIJ1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		sb1 = TWSB1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
		sb2 = TWSB2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		ab1 = TWAB1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		ab2 = TWAB2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		ib1 = TWIB1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		ij1 = TWIJ1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		sb1 = TWSB1Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
		sb2 = TWSB2Logger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += ab1.count()

	database_list = zip(list(ab1),list(ab2),list(ib1),list(ij1),list(sb1),list(sb2))
	data = {
		'database_list':database_list,
		'count': count,
	}
	return data
def search_power_cur(start_date, end_date, count, excel):
	# 순시전력
	if excel:
		power = PowerConsumptionLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		power = PowerConsumptionLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += power.count()
	database_list = list(power)

	data = {
		'database_list': database_list,
		'count': count,
	}
	return data
def search_power_int(start_date, end_date, count):
	# 적산전력
	power2 = [];
	count = 0
	
	# 검색할 날짜 리스트
	start = dt.strptime(start_date, date_format)
	end = dt.strptime(end_date, date_format) - timezone.timedelta(days=1)
	num_date = end - start
	date_list = [end - timezone.timedelta(days=x) for x in range(num_date.days+1)]
	# log.debug(str(date_list))
	for date in date_list:
		d = dt.strftime(date, date_format)
		# log.debug(str(date.day))
		try:
			power2.append(PowerConsumptionLogger.objects.filter(Q(dateTime__year=date.year), Q(dateTime__month=date.month), Q(dateTime__day=date.day)).latest('dateTime'))
		except:
			pass
	count = len(power2)
	database_list = power2

	data = {
		'database_list': database_list,
		'count': count,
	}
	return data
def search_cop(start_date, end_date, count, excel):
	if excel:
		cop = CoefficientOfPerformanceLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')
	else:
		cop = CoefficientOfPerformanceLogger.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
	count += cop.count()

	database_list = list(cop)
	data = {
		'database_list':database_list,
		'count': count,
	}
	return data


def search_database(obj, start_date, end_date, count=0, floor=0, name=0, excel=False):
	# 시간이 end_date 00:00:00이라 하루를 더해야 해당 날짜의 데이터가 검색됨
	end = dt.strptime(end_date, date_format) + timezone.timedelta(days=1)
	end_date = dt.strftime(end, date_format)

	if obj == 'hp':
		return search_hp(start_date, end_date, count=count, excel=excel)
	elif obj == 'cp':
		return search_cp(start_date, end_date, count=count, excel=excel)
	elif obj == 'dwp':
		return search_dwp(start_date, end_date, count=count, excel=excel)
	elif obj == 'fm-cur':
		return search_fm_cur(start_date, end_date, count=count, excel=excel)
	elif obj == 'fm-int':
		return search_fm_int(start_date, end_date, count=count)
	elif obj == 'tw':
		return search_tw(start_date, end_date, count=count, excel=excel)
	elif obj == 'power-cur':
		return search_power_cur(start_date, end_date, count=count, excel=excel)
	elif obj == 'power-int':
		return search_power_int(start_date, end_date, count=count)
	elif obj == 'cop':
		return search_cop(start_date, end_date, count=count, excel=excel)
	else: # ciu
		return search_ciu(start_date, end_date, count=count, floor=floor, name=name, excel=excel)


def search_ciu(start_date, end_date, count, floor, name, excel):
	if excel:
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
				
				count += d1.count()
				response_data = {
					"database":database1,
					"count":count,
				}
				# log.debug(str(len([database1])))
				# log.debug(str(len([database1][0])))

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
				
				count += d1.count()
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
				
				count += d1.count()
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
			count += d1.count()
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
	else:
		# 50개 씩
		if floor == '1':
			if name == '1':
				database = Floor1CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			elif name == '2':
				database = Floor1CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			elif name == '3':
				database = Floor1CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '4':
				database = Floor1CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '5':
				database = Floor1CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '6':
				database = Floor1CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '7':
				database = Floor1CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '8':
				database = Floor1CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '9':
				database = Floor1CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '10':
				database = Floor1CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '11':
				database = Floor1CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '12':
				database = Floor1CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '13':
				database = Floor1CIU13.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '14':
				database = Floor1CIU14.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			else: # (전체)
				d1 = Floor1CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
				d2 = Floor1CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
				d3 = Floor1CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d4 = Floor1CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d5 = Floor1CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d6 = Floor1CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d7 = Floor1CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d8 = Floor1CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d9 = Floor1CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d10 = Floor1CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d11 = Floor1CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d12 = Floor1CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d13 = Floor1CIU13.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d14 = Floor1CIU14.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				database1 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14]
				
				count += d1.count()
				response_data = {
					"database":database1,
					"count":count,
				}
				# log.debug(str(len([database1])))
				# log.debug(str(len([database1][0])))

		elif floor == '2':
			if name == '1':
				database = Floor2CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			elif name == '2':
				database = Floor2CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			elif name == '3':
				database = Floor2CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '4':
				database = Floor2CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '5':
				database = Floor2CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '6':
				database = Floor2CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '7':
				database = Floor2CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '8':
				database = Floor2CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '9':
				database = Floor2CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '10':
				database = Floor2CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '11':
				database = Floor2CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '12':
				database = Floor2CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			else: # (전체)
				d1 = Floor2CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
				d2 = Floor2CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
				d3 = Floor2CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d4 = Floor2CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d5 = Floor2CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d6 = Floor2CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d7 = Floor2CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d8 = Floor2CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d9 = Floor2CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d10 = Floor2CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d11 = Floor2CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d12 = Floor2CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				database2 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
				
				count += d1.count()
				response_data = {
					"database":database2,
					"count":count,
				}
		elif floor == '3':
			if name == '1':
				database = Floor3CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			elif name == '2':
				database = Floor3CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			elif name == '3':
				database = Floor3CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '4':
				database = Floor3CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '5':
				database = Floor3CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '6':
				database = Floor3CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '7':
				database = Floor3CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '8':
				database = Floor3CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '9':
				database = Floor3CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '10':
				database = Floor3CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '11':
				database = Floor3CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			elif name == '12':
				database = Floor3CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			else: # (전체)
				d1 = Floor3CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
				d2 = Floor3CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
				d3 = Floor3CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d4 = Floor3CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d5 = Floor3CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d6 = Floor3CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d7 = Floor3CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d8 = Floor3CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d9 = Floor3CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d10 = Floor3CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d11 = Floor3CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				d12 = Floor3CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
				database3 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
				
				count += d1.count()
				response_data = {
					"database":database3,
					"count":count,
				}
		else: # (전체)
			d1 = Floor1CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			d2 = Floor1CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			d3 = Floor1CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d4 = Floor1CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d5 = Floor1CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d6 = Floor1CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d7 = Floor1CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d8 = Floor1CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d9 = Floor1CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d10 = Floor1CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d11 = Floor1CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d12 = Floor1CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d13 = Floor1CIU13.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d14 = Floor1CIU14.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			database1 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14]
			d1 = Floor2CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			d2 = Floor2CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			d3 = Floor2CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d4 = Floor2CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d5 = Floor2CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d6 = Floor2CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d7 = Floor2CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d8 = Floor2CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d9 = Floor2CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d10 = Floor2CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d11 = Floor2CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d12 = Floor2CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			database2 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
			d1 = Floor3CIU1.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			d2 = Floor3CIU2.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50] 
			d3 = Floor3CIU3.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d4 = Floor3CIU4.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d5 = Floor3CIU5.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d6 = Floor3CIU6.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d7 = Floor3CIU7.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d8 = Floor3CIU8.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d9 = Floor3CIU9.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d10 = Floor3CIU10.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d11 = Floor3CIU11.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			d12 = Floor3CIU12.objects.filter(Q(dateTime__gte=start_date), Q(dateTime__lte=end_date)).order_by('-dateTime')[count:count+50]
			database3 = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12]
			database_list = [database1,database2,database3]
		
			count += d1.count()
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

	return response_data



