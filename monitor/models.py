#-*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone


SWITCH_CHOICES = (
	('ON', 'On'),
	('OFF', 'Off'),
)

MANUAL = 'MN'
AUTO = 'AT'
OPMODE_CHOICES = (
	(MANUAL, '수동'),
	(AUTO, '자동'),
)

# switch control
class OperationSwitchControl(models.Model):
	dateTime = models.DateTimeField()
	LOCATION_CHOICES = (
		('AT', '자동 모드'),
		('MN', '수동 모드'),
		('CL', '냉방 모드'),
		('HT', '난방 모드'),
		('HP1', '히트 펌프 1'),
		('HP2', '히트 펌프 2'),
		('HP3', '히트 펌프 3'),
		('HP4', '히트 펌프 4'),
		('HP5', '히트 펌프 5'),
		('HP6', '히트 펌프 6'),
		('DWP1', '심정 펌프 1'),
		('DWP2', '심정 펌프 2'),
		('DWP3', '심정 펌프 3'),
		('DWP4', '심정 펌프 4'),
		('CP1', '순환 펌프 1'),
		('CP2', '순환 펌프 2'),
		('IV', '인버터'),
	)
	location = models.CharField(max_length=4, choices=LOCATION_CHOICES)
	OP_SWITCH_CHOICES = (
		('ON', 'On'),
		('OFF', 'Off'),
		('N/A', 'n/a'),
	)
	switch = models.CharField(max_length=3, choices=OP_SWITCH_CHOICES)
	def __str__(self):
		return '{}, location: {}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.location, self.switch)


# pump
APPROPRIATE='AP'
NOTAPPROPRIATE='NA'
WATERLEVEL_CHOICES = (
	(APPROPRIATE, '적정'),
	(NOTAPPROPRIATE, '부적정'),
)
class DeepwellPump1Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 	
	waterLevel = models.CharField(max_length=2, choices=WATERLEVEL_CHOICES, default="AP")
	def __str__(self):
		return u'{}, {}-{}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch)
	# def __unicode__(self):
	# 	return unicode(self.DeepwellPump1Logger)

class DeepwellPump2Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 	
	waterLevel = models.CharField(max_length=2, choices=WATERLEVEL_CHOICES, default="AP")
	def __str__(self):
		return u'{}, {}-{}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch)
	# def __unicode__(self):
	# 	return unicode(self.DeepwellPump2Logger)

class DeepwellPump3Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 	
	waterLevel = models.CharField(max_length=2, choices=WATERLEVEL_CHOICES, default="AP")
	def __str__(self):
		return u'{}, {}-{}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch)
	# def __unicode__(self):
	# 	return unicode(self.DeepwellPump3Logger)

class DeepwellPump4Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 	
	waterLevel = models.CharField(max_length=2, choices=WATERLEVEL_CHOICES, default="AP")
	def __str__(self):
		return u'{}, {}-{}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch)
	# def __unicode__(self):
	# 	return unicode(self.DeepwellPump4Logger)

CP_ID_CHOICES = (
	(1, '1'),
	(2, '2'),
)
class CirculatingPump1Logger(models.Model):
	dateTime = models.DateTimeField()
	CPID = models.SmallIntegerField(choices=CP_ID_CHOICES, default=1)
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	Hz = models.SmallIntegerField(default=0)
	flux = models.SmallIntegerField(default=0)
	def __str__(self):
		return u'{}, {}-{}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch)

class CirculatingPump2Logger(models.Model):
	dateTime = models.DateTimeField()
	CPID = models.SmallIntegerField(choices=CP_ID_CHOICES, default=2)
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	Hz = models.SmallIntegerField(default=0)
	flux = models.SmallIntegerField(default=0)
	def __str__(self):
		return u'{}, {}-{}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch)


# inverter
# class InverterLogger(models.Model):
# 	dateTime = models.DateTimeField()
# 	INVERTER_ID_CHOICES = (
# 		(1, 'Inverter1'),
# 		(2, 'Inverter2'),
# 	)
# 	inverterID = models.SmallIntegerField(choices=INVERTER_ID_CHOICES, default=1)
# 	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
# 	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
# 	RPM = models.SmallIntegerField()
# 	Hz = models.IntegerField(null=True, blank=True)
# 	def __str__(self):
# 		return u'{}, {}-{}, RPM: {}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch, self.RPM)
# 	# def __unicode__(self):
# 	# 	return u'{}, {}-{}, RPM: {}'.format(str(self.dateTime.replace(microsecond=0)), self.opMode, self.switch, self.RPM)


# flowmeter
class DWPFlowmeterLogger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField()
	currentFlux = models.SmallIntegerField()
	integralFlux = models.IntegerField()
	velocity = models.FloatField()
	def __str__(self):
		return '{}, current: {}'.format(str(self.dateTime.replace(microsecond=0)), self.currentFlux)
	# def __unicode__(self):
	# 	return unicode(self.DWPFlowmeterLogger)

class CPFlowmeterLogger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField()
	currentFlux = models.SmallIntegerField()
	integralFlux = models.IntegerField()
	velocity = models.FloatField(default=0)
	def __str__(self):
		return '{}, current: {}'.format(str(self.dateTime.replace(microsecond=0)), self.currentFlux)
	# def __unicode__(self):
	# 	return unicode(self.CPFlowmeterLogger)

class TempHEIn1Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHEIn1Logger)

class TempHEOut1Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHEOut1Logger)

class TempHEIn2Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHEIn2Logger)

class TempHEOut2Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHEOut2Logger)

class TempHPIn1Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPIn1Logger)

class TempHPOut1Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPOut1Logger)

class TempHPIn2Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPIn2Logger)

class TempHPOut2Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPOut2Logger)

class TempHPIn3Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPIn3Logger)

class TempHPOut3Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPOut3Logger)

class TempHPIn4Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPIn4Logger)

class TempHPOut4Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPOut4Logger)

class TempHPIn5Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPIn5Logger)

class TempHPOut5Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPOut5Logger)

class TempHPIn6Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPIn6Logger)

class TempHPOut6Logger(models.Model):
	dateTime = models.DateTimeField()
	temperature = models.FloatField(default=0.0)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.temperature)
	# def __unicode__(self):
	# 	return unicode(self.TempHPOut6Logger)


def get_HPI1():
	return TempHPIn1Logger.objects.latest('temperature')
def get_HPO1():
	return TempHPOut1Logger.objects.latest('temperature')
def get_HPI2():
	return TemperatureLogger.objects.latest('dateTime').HPI2
def get_HPO2():
	return TemperatureLogger.objects.latest('dateTime').HPO2
def get_HPI3():
	return TemperatureLogger.objects.latest('dateTime').HPI3
def get_HPO3():
	return TemperatureLogger.objects.latest('dateTime').HPO3
def get_HPI4():
	return TemperatureLogger.objects.latest('dateTime').HPI4
def get_HPO4():
	return TemperatureLogger.objects.latest('dateTime').HPO4
def get_HPI5():
	return TemperatureLogger.objects.latest('dateTime').HPI5
def get_HPO5():
	return TemperatureLogger.objects.latest('dateTime').HPO5
def get_HPI6():
	return TemperatureLogger.objects.latest('dateTime').HPI6
def get_HPO6():
	return TemperatureLogger.objects.latest('dateTime').HPO6

# thermometer
class TemperatureLogger(models.Model):
	dateTime = models.DateTimeField()
	HEI1 = models.ForeignKey(TempHEIn1Logger)
	HEO1 = models.ForeignKey(TempHEOut1Logger)
	HEI2 = models.ForeignKey(TempHEIn2Logger)
	HEO2 = models.ForeignKey(TempHEOut2Logger)
	HPI1 = models.ForeignKey(TempHPIn1Logger)
	HPO1 = models.ForeignKey(TempHPOut1Logger)
	HPI2 = models.ForeignKey(TempHPIn2Logger)
	HPO2 = models.ForeignKey(TempHPOut2Logger)
	HPI3 = models.ForeignKey(TempHPIn3Logger)
	HPO3 = models.ForeignKey(TempHPOut3Logger)
	HPI4 = models.ForeignKey(TempHPIn4Logger)
	HPO4 = models.ForeignKey(TempHPOut4Logger)
	HPI5 = models.ForeignKey(TempHPIn5Logger)
	HPO5 = models.ForeignKey(TempHPOut5Logger)
	HPI6 = models.ForeignKey(TempHPIn6Logger)
	HPO6 = models.ForeignKey(TempHPOut6Logger)
	def __str__(self):
		return str(str(self.dateTime.replace(microsecond=0)))
	# def __unicode__(self):
	# 	return unicode(self.TemperatureLogger)





# heat pump
class HeatPump1Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	tempIn = models.ForeignKey(TempHPIn1Logger)
	tempOut = models.ForeignKey(TempHPOut1Logger)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.switch)
	# def __unicode__(self):
	# 	return unicode(self.HeatPump1Logger)

class HeatPump2Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	tempIn = models.ForeignKey(TempHPIn2Logger)
	tempOut = models.ForeignKey(TempHPOut2Logger)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.switch)
	# def __unicode__(self):
	# 	return unicode(self.HeatPump2Logger)

class HeatPump3Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	tempIn = models.ForeignKey(TempHPIn3Logger)
	tempOut = models.ForeignKey(TempHPOut3Logger)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.switch)
	# def __unicode__(self):
	# 	return unicode(self.HeatPump3Logger)

class HeatPump4Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	tempIn = models.ForeignKey(TempHPIn4Logger)
	tempOut = models.ForeignKey(TempHPOut4Logger)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.switch)
	# def __unicode__(self):
	# 	return unicode(self.HeatPump4Logger)

class HeatPump5Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	tempIn = models.ForeignKey(TempHPIn5Logger)
	tempOut = models.ForeignKey(TempHPOut5Logger)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.switch)
	# def __unicode__(self):
	# 	return unicode(self.HeatPump5Logger)

class HeatPump6Logger(models.Model):
	dateTime = models.DateTimeField()
	opMode = models.CharField(max_length=2, choices=OPMODE_CHOICES, default=AUTO)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	tempIn = models.ForeignKey(TempHPIn6Logger)
	tempOut = models.ForeignKey(TempHPOut6Logger)
	def __str__(self):
		return '{}, {}'.format(str(self.dateTime.replace(microsecond=0)), self.switch)
	# def __unicode__(self):
	# 	return unicode(self.HeatPump6Logger)


# power consumption
class PowerConsumptionLogger(models.Model):
	dateTime = models.DateTimeField()
	currentPowerConsumption = models.FloatField()
	integralPowerConsumption = models.FloatField()
	def __str__(self):
		return '{}, current: {}'.format(str(self.dateTime.replace(microsecond=0)), self.currentPowerConsumption)
	# def __unicode__(self):
	# 	return unicode(self.PowerConsumptionLogger)

# refrigeration ton
class RefrigerationTonLogger(models.Model):
	dateTime = models.DateTimeField()
	RT = models.FloatField()
	def __str__(self):
		return '{}, RT: {}'.format(str(self.dateTime.replace(microsecond=0)), self.RT)
	# def __unicode__(self):
	# 	return unicode(self.RefrigerationTonLogger)


# tube well 
class TubeWellLogger(models.Model):
	T1level = models.FloatField()
	T1temp = models.FloatField()
	T2level = models.FloatField()
	T2temp = models.FloatField()
	T3level = models.FloatField()
	T3temp = models.FloatField()
	T4level = models.FloatField()
	T4temp = models.FloatField()
	# def __unicode__(self):
	# 	return unicode(self.TubeWellLogger)


################ CEILING INDOOR UNIT #########################
ACOOL = 'CL'
AHEAT = 'HT'
AAIR = 'AR'
AAUTO = 'AT'
AIR_OP_MODE = (
	(ACOOL, '냉방'),
	(AHEAT, '난방'),
	(AAIR, '송풍'),
	(AAUTO, '자동'),
)
WEAK = 'WK'
NORMAL = 'NM'
STRONG = 'ST'
AIRFLOW_CHOICES = (
	(WEAK, '약풍'),
	(NORMAL, '중풍'),
	(STRONG, '강풍'),
)
ERROR = 'ER'
STATE_CHOICES = (
	(ERROR, '에러'),
	(NORMAL, '정상'),
)

FL1_CHOICES = (
	('EMR', '방재실'),
	('LBY1', '로비1'),
	('LBY2', '로비2'),
	('NUR', '수유실'),
	('LIC', '저소득층상담실'),
	('CONF', '회의실'),
	('OFC1', '사무실1'),
	('OFC2', '사무실2'),
	('OFC3', '사무실3'),
	('RRR', '주민등록실'),
	('MDF','MDF실'),
	('TRT', '진료실'),
	('WWR', '사무대기실'),
	('PHR', '접종보건실')
)

class Floor1CIU1(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='EMR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU2(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='LBY1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU3(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='LBY2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU4(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='NUR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU5(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='LIC')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU6(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='CONF')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU7(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='OFC1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU8(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='OFC2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU9(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='OFC3')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU10(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='RRR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU11(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='MDF')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU12(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='TRT')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU13(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='WWR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIU14(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=1)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL1_CHOICES, default='PHR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)


FL2_CHOICES = (
	('HAL2', '2층 홀'),
	('CTR', '조정실'),
	('PPR', '준비실'),
	('HOT', '면장실'),
	('EDU1', '교육실1'),
	('EDU2', '교육실2'),
	('EDU3', '교육실3'),
	('FMC1', '농업인상담실1'),
	('FMC2', '농업인상담실2'),
	('LIB', '서고'),
	('FTC1', '면대1'),
	('FTC2', '면대2'),
)
class Floor2CIU1(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='HAL2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU2(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='CTR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU3(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='PPR')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU4(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='HOT')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU5(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='EDU1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU6(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='EDU2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU7(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='EDU3')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU8(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='FMC1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU9(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='FMC2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU10(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='LIB')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU11(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='FTC1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor2CIU12(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=2)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL2_CHOICES, default='FTC2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)


FL3_CHOICES = (
	('HAL3', '3층 홀'),
	('AUD1', '강당1'),
	('AUD2', '강당2'),
	('MPR1', '다목적홀1'),
	('MPR2', '다목적홀2'),
	('MPR3', '다목적홀3'),
	('HR1', '홀공간1'),
	('HR2', '홀공간2'),
	('LE11', '평생학습실1-1'),
	('LE12', '평생학습실1-2'),
	('LE21', '평생학습실2-1'),
	('LE22', '평생학습실2-2'),
)
class Floor3CIU1(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='HAL3')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU2(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='AUD1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU3(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='AUD2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU4(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='MPR1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU5(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='MPR2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU6(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='MPR3')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU7(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='HR1')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU8(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='HR2')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU9(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='LE11')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU10(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='LE12')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU11(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='LE21')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor3CIU12(models.Model):
	dateTime = models.DateTimeField()
	floor = models.SmallIntegerField(default=3)
	switch = models.CharField(max_length=3, choices=SWITCH_CHOICES, default='OFF') 
	temperature = models.FloatField(default=20.1)
	setTemp = models.FloatField(default=19)
	opMode = models.CharField(max_length=2, choices=AIR_OP_MODE, default='AT')
	airFlow = models.CharField(max_length=2, choices=AIRFLOW_CHOICES, default='ST')
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='NM')
	location = models.CharField(max_length=4, choices=FL3_CHOICES, default='LE22')
	def __str__(self):
		return '{}, {}, {}'.format(self.dateTime.replace(microsecond=0), self.switch, self.temperature)

class Floor1CIUs(models.Model):
	u1 = models.ForeignKey(Floor1CIU1)
	u2 = models.ForeignKey(Floor1CIU2)
	u3 = models.ForeignKey(Floor1CIU3)
	u4 = models.ForeignKey(Floor1CIU4)
	u5 = models.ForeignKey(Floor1CIU5)
	u6 = models.ForeignKey(Floor1CIU6)
	u7 = models.ForeignKey(Floor1CIU7)
	u8 = models.ForeignKey(Floor1CIU8)
	u9 = models.ForeignKey(Floor1CIU9)
	u10 = models.ForeignKey(Floor1CIU10)
	u11 = models.ForeignKey(Floor1CIU11)
	u12 = models.ForeignKey(Floor1CIU12)
	u13 = models.ForeignKey(Floor1CIU13)
	u14 = models.ForeignKey(Floor1CIU14)

class Floor2CIUs(models.Model):
	u1 = models.ForeignKey(Floor2CIU1)
	u2 = models.ForeignKey(Floor2CIU2)
	u3 = models.ForeignKey(Floor2CIU3)
	u4 = models.ForeignKey(Floor2CIU4)
	u5 = models.ForeignKey(Floor2CIU5)
	u6 = models.ForeignKey(Floor2CIU6)
	u7 = models.ForeignKey(Floor2CIU7)
	u8 = models.ForeignKey(Floor2CIU8)
	u9 = models.ForeignKey(Floor2CIU9)
	u10 = models.ForeignKey(Floor2CIU10)
	u11 = models.ForeignKey(Floor2CIU11)
	u12 = models.ForeignKey(Floor2CIU12)

class Floor3CIUs(models.Model):
	u1 = models.ForeignKey(Floor3CIU1)
	u2 = models.ForeignKey(Floor3CIU2)
	u3 = models.ForeignKey(Floor3CIU3)
	u4 = models.ForeignKey(Floor3CIU4)
	u5 = models.ForeignKey(Floor3CIU5)
	u6 = models.ForeignKey(Floor3CIU6)
	u7 = models.ForeignKey(Floor3CIU7)
	u8 = models.ForeignKey(Floor3CIU8)
	u9 = models.ForeignKey(Floor3CIU9)
	u10 = models.ForeignKey(Floor3CIU10)
	u11 = models.ForeignKey(Floor3CIU11)
	u12 = models.ForeignKey(Floor3CIU12)






################ DEVICE SPEC #########################

class FlowmeterInfo(models.Model):
	name = models.CharField(max_length=10)
	size = models.CharField(max_length=15)
	measureGauge = models.CharField(max_length=15)
	inputPower = models.CharField(max_length=30)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name

class InverterInfo(models.Model):
	name = models.CharField(max_length=15)
	size = models.CharField(max_length=15)
	motorHP = models.CharField(max_length=20)
	ratedCapacity = models.CharField(max_length=15)
	ratedCurrent = models.CharField(max_length=15)
	frequency = models.CharField(max_length=15)
	maxVoltage = models.CharField(max_length=25)
	power =  models.CharField(max_length=50)
	coolingSystem = models.CharField(max_length=25)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name

class WattHourMeterInfo(models.Model):
	name = models.CharField(max_length=25)
	size = models.CharField(max_length=40)
	ratedVoltage = models.CharField(max_length=25)
	ratedCurrent = models.CharField(max_length=15)
	accuracy = models.CharField(max_length=25)
	constant = models.CharField(max_length=25)
	outputPulse = models.CharField(max_length=25)
	pulseSpec = models.CharField(max_length=100)	
	powerConsumption = models.CharField(max_length=15)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name

class HeatExchangerInfo(models.Model):
	name = models.CharField(max_length=15)
	maxPressure = models.CharField(max_length=15)
	tempRange = models.CharField(max_length=15)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name

class HeatPumpInfo(models.Model):
	name = models.CharField(max_length=15)
	voltage = models.CharField(max_length=30)
	capacity = models.CharField(max_length=15)
	refrigerant = models.CharField(max_length=15)
	size = models.CharField(max_length=30)
	weight = models.CharField(max_length=15)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name

class CirculatingPumpInfo(models.Model):
	name = models.CharField(max_length=15)
	flux = models.CharField(max_length=15)
	suction = models.CharField(max_length=15)
	motorHP = models.CharField(max_length=15)
	maxPressure = models.CharField(max_length=60)
	motor = models.CharField(max_length=15)
	voltage = models.CharField(max_length=100)
	frequency = models.CharField(max_length=15)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name

class DeepwellPumpInfo(models.Model):
	name = models.CharField(max_length=15)
	volume = models.CharField(max_length=15)
	output = models.CharField(max_length=25)
	power = models.CharField(max_length=25)
	height = models.CharField(max_length=15)
	length = models.CharField(max_length=15)
	diameter = models.CharField(max_length=15)
	quantity = models.SmallIntegerField()
	def __str__(self):
		return self.name


class CiuOnHeatPump1(models.Model):
	u1 = models.ForeignKey(Floor3CIU9)
	u2 = models.ForeignKey(Floor3CIU10)
	u3 = models.ForeignKey(Floor3CIU11)
	u4 = models.ForeignKey(Floor3CIU12)
	def to_dict(self):
		return {"u1":self.u1, "u2":self.u2, "u3":self.u3, "u4":self.u4}
	def items(self):
		return [self.u1,self.u2,self.u3,self.u4]

class CiuOnHeatPump2(models.Model):
	u1 = models.ForeignKey(Floor2CIU8)
	u2 = models.ForeignKey(Floor2CIU9)
	u3 = models.ForeignKey(Floor2CIU10)
	u4 = models.ForeignKey(Floor2CIU11)
	u5 = models.ForeignKey(Floor2CIU12)
	def to_dict(self):
		return {"u1":self.u1, "u2":self.u2, "u3":self.u3, "u4":self.u4, "u5":self.u5}
	def items(self):
		return [self.u1,self.u2,self.u3,self.u4,self.u5]

class CiuOnHeatPump3(models.Model):
	u1 = models.ForeignKey(Floor2CIU2)
	u2 = models.ForeignKey(Floor2CIU3)
	u3 = models.ForeignKey(Floor2CIU4)
	u4 = models.ForeignKey(Floor2CIU5)
	u5 = models.ForeignKey(Floor2CIU6)
	u6 = models.ForeignKey(Floor2CIU7)
	def to_dict(self):
		return {"u1":self.u1, "u2":self.u2, "u3":self.u3, "u4":self.u4, "u5":self.u5, "u6":self.u6}
	def items(self):
		return [self.u1,self.u2,self.u3,self.u4,self.u5,self.u6]

class CiuOnHeatPump4(models.Model):
	u1 = models.ForeignKey(Floor1CIU1)
	u2 = models.ForeignKey(Floor1CIU2)
	u3 = models.ForeignKey(Floor1CIU3)
	u4 = models.ForeignKey(Floor1CIU4)
	u5 = models.ForeignKey(Floor1CIU5)
	u6 = models.ForeignKey(Floor2CIU1)
	u7 = models.ForeignKey(Floor3CIU1)
	def to_dict(self):
		return {"u1":self.u1, "u2":self.u2, "u3":self.u3, "u4":self.u4, "u5":self.u5, "u6":self.u6, "u7":self.u7}
	def items(self):
		return [self.u1,self.u2,self.u3,self.u4,self.u5,self.u6,self.u7]

class CiuOnHeatPump5(models.Model):
	u1 = models.ForeignKey(Floor1CIU6)
	u2 = models.ForeignKey(Floor1CIU7)
	u3 = models.ForeignKey(Floor1CIU8)
	u4 = models.ForeignKey(Floor1CIU9)
	u5 = models.ForeignKey(Floor1CIU10)
	u6 = models.ForeignKey(Floor1CIU11)
	u7 = models.ForeignKey(Floor1CIU12)
	u8 = models.ForeignKey(Floor1CIU13)
	u9 = models.ForeignKey(Floor1CIU14)
	def to_dict(self):
		return {"u1":self.u1, "u2":self.u2, "u3":self.u3, "u4":self.u4, "u5":self.u5, "u6":self.u6, "u7":self.u7, "u8":self.u8, "u9":self.u9}
	def items(self):
		return [self.u1,self.u2,self.u3,self.u4,self.u5,self.u6,self.u7,self.u8,self.u9]

class CiuOnHeatPump6(models.Model):
	u1 = models.ForeignKey(Floor3CIU2)
	u2 = models.ForeignKey(Floor3CIU3)
	u3 = models.ForeignKey(Floor3CIU4)
	u4 = models.ForeignKey(Floor3CIU5)
	u5 = models.ForeignKey(Floor3CIU6)
	u6 = models.ForeignKey(Floor3CIU7)
	u7 = models.ForeignKey(Floor3CIU8)
	def to_dict(self):
		return {"u1":self.u1, "u2":self.u2, "u3":self.u3, "u4":self.u4, "u5":self.u5, "u6":self.u6, "u7":self.u7}
	def items(self):
		return [self.u1,self.u2,self.u3,self.u4,self.u5,self.u6,self.u7]










