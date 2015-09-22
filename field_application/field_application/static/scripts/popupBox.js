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
		 	callback: function(){ this.close(); }
		 	}]
		});
}
function appListGen( ary, place ){
	ary = eval('('+ary+')');

	var appList = document.createElement( 'table' );
	appList.className = 'app_table';

	var appListTR = appList.insertRow( 0 );

	var appListTD = appListTR.insertCell( 0 );
	appListTD.className = 'app_table_title';
	appListTD.colSpan = "2";
	appListTD.appendChild( document.createTextNode( "点击标题查看详细内容" ) );

	var i;
	for( i = 0; i < ary.length ; i++ ){
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
		
		appListTD = appListTR.insertCell( -1 );
		appListTD.className = 'app_sing_appTime';
		appListTD.innerHTML = ary[i].app_time;

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

	var width = 500;
	if( place == 'meeting_room' ){
		width: 700;
	}

	var dialog = artDlgBox.dialog({
				  title: "",

				  width: width,
				 height: 300,

				   lock: true,
				 button: [{
				 		    name: "返回",
				 		callback: function(){ this.close() }
				 }]
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
	  //{ index: "plan_file"              , 'text': "策划文件"        },
		{ index: "remarks"                , 'text': "备注"           },
		{ index: "conflict_apps"		  , 'text': "时间重叠的申请" }
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

	indexToText['integrated_service'] = [
		{ index: "topic"                  , 'text': "活动主题"   },
		{ index: "organization"           , 'text': "申请部门"   },
		{ index: "applicant_name"         , 'text': "申请人姓名" },
		{ index: "applicant_stu_id"       , 'text': "申请人学号"     },
		{ index: "applicant_college"      , 'text': "申请人学院"     },
		{ index: "applicant_phone_number" , 'text': "联系电话"   },
		{ index: "place"                  , 'text': "申请所用场地"   },
		{ index: "date"                   , 'text': "申请日期"   },	
		{ index: "time"                   , 'text': "活动时段"   },
		{ index: "summary"                , 'text': "活动内容简介"   },
		{ index: "remarks"                , 'text': "备注"           },
		{ index: "conflict_apps"		  , 'text': "时间重叠的申请" },

		{ index: "sponsor"                , 'text': "赞助商"         },
		{ index: "sponsorship"            , 'text': "赞助金额及物品" },
		{ index: "sponsorship_usage"      , 'text': "赞助财物用途"   },
	];

	var appFormTable = document.createElement( 'table' );
	appFormTable.className = 'app_table';
	if( place == 'meeting_room' ){
		appFormTable.className += ' app_table_with_conf';
	}
	else{
		appFormTable.className += ' app_info_table';
	}
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
		    	case 'conflict_apps':
		    		var conflictAppsText = new Array();
		    		var conf_apps = detail['conflict_apps'];

		    		if( conf_apps.length == 0 ){
		    			detail['conflict_apps'] = "无";
		    		}
		    		else{
			    		var j = 0;
			    		for( j = 0; j <conf_apps.length; j++ ) {
			    			var currentConflictApp = conf_apps[ j ];
			    			currentConflictApp['approved'] = (currentConflictApp['approved']==true)?"已审批":"未审批";
			    			conflictAppsText[j]= '<table class="conf_app_table">\
			    									<tr class="conflict_app_info">\
			    										<td class="conflict_app_info_title">会议主题：</td><td>'+
			    										currentConflictApp['meeting_topic']+
			    										'</td>\
			    									</tr>\
			    									<tr class="conflict_app_info">\
			    										<td class="conflict_app_info_title">申请组织：</td><td>'+
			    										currentConflictApp['org']+
			    										'</td>\
			    									</tr>\
			    									<tr class="conflict_app_info">\
			    										<td class="conflict_app_info_title">申请时间：</td><td>'+
			    										currentConflictApp['apply_time']+
			    										'</td>\
			    									</tr>\
			    									<tr class="conflict_app_info">\
			    										<td class="conflict_app_info_title">审批情况：</td><td>'+
			    										currentConflictApp['approved']+
			    										'</td>\
			    									</tr>\
			    									<tr class="conflict_times">\
			    										<td class="conflict_app_info_title">冲突时间：</td>\
			    										<td colSpan="2">'+
			    											currentConflictApp['conflict_time'].join(',')+
			    										'</td>\
			    									</tr>\
			    								  </table>';

			    		};
		    			detail['conflict_apps'] =  conflictAppsText.join( " " );
		    		}

		    		break;
		    }

		    appFormTableTD.innerHTML =  detail[iTT[i]['index']];

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
