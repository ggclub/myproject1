#-*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.core.urlresolvers import reverse

from .views import *

urlpatterns = [
	url('^', include('django.contrib.auth.urls')),
	url(r'^$', index, name='index'),
	url(r'^reload_display/$', reload_display, name='reload_display'),
	url(r'^specs/$', specs, name='specs'),
	url(r'^setting_cp/$', setting_cp, name='setting_cp'),
	url(r'^show_database/$', show_database, name='show_db'),
	url(r'^setting_cp_done/$', setting_cp_done, name='setting_cp_done'),
	url(r'^page_request/$', page_request, name='page_request'),
	url(r'^toggle_switch/$', toggle_switch, name='toggle_switch'),
	url(r'^floor_change/$', floor_change, name='floor_change'),
	url(r'^change_ciuonhp/$', change_ciuonhp, name='change_ciuonhp'),
	# Nav bar
	# 동작설정
	url(r'^setting_mode/$', setting_mode, name='setting_mode'),
	url(r'^setting_mode_confirm/$', setting_mode_confirm, name='setting_mode_confirm'),
	url(r'^operation_control/$', operation_control, name='operation_control'),
	# url(r'^set_db_save_interval/$', set_db_save_interval, name='set_db_save_interval'),
	# DB 검색
	url(r'^show_database/$', show_database, name='show_database'),
	url(r'^search_db_excel/$', search_db_excel, name='search_db_excel'),
	url(r'^search_db_ciu/$', search_db_ciu, name='search_db_ciu'),
	url(r'^search_db_ciu_result/$', search_db_ciu_result, name='search_db_ciu_result'),
	url(r'^search_db_hp/$', search_db_hp, name='search_db_hp'),
	url(r'^search_db_hp_result/$', search_db_hp_result, name='search_db_hp_result'),
	url(r'^search_db_cp/$', search_db_cp, name='search_db_cp'),
	url(r'^search_db_cp_result/$', search_db_cp_result, name='search_db_cp_result'),
	url(r'^search_db_dwp/$', search_db_dwp, name='search_db_dwp'),
	url(r'^search_db_dwp_result/$', search_db_dwp_result, name='search_db_dwp_result'),
	url(r'^search_db_fm/$', search_db_fm, name='search_db_fm'),
	url(r'^search_db_fm_result/$', search_db_fm_result, name='search_db_fm_result'),
	url(r'^search_db_power/$', search_db_power, name='search_db_power'),
	url(r'^search_db_power_result/$', search_db_power_result, name='search_db_power_result'),
	# 결과 다운로드
	url(r'^download_result/(?P<o>.*)/$', download_result, name='download_result'),
]
