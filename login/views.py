﻿#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

# import logging
# log = logging.getLogger(__name__)

# Create your views here.
def index(request):
	username = password = state = ''
	# log.debug("index")

	# if already logged in
	from monitor.views import index
	if request.user.is_authenticated():
		# log.debug("user authenticated")
		return index(request)


	if request.method == 'POST':
		# login submit button
		if 'submit' in request.POST:
			username = request.POST.get('username')
			password = request.POST.get('password')

			# request.session.set_expiry(0)
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)

				# if request.POST.get('remember', None):
					# request.session.set_expiry(0)

				state = "Login success."
				return index(request)

				# url='login/success.html'
				# response_data = {"state":state}
				# response_data.update(csrf(request))
				# return render(request, url, response_data)
			else :
				state = "incorrect username and/or password."

		# logout button
		if 'logout' in request.POST:
			logout(request)
			return HttpResponseRedirect('/')


	url='login/index.html'
	response_data = {
		'state': state,
	}
	response_data.update(csrf(request))
	return render(request, url, response_data)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')


def change_password_page(request):
	html = render_to_response('login/change_password_page.html', {}, RequestContext(request))
	return HttpResponse(html)

def change_password_done(request):
	# if request.POST.get('check_new_pws', 'false'):
	# 	return HttpResponseRedirect('login/change_password_page')

	cur_pw = request.POST.get('cur_pw')
	new_pw1 = request.POST.get('new_pw1')
	new_pw2 = request.POST.get('new_pw2')
	user = authenticate(username='admin', password=cur_pw)
	if user is not None:
		logging.debug("user is not none")
		if new_pw1 == new_pw2:
			# 비밀번호 변경 완료
			user.set_password(new_pw1)
			user.save()
			logging.debug("password changed")
		else:	
			response_data = {
				"message": "새로운 비밀번호가 일치하지 않습니다.",
			}
			url = 'login/change_password_page.html'
			html = render_to_string(url, response_data, RequestContext(request))
			return HttpResponse(html)

	else:
		response_data = {
			"message": "비밀번호가 틀렸습니다.",
		}
		url = 'login/change_password_page.html'
		html = render_to_string(url, response_data, RequestContext(request))
		return HttpResponse(html)

	response_data = {
		"message": "password changed"
	}
	logout(request)
	logging.debug("logout on password change")
	return render(request, "login/index.html", {})

def on_mode_change(request):
	return render(request, 'login/on_mode_change.html')

def on_mode_confirm(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		content = {}
		if user is not None:
	    		if user.username == 'iljoog':
	        			# login(request, user)
	        			content = {'confirm': True}
    			else:
	        			# Return a 'disabled account' error message
	        			content = {'error_msg': '수동 모드 변경 권한이 없는 계정입니다.'}
		else:
	    		# Return an 'invalid login' error message.
	    		content = {'error_msg': '아이디 혹은 비밀번호가 일치하지 않습니다.'}
	
		return render(request, 'login/on_mode_change.html', content)

