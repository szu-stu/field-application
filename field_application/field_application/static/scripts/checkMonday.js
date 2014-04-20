$(function(){
	$('#id_date_month, #id_date_day, #id_date_year').change(checkMonday);
	$('[id^="id_place_"]').change(checkMonday);
	$('form').submit(checkMonday);

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
			bannedTimeChkBoxs.attr( 'disabled', 'disabled' );
			timeErrorBox.text( '石头坞一楼会议室周一12：00-14：00暂停申请，谢谢合作!' );
			return false;
		}
		else{
			bannedTimeChkBoxs.removeAttr( 'disabled' );
			timeErrorBox.text('');
		}
}

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
