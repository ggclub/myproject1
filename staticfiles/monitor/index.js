jQuery(function($){

// // 초기 세팅
// $(document).ready(function () {
// 	$('#cl-status').addClass('sys-selected');
// 	$('#mn-status').addClass('sys-selected');

// 	var btns = $('.btn-status');
// 	$.each(btns, function(i, val) {
// 		// alert(val.value);
// 		if(val.innerText === "OFF"){
// 			$(this).removeClass('status-on');
// 			$(this).addClass('status-off');
// 		} else {
// 			$(this).removeClass('status-off');
// 			$(this).addClass('status-on');
// 		}
// 	});
// 	$.each($('.hp-status'), function(i, val) {
// 		if(val.innerText === "OFF"){
// 			$(this).removeClass('status-on');
// 			$(this).addClass('status-off');
// 		} else {
// 			$(this).removeClass('status-off');
// 			$(this).addClass('status-on');
// 		}
// 		$(this).attr('disabled', true);
// 		$('.hp-status').removeClass('btn-default');
// 	});
// });


// $(document).ready(function () { 
// 	// 냉방 버튼 클릭
// 	$('.btn-coolMode').on('click', function setCoolImg(){
// 		$('.btn-heatMode').removeClass('sys-selected');
// 		$('.btn-coolMode').addClass('sys-selected');
// 		$('#left').css("background-image", "url(/static/monitor/cool_bg.jpg)");
// 	});
// 	// 난방 버튼 클릭
// 	$('.btn-heatMode').on('click', function setHeatImg(){
// 		$('.btn-coolMode').removeClass('sys-selected');
// 		$('.btn-heatMode').addClass('sys-selected');
// 		$('#left').css("background-image", "url(/static/monitor/heat_bg.jpg)");
// 	});
// 	// 자동 버튼 클릭
// 	$('.btn-auto').on('click', function setHeatImg(){
// 		$('.btn-manual').removeClass('sys-selected');
// 		$('.btn-auto').addClass('sys-selected');
// 		$('.btn-status').attr('disabled', true);
// 		$('.btn-status').removeClass('btn-default');
// 	});
// 	// 수동 버튼 클릭
// 	$('.btn-manual').on('click', function setHeatImg(){
// 		$('.btn-auto').removeClass('sys-selected');
// 		$('.btn-manual').addClass('sys-selected');
// 		$('.btn-status').removeAttr('disabled');
// 		$('.btn-status').addClass('btn-default');
// 	});


// 	// 실내기 그림 표시
// 	// 1층
// 	$('#floor1-nav').on('click', function () {
// 		$('.slides').find('li').css('display', 'none');
// 		var img = $('#floor1').css('display', 'list-item')
// 	});
// 	// 2층
// 	$('#floor2-nav').on('click', function () {
// 		$('.slides').find('li').css('display', 'none');
// 		$('#floor2').css('display', 'list-item')
// 	});
// 	// 3층
// 	$('#floor3-nav').on('click', function () {
// 		$('.slides').find('li').css('display', 'none');
// 		$('#floor3').css('display', 'list-item')
// 	});


// 	// 장비 스펙 표시
// 	$('.device').on('click', function () {
// 		var dev = this.id;
// 		$('.left').addClass('show-spec');
// 		$('iframe').css('display', 'block');
// 	});

// });



//  End jQuery
});
