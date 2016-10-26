$(function(){
	//$('#id_date_month, #id_date_day, #id_date_year').change(checkMonday);
	//$('[id^="id_place_"]').change(checkMonday);
	//$('form').submit(checkMonday);
	//$('#id_date_month, #id_date_day, #id_date_year').change(checkSunday);
	//$('form').submit(checkSunday);
});

function checkMonday(){
		var bannedPlaceBox = $('#id_place_1');
		var bannedTimeChkBoxs = $( '#id_time_8, #id_time_9, #id_time_10, #id_time_11 ' );
		var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');

        var bannedTimeChecked = false;
        for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
            if(bannedTimeChkBoxs[i].checked)
            {
                bannedTimeChecked = true;
                break;
            }
        }
		if(isMonday() && bannedPlaceBox.prop('checked') == true && bannedTimeChecked){
			timeErrorBox.text( '石头坞一楼会议室周一12：00-14：00暂停申请，谢谢合作!' );
			alert('石头坞一楼会议室周一12：00-14：00暂停申请，谢谢合作!')
			return false;
		}
		else{
			bannedTimeChkBoxs.removeAttr( 'disabled' );
			timeErrorBox.text('');
		}
}
/*
function checkSunday(){
		var bannedPlaceBox = $('#id_place_0');
		var bannedTimeChkBoxs = $( '#id_time_24, #id_time_25, #id_time_26, #id_time_27, #id_time_28, #id_time_29 ' );
		var timeErrorBox = $( '#id_time_29' ).closest('ul').siblings('div.error');

        var bannedTimeChecked = false;
        for(var i = 0; i < bannedTimeChkBoxs.length; i++) {
            if(bannedTimeChkBoxs[i].checked)
            {
                bannedTimeChecked = true;
                break;
            }
        }
        
		if(isSunday() && bannedPlaceBox.prop('checked') == true && bannedTimeChecked){
			timeErrorBox.text( '307会议室周日20：00-23：00暂停申请，谢谢合作!' );
			alert('307会议室周日20：00-23：00暂停申请，谢谢合作!')
			return false;
		}
		else{
			bannedTimeChkBoxs.removeAttr( 'disabled' );
			timeErrorBox.text('');
		}
}
*/
function isMonday(){
	if( $( '#id_date_year'  ).val() == '' ||
	    $( '#id_date_month' ).val() == '' || 
	    $( '#id_date_day'   ).val() == '' ){
		return;
	}
	
	var applDay = new Date( $( '#id_date_year'  ).val(), $( '#id_date_month' ).val()-1, $( '#id_date_day'   ).val() );
	if( applDay.getDay() == 1 ){
		return true;
	}
	else{
		return false;
	}
}

function isSunday(){
	if( $( '#id_date_year'  ).val() == '' ||
	    $( '#id_date_month' ).val() == '' || 
	    $( '#id_date_day'   ).val() == '' ){
		return;
	}
	var applDay = new Date( $( '#id_date_year'  ).val(), $( '#id_date_month' ).val()-1, $( '#id_date_day'   ).val() );
	if( applDay.getDay() == 0 ){
		return true;
	}
	else{
		return false;
	}
}


function checkConflict( ){
	var app_info = [];

	// check is modifying or adding
	if( getParameterByName('id') != '' ){
		app_info.push( 'id=' + getParameterByName('id') );
	}

	var select_time = $('label[for^=id_time_]').children('input:checked').map(function(){
		return $(this).attr('value');
	}).get().join(',');
	app_info.push( 'time=' + select_time);
	app_info.push( 'date=' + [$('#id_date_year').val(), $('#id_date_month').val(), $('#id_date_day').val()].join('-'));
	app_info.push( 'place=' + $('label[for^=id_place_]').children('input:checked').val());
	var time_index = {
		'8点-8点30分':0,
		'8点30分-9点':1,
		'9点-9点30分':2,
		'9点30分-10点':3,
		'10点-10点30分':4,
		'10点30分-11点':5,
		'11点-11点30分':6,
		'11点30分-12点':7,
		'12点-12点30分':8,
		'12点30分-13点':9,
		'13点-13点30分':10,
		'13点30分-14点':11,
		'14点-14点30分':12,
		'14点30分-15点':13,
		'15点-15点30分':14,
		'15点30分-16点':15,
		'16点-16点30分':16,
		'16点30分-17点':17,
		'17点-17点30分':18,
		'17点30分-18点':19,
		'18点-18点30分':20,
		'18点30分-19点':21,
		'19点-19点30分':22,
		'19点30分-20点':23,
		'20点-20点30分':24,
		'20点30分-21点':25,
		'21点-21点30分':26,
		'21点30分-22点':27,
		'22点-22点30分':28,
		'22点30分-23点':29,
	}
	$.ajax({
	    url: '../conflict_for_form/',
	    data: app_info.join('&'),
	    success: function( conflict_apps ) {
	    	var alert_text = [];
	    	if( conflict_apps.length > 0 ){
	    		alert_text.push( '下列申请时间与您欲申请的时间有重叠，\n**有可能**导致您的申请不能通过审批。' );
		    	alert_text.push( '--------------------------------------------' );

	    		var i;
	    		var conflict_time_json = {};
	    		var conflict_time_array = [];
	    		var c_t_array=[];
		    	for( i = 0; i < conflict_apps.length; i++ ){
		    		for ( j=0; j<conflict_apps[i]['conflict_time'].length; j++){
		    			conflict_time_json[conflict_apps[i]['conflict_time'][j]]='';
		    		}
		    	}
		    	for( c_t in conflict_time_json){
		    		c_t_array[time_index[c_t]]=c_t;
		    	}
		    	for( c_t in c_t_array ){
		    		conflict_time_array.push( c_t_array[c_t] );
		    	}
		    	alert_text.push( conflict_time_array.join(',\n'));
	    		alert_text.push( '--------------------------------------------' );
		    	alert_text.push( '点击"确定"继续提交，点击"取消"修改时间。' );

		        var continue_submit_form = confirm( alert_text.join('\n') );
		        if( continue_submit_form ){
		        	$('#application_form').submit();
	    		}
	        }
	        else{
	        	$('#application_form').submit();
	        }
	    	
	    }
	});
	//return false;
}

// 从地址中获取值
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
