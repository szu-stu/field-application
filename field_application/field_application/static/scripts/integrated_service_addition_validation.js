
//@autor Dolby
//@Checker Jim

$(function(){
	$('#id_date_month, #id_date_day, #id_date_year').change(checkSunday426);// 综合服务楼426周日20:30-11:00仅供深大团委使用
	$('form').submit(checkSunday426);
	
	$('#id_date_month, #id_date_day, #id_date_year').change(checkNoon426);// 西南综合服务楼426会议室 周一到周五的12点半至14点半期间不可用
	$('form').submit(checkNoon426);
	$('#id_date_month, #id_date_day, #id_date_year').change(checkMonday101);//每周一晚18:00-22:00，综合服务楼101，深大艺术团戏剧分团使用。
	$('form').submit(checkMonday101);
	$('#id_date_month, #id_date_day, #id_date_year').change(checkFriday101);//每周五晚18:00-22:00，综合服务楼101，深大艺术团使用。
	$('form').submit(checkFriday101);
	$('#id_date_month, #id_date_day, #id_date_year').change(checkSaturday101);//每周六下午15:00-21:00，综合服务楼101，深大艺术团戏剧分团使用
	$('form').submit(checkSaturday101);
	$('#id_date_month, #id_date_day, #id_date_year').change(checkThursdayNav);///每周四晚19:00-22:00综合服务楼大厅，深大艺术团使用
	$('form').submit(checkThursdayNav);

});



//20:30-23:00
function checkSunday426(){
	var bannedPlaceBox = $('#id_place_3');
	var bannedTimeChkBoxs = $('#id_time_25,#id_time_26,#id_time_27,#id_time_28,#id_time_29');
	var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');
	var apartmentNameBox = $('#id_appartment_name').val();
	function checkApartment(apartmentNameBox){
		var allowableApartment = "深大团委";
		if (apartmentNameBox == allowableApartment) {
			return true;
		}
		else{
			return false;
		}
	}
	var bannedTimeChecked = false;
	for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
		if(bannedTimeChkBoxs[i].checked)
		{
			bannedTimeChecked = true;
			break;
		}
	}
	if(isDay([0]) && bannedPlaceBox.prop('checked') == true && bannedTimeChecked && checkApartment(apartmentNameBox) == false){
		timeErrorBox.text( '426会议室周日20:30-23:00供深大团委使用，不便之处请谅解，谢谢合作！' );
		alert('426会议室周日20:30-23:00供深大团委使用，不便之处请谅解，谢谢合作！');
		return false;
	}
	else{
		bannedTimeChkBoxs.removeAttr( 'disabled' );
		timeErrorBox.text('');
	}
}

//每周五晚18:00-22:00，综合服务楼110，仅供深大艺术团戏剧分团使用，每周五晚19:00-21:30，综合服务楼110，仅供深大艺术团民乐分团使用
function checkFriday101()
{
	var bannedPlaceBox = $('#id_place_0');
	var bannedTimeChkBoxs = $( '#id_time_20,#id_time_21,#id_time_22,#id_time_23,#id_time_24, #id_time_25, #id_time_26,#id_time_27' );
	var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');
	var apartmentNameBox = $('#id_appartment_name').val();
	function checkApartment(apartmentNameBox){
		var allowableApartment = "艺术团";
		if (apartmentNameBox == allowableApartment) {
			return true;
		}
		else{
			return false;
		}
	}
	var bannedTimeChecked = false;
	for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
		if(bannedTimeChkBoxs[i].checked)
		{
			bannedTimeChecked = true;
			break;
		}
	}
	if(isDay([5]) && bannedPlaceBox.prop('checked') == true && bannedTimeChecked && checkApartment(apartmentNameBox) == false){
		timeErrorBox.text( '每周五晚18:00-22:00，综合服务楼101，仅供深大艺术团使用，不便之处请谅解，谢谢合作！' );
		alert('每周五晚18:00-22:00，综合服务楼101，仅供深大艺术团使用，不便之处请谅解，谢谢合作！');
		return false;
	}
	else{
		bannedTimeChkBoxs.removeAttr( 'disabled' );
		timeErrorBox.text('');
	}
}

//每周1玩18.00 到 22.00 深大艺术团戏剧分团
function checkMonday101()
{
	var bannedPlaceBox = $('#id_place_0');
	var bannedTimeChkBoxs = $( '#id_time_20,#id_time_21,#id_time_22,#id_time_23,#id_time_24, #id_time_25, #id_time_26,#id_time_27' );
	var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');
	var apartmentNameBox = $('#id_appartment_name').val();
	function checkApartment(apartmentNameBox){
		var allowableApartment = "艺术团";
		if (apartmentNameBox == allowableApartment) {
			return true;
		}
		else{
			return false;
		}
	}
	var bannedTimeChecked = false;
	for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
		if(bannedTimeChkBoxs[i].checked)
		{
			bannedTimeChecked = true;
			break;
		}
	}
	if(isDay([1]) && bannedPlaceBox.prop('checked') == true && bannedTimeChecked && checkApartment(apartmentNameBox) == false){
		timeErrorBox.text( '每周一晚18:00-22:00，综合服务楼101，仅供深大艺术团戏剧分团使用，不便之处请谅解，谢谢合作！' );
		alert('每周一晚18:00-22:00，综合服务楼101，仅供深大艺术团戏剧分团使用，不便之处请谅解，谢谢合作！');
		return false;
	}
	else{
		bannedTimeChkBoxs.removeAttr( 'disabled' );
		timeErrorBox.text('');
	}
}

//每周6下午15.00 到 21.00 深大艺术团戏剧分团
function checkSaturday101()
{
	var bannedPlaceBox = $('#id_place_0');
	var bannedTimeChkBoxs = $( '#id_time_14,#id_time_15,#id_time_16,#id_time_17,#id_time_18,#id_time_19,#id_time_20,#id_time_21_#id_time_22,#id_time_23,#id_time_24,#id_time_25' );
	var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');
	var apartmentNameBox = $('#id_appartment_name').val();
	function checkApartment(apartmentNameBox){
		var allowableApartment = "艺术团";
		if (apartmentNameBox == allowableApartment) {
			return true;
		}
		else{
			return false;
		}
	}
	var bannedTimeChecked = false;
	for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
		if(bannedTimeChkBoxs[i].checked)
		{
			bannedTimeChecked = true;
			break;
		}
	}
	if(isDay([6]) && bannedPlaceBox.prop('checked') == true && bannedTimeChecked && checkApartment(apartmentNameBox) == false){
		timeErrorBox.text( '每周六下午15:00-21:00，综合服务楼101，仅供深大艺术团戏剧分团使用，不便之处请谅解，谢谢合作！' );
		alert('每周六下午15:00-21:00，综合服务楼101，仅供深大艺术团戏剧分团使用，不便之处请谅解，谢谢合作！');
		return false;
	}
	else{
		bannedTimeChkBoxs.removeAttr( 'disabled' );
		timeErrorBox.text('');
	}
}

//每周四晚上19.-22. 深圳大学艺术团训练使用，综合服务楼大厅
function checkThursdayNav(){
	var bannedPlaceBox = $('#id_place_4');
	var bannedTimeChkBoxs = $( '#id_time_22,#id_time_23,#id_time_24, #id_time_25, #id_time_26,#id_time_27' );
	var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');
	var apartmentNameBox = $('#id_appartment_name').val();
	function checkApartment(apartmentNameBox){
		var allowableApartment = "艺术团";
		if (apartmentNameBox == allowableApartment) {
			return true;
		}
		else{
			return false;
		}
	}
	var bannedTimeChecked = false;
	for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
		if(bannedTimeChkBoxs[i].checked)
		{
			bannedTimeChecked = true;
			break;
		}
	}
	if(isDay([4]) && bannedPlaceBox.prop('checked') == true && bannedTimeChecked && checkApartment(apartmentNameBox) == false){
		timeErrorBox.text( '每周四下午19:00-22:00，综合服务楼101，仅供深大艺术团使用，不便之处请谅解，谢谢合作！' );
		alert('每周四下午19:00-22:00，综合服务楼101，仅供深大艺术团使用，不便之处请谅解，谢谢合作！');
		return false;
	}
	else{
		bannedTimeChkBoxs.removeAttr( 'disabled' );
		timeErrorBox.text('');
	}
}
// 西南综合服务楼426会议室 周一到周五的12点半至14点半期间不可用
function checkNoon426(){
	var bannedPlaceBox = $('#id_place_3');
	var bannedTimeChkBoxs = $( '#id_time_9,#id_time_10,#id_time_11,#id_time_12' );
	var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');
	var apartmentNameBox = $('#id_appartment_name').val();
	var bannedTimeChecked = false;

	function checkApartment(apartmentNameBox){
		var allowableApartment1 = "公会";
		var allowableApartment2 = "督导室";
		var allowableApartment3 = "离退办";
		if (apartmentNameBox == allowableApartment1||apartmentNameBox == allowableApartment2||apartmentNameBox == allowableApartment3) {
			return false;
		}
		else{
			return true;
		}
	}
	for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
		if(bannedTimeChkBoxs[i].checked)
		{
			bannedTimeChecked = true;
			break;
		}
	}
	if(isDay([1,2,3,4,5]) && bannedPlaceBox.prop('checked') == true && bannedTimeChecked&&checkApartment(apartmentNameBox)){
		timeErrorBox.text( '西南综合服务楼426会议室 周一到周五的12点半至14点半期间不可用,谢谢合作!' );
		alert('西南综合服务楼426会议室 周一到周五的12点半至14点半期间不可用,谢谢合作!');
		return false;
	}
	else{
		bannedTimeChkBoxs.removeAttr( 'disabled' );
		timeErrorBox.text('');
	}
}




var contains = function(arr,obj) {
    var i = arr.length;
    while (i--) {
        if (arr[i] === obj) {
            return true;
        }
    }
    return false;
}

function isDay(daylist)//daylist is a list 0 is Sunday,1 is Monday,eg: daylist=[1,2];
{
	var year=$( '#id_date_year'  ).val(),
		month=$( '#id_date_month' ).val(),
		day=$( '#id_date_day'   ).val(),
		applDate = new Date( year,month-1, day ),
		applDay=applDate.getDay();

	if( year == '' ||month == '' || day == '' ){
		return;
	}
	if( contains(daylist,applDay) ){
		return true;
	}
	else{
		return false;
	}

}



// 从地址中获取值
function getParameterByName(name) {
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
	var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
	results = regex.exec(location.search);
	return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
