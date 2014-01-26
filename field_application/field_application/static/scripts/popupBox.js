/**
 * @author skys215
 * @uses   Popup a box showing detailed informations
 */

function showAppList( applAry, place ){
    var artDlgBox;
    try{
		artDlgBox = art;
    }
    catch( err ){
		console.log( "ArtDialog not found." );	
    }

	var content = appListGen( applAry, place );

    var artdialog = art.dialog({
		  title: "申请列表",
		content: content,

		  width: 500,
		 height: 300,

		   lock: true,
		 button:[{
		 	    name: '关闭',
		 	callback: function(){ this.close(); },
		 	}],
		});
}
function appListGen( ary, place ){
	ary = eval('('+ary+')');

	var appList = document.createElement( 'table' );
	appList.className = 'app_table';

	var appListTR = appList.insertRow();

	var appListTD = appListTR.insertCell();
	appListTD.className = 'app_table_title';
	appListTD.appendChild( document.createTextNode( "点击标题查看详细内容" ) );


	var i;
	for( i = 0; i <= ary.length - 1; i++ ){
		appListTR = appList.insertRow();
		appListTD = appListTR.insertCell();
		appListTD.className = 'app_sing_cond';

		var detailLink  = '';
			detailLink += '<a href="#" onclick="javascript:showAppForm(\'' + ary[i]['id'] + '\', \'' + place + '\')">';
			detailLink += ary[i]['title'];
			detailLink += '</a>';
		var approvedText = ( ary[i]['approved'] == 'False' ) ? '>未审批' : ' class="app_approved">已审批';

		appListTD.innerHTML += detailLink;
		appListTD.innerHTML += "&nbsp;&nbsp;【<span" + approvedText + "</span>】";
	}

	return appList;
}
// Didn't filter appId is an integer or not
function showAppForm( appId, place ){
	var artDlgBox;
	try{
		artDlgBox = art;
	}
	catch( err ){
		console.log( "ArtDialog not found." );
	}

	var xmlhttp;
	if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange=function(){
		if ( xmlhttp.readyState == 4 && xmlhttp.status == 200 ){
			var content = genAppInfoTable( xmlhttp.responseText, place );

			var artdialog = art.dialog({
				     id: "app_info",
				  title: "",
				content: content,

				  width: 500,
				 height: 300,	

				   lock: true,
				 button: [{
				 		    name: "返回",
				 		callback: function(){ this.close() },
				 }],
			});
		}
	}

	xmlhttp.open( "GET", "../get_detail/?id=" + appId , false );
	xmlhttp.send();

}
/***** generate application info table *****/
function genAppInfoTable( detail, place ){
	detail = eval('('+detail+')');
	detail['place'] = place;
	var indexToText = [];

	indexToText['south_stadium'] = [
		{ index: "activity"               , 'text': "活动项目"          },
		{ index: "organization"           , 'text': "申请部门"          },
		{ index: "applicant_name"         , 'text': "申请人姓名"        },
		{ index: "applicant_phone_number" , 'text': "联系电话"          },
	  //{ index: "place"                   , 'text': "申请场地"         },
		{ index: "date"                   , 'text': "使用日期"          },	
		{ index: "time"                   , 'text': "使用时间"          },
		{ index: "activity_summary"       , 'text': "活动简介"          },
		{ index: "plan_file"              , 'text': "策划文件"          },
	  //{ index: "remarks"                , 'text': "备注"              },

	  //{ index: "sponsor"                , 'text': "赞助商"            },
	  //{ index: "sponsorship"            , 'text': "赞助金额及物品"    },
	  //{ index: "sponsorship_usage"      , 'text': "赞助财物用途"      },

	  //{ index: "approved"               , 'text': "审批情况"          },
	  //{ index: "application_time"       , 'text': "申请时间"          },
	];

	indexToText['student_activity_center'] = indexToText['south_stadium'];

	var appFormTable = document.createElement( 'table' );
	appFormTable.className = 'app_table app_info_table';

	var i;
	var iTT = indexToText[place];
	for( i = 0; i < iTT.length; i++ ){
		var appFormTableTD, appFormTableTR;

		appFormTableTR = appFormTable.insertRow();

			appFormTableTD = appFormTableTR.insertCell();
			appFormTableTD.className = 'app_info_title';
		    appFormTableTD.appendChild( document.createTextNode( iTT[i]['text'] + "：" ) );

		    appFormTableTD = appFormTableTR.insertCell();
			appFormTableTD.className = 'app_info_cont';

		    var insertText = '';
		    switch( iTT[i]['index'] ){
		    	case 'plan_file':
		    		if( detail[iTT[i]['index']] !='' )
		    			insertText = '<a href="' + detail[iTT[i]['index']] + '">下载</a>';
		    		else
		    			insertText = '无文件可供下载';	
		    		break;
		    	case 'approved':
		    		console.log( typeof detail['approved']);
		    		detail['approved'] = ( detail['approved'] == true ) ? "已审批": "未审批";
		    	default:
		    		 insertText = detail[iTT[i]['index']];
		    }
		    appFormTableTD.innerHTML = insertText;

		//end inserting row
	}
	
	return appFormTable;
}