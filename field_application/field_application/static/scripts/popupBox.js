/**
 * @author skys215
 * @uses   Popup a box showing detailed informations
 */

function genTable( ary ){
	ary = eval('('+ary+')');
	var appList      = document.createElement( 'table' );
	appList.className = 'app_table';
	var appListTBody = document.createElement( 'tbody' );
	appList.appendChild( appListTBody );

	var appListTR = appList.insertRow();
	var appListTD = appListTR.insertCell();
	appListTD.className = 'app_table_title';
	appListTD.appendChild( document.createTextNode( "点击标题查看详细内容" ) );

	var i;
	for( i = 0; i <= ary.length - 1; i++ ){
		appListTR = appList.insertRow();
		appListTD = appListTR.insertCell();
		appListTD.className = 'app_sing_cond';
		var approvedText = ( ary[i]['approved'] == 'False' ) ? '>未审批' : ' class="app_approved">已审批';
		appListTD.appendChild( document.createTextNode( ary[i]['title'] ) );
		appListTD.innerHTML+="&nbsp;&nbsp;【<span"+approvedText+"</span>】";
	}
	return appList;
}

function popupBox( applAry ){
    var artDlgBox;
    try{
		artDlgBox = art;
    }
    catch(err){
		alert( "ArtDialog not found." );	
    }
    var content = genTable( applAry );

    var artdialog = art.dialog({
		  title: "申请列表",
		content: content,

		  width: 500,
		 height:300,
	})

}
