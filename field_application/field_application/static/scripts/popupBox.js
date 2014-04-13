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

    artDlgBox.dialog({
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

	var appListTR = appList.insertRow( 0 );

	var appListTD = appListTR.insertCell( 0 );
	appListTD.className = 'app_table_title';
	appListTD.appendChild( document.createTextNode( "点击标题查看详细内容" ) );


	var i;
	for( i = 0; i <= ary.length - 1; i++ ){
		appListTR = appList.insertRow( -1 );
		appListTD = appListTR.insertCell( -1 );
		appListTD.className = 'app_sing_cond';

		var detailLink  = '';
			detailLink += '<a href="" onclick="javascript:showAppForm(\'' + ary[i]['id'] + '\', \'' + place + '\'); return false;">';
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

	var dialog = artDlgBox.dialog({
				  title: "",

				  width: 500,
				 height: 300,

				   lock: true,
				 button: [{
				 		    name: "返回",
				 		callback: function(){ this.close() },
				 }],
			});

	//artDialog built in ajax   
	$.ajax({
	    url: '../get_detail/?id=' + appId,
	    success: function( data ) {
	        dialog.content( genAppInfoTable( data, place ) );
	    },
	    cache: false
	});
}
/***** generate application info table *****/
function genAppInfoTable( detail, place ){
	detail = eval('('+detail+')');
	
	var indexToText = [];

	indexToText['south_stadium'] = [
		{ index: "activity"               , 'text': "活动项目"       },
		{ index: "organization"           , 'text': "申请部门"       },
		{ index: "applicant_name"         , 'text': "申请人姓名"     },
		{ index: "applicant_stu_id"       , 'text': "申请人学号"     },
		{ index: "applicant_college"      , 'text': "申请人学院"     },
		{ index: "applicant_name"         , 'text': "申请人姓名"     },
		{ index: "applicant_phone_number" , 'text': "联系电话"       },
	  //{ index: "place"                   , 'text': "申请场地"      },
		{ index: "date"                   , 'text': "使用日期"       },	
		{ index: "time"                   , 'text': "使用时间"       },
		{ index: "activity_summary"       , 'text': "活动简介"       },
		{ index: "plan_file"              , 'text': "策划文件"       },
	  //{ index: "remarks"                , 'text': "备注"           },

	    { index: "sponsor"                , 'text': "赞助商"         },
	    { index: "sponsorship"            , 'text': "赞助金额及物品" },
	    { index: "sponsorship_usage"      , 'text': "赞助财物用途"   },

	  //{ index: "approved"               , 'text': "审批情况"       },
	  //{ index: "application_time"       , 'text': "申请时间"       },
	];

	indexToText['student_activity_center'] = [
		{ index: "activity"               , 'text': "活动项目"       },
		{ index: "organization"           , 'text': "申请部门"       },
		{ index: "applicant_name"         , 'text': "申请人姓名"     },
		{ index: "applicant_stu_id"       , 'text': "申请人学号"     },
		{ index: "applicant_college"      , 'text': "申请人学院"     },
		{ index: "applicant_name"         , 'text': "申请人姓名"     },
		{ index: "applicant_phone_number" , 'text': "联系电话"       },
		
		{ index: "date"                   , 'text': "使用日期"       },	
		{ index: "time"                   , 'text': "使用时间"       },
		{ index: "activity_summary"       , 'text': "活动简介"       },
		{ index: "plan_file"              , 'text': "策划文件"       },

	    { index: "sponsor"                , 'text': "赞助商"         },
	    { index: "sponsorship"            , 'text': "赞助金额及物品" },
	    { index: "sponsorship_usage"      , 'text': "赞助财物用途"   },

	    { index: "approved"               , 'text': "审批情况"       },
	    { index: "application_time"       , 'text': "申请时间"       },
	];

	indexToText['meeting_room'] = [
		{ index: "meeting_topic"          , 'text': "会议主题"   },
		{ index: "organization"           , 'text': "申请部门"   },
		{ index: "applicant_name"         , 'text': "申请人姓名" },
		{ index: "applicant_stu_id"       , 'text': "申请人学号"     },
		{ index: "applicant_college"      , 'text': "申请人学院"     },
		{ index: "applicant_phone_number" , 'text': "联系电话"   },
		{ index: "place"                  , 'text': "会议地址"   },
		{ index: "date"                   , 'text': "会议日期"   },	
		{ index: "time"                   , 'text': "会议时间"   },
		{ index: "meeting_summary"        , 'text': "会议简介"   },
	  //{ index: "plan_file"              , 'text': "策划文件"   },
		{ index: "remarks"                , 'text': "备注"       },
	];

	indexToText['exhibit'] = [
		{ index: "activity"               , 'text': "活动项目"       },
		{ index: "organization"           , 'text': "申请部门"       },
		{ index: "applicant_name"         , 'text': "申请人姓名"     },
		{ index: "applicant_stu_id"       , 'text': "申请人学号"     },
		{ index: "applicant_college"      , 'text': "申请人学院"     },
		{ index: "applicant_phone_number" , 'text': "联系电话"       },
		{ index: "exhibition"             , 'text': "展览内容"       },
		{ index: "exhibit_board_number"   , 'text': "使用展板"       },
		{ index: "place"                  , 'text': "活动地址"       },
		{ index: "start_date"             , 'text': "活动开始时间"   },
		{ index: "end_date"               , 'text': "活动结束时间"   },
		{ index: "time"                   , 'text': "活动时段"       },

	    { index: "sponsor"                , 'text': "赞助商"          },
	    { index: "sponsorship"            , 'text': "赞助金额及物品"  },
	    { index: "sponsorship_usage"      , 'text': "赞助财物用途"    },

		{ index: "activity_summary" , 'text': "活动简介"              },
		{ index: "remarks" , 'text': "备注" },
		{ index: "plan_file" , 'text': "策划文件" },
	];

	indexToText['publicity'] = [
		{ index: "activity"               , 'text': "活动项目" 		 },
		{ index: "organization"           , 'text': "申请部门"	 	 },
		{ index: "applicant_name"         , 'text': "申请人姓名" 	 },
		{ index: "applicant_stu_id"       , 'text': "申请人学号"     },
		{ index: "applicant_college"      , 'text': "申请人学院"     },
		{ index: "applicant_phone_number" , 'text': "联系电话" 		 },
		{ index: "activity_type"          , 'text': "活动类型" 		 },
		{ index: "place"                  , 'text': "活动地址"       },
		{ index: "start_date"             , 'text': "活动开始时间"   },
		{ index: "end_date"               , 'text': "活动结束时间"   },
		{ index: "time"                   , 'text': "活动时段"       },

		{ index: "sponsor"                , 'text': "赞助商"         },
		{ index: "sponsorship"            , 'text': "赞助金额及物品" },
		{ index: "sponsorship_usage"      , 'text': "赞助财物用途"   },
		
		{ index: "activity_summary"       , 'text': "活动简介"		 },
		{ index: "remarks"                , 'text': "备注" 			 },
		{ index: "plan_file"              , 'text': "策划文件" 		 },
	];


	var appFormTable = document.createElement( 'table' );
	appFormTable.className = 'app_table app_info_table';

	var i;
	var iTT = indexToText[place];
	var appFormTableTR, appFormTableTD;
	for( i = 0; i < iTT.length; i++ ){

		appFormTableTR = appFormTable.insertRow( i );

			appFormTableTD = appFormTableTR.insertCell( -1 );
			appFormTableTD.className = 'app_info_title';
		    appFormTableTD.appendChild( document.createTextNode( iTT[i]['text'] + "：" ) );

		    appFormTableTD = appFormTableTR.insertCell( -1 );
			appFormTableTD.className = 'app_info_cont';

		    var insertText = '';
		    switch( iTT[i]['index'] ){
		    	case 'plan_file':
		    		if( detail[iTT[i]['index']] !='' )
		    			detail['plan_file'] = '<a href="' + detail[iTT[i]['index']] + '">下载</a>';
		    		else
		    			detail['plan_file'] = '无文件可供下载';
		    		break;
		    	case 'approved':
		    		detail['approved'] = ( detail['approved'] == true ) ? "已审批": "未审批";
		    		break;
		    }
		    insertText = detail[iTT[i]['index']];
		    appFormTableTD.innerHTML = insertText;

		//end inserting row
	}

	if( detail['user_is_manager'] === true ){
		appFormTableTR = appFormTable.insertRow( i );
		appFormTableTD = appFormTableTR.insertCell( -1 );
		appFormTableTD.colSpan = 2;
		var linkAdd = '/' + place + '/manager_approve/?id=' + detail['id'];
		var linkText = ( detail['approved'] == true ) ? "解除通过": "通过审批"
		appFormTableTD.innerHTML = '<a href="' + linkAdd + '">' + linkText + '</a>';
	}
	
	return appFormTable;
}
