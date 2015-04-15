var path = "";
var base_url = "http://203.195.151.157:7900";

$(document).ready(
	function(){
		bindEvent();
});

//绑定事件
function bindEvent() {
	document.onkeydown = function(e){
	    // 兼容FF和IE和Opera
		var theEvent = e || window.event;
		var code = theEvent.keyCode || theEvent.which || theEvent.charCode;
		if (code == 13){
			login();
	    }
	};
}

//防js注入等
function isValid(str) {
	re= /script|<|>/i;
	return !re.test(str);
}
//字符串非空判断
function isEmpty(str) {
	return (str == null || str.length <= 0);
}

function textChange(textId, action) {
	if($.browser.msie)
	{
		$("#"+textId).bind("propertychange", action);
	}
	else
	{
		$("#"+textId).bind("blur", action);
	}
}

function showCount(tid, sid, limitCount) {
	var strChar = $(tid).val();
	var charCount = strChar.length;
	if(charCount<limitCount){
		$(sid).text('还能输入'+(limitCount-charCount)+'个字');
	}else{
		alert('输入数字超过最大限制！');
		$(tid).value=strChar;
	}
}

/**
 * 时间格式  "yyyy-MM-dd HH:ss:mm"
 */
function ftime(date) {
	if(date != null){
		return date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+' '+date.getHours()+':'+date.getMinutes()+':'+date.getSeconds();
	}else{
		return "0000-00-00 00:00:00";
	}
}

function getCookie(name) {
    var r = top.document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function ajax_post(path, data, callback){
	if(callback==undefined){
		callback=function(result){};
	}
	data["_xsrf"] = getCookie("_xsrf");
	$.ajax({
			type: "POST",
			url: path,
			async:false,
			data: data ,
			dataType: 'json',//返回值类型 一般设置为json
			success: function (result, textStatus){//请求成功后回调函数。这个方法有两个参数：服务器返回数据，返回状态。data类型由dataType决定
				callback(result);
			},
			error: function (XMLHttpRequest, textStatus, errorThrown){//默认: 自动判断 (xml 或 html)) 请求失败时将调用此方法。这个方法有三个参数：XMLHttpRequest 对象，错误信息，（可能）捕获的错误对象。通常情况下textStatus和errorThown只有其中一个有值
				try{
					var result = jQuery.parseJSON(XMLHttpRequest.responseText);
					callback(result);
				}catch(e){
					alert("submit error!");
				}
			}
	});
}

function ajax_upload(path, data, fileid, callback){
	if(callback==undefined){
		callback=function(result){};
	}
	data["_xsrf"] = getCookie("_xsrf");
	$.ajax({
			type: "POST",
			url: path,
			secureuri:false,//一般设置为false
			fileElementId:fileid,//文件上传空间的id属性  <input type="file" id="file" name="file" />
			data: data ,
			dataType: 'json',//返回值类型 一般设置为json
			//async:false,
			//contentType: "application/json",
			success: function (result, textStatus){//请求成功后回调函数。这个方法有两个参数：服务器返回数据，返回状态。data类型由dataType决定
				callback(result);
			},
			error: function (XMLHttpRequest, textStatus, errorThrown){//默认: 自动判断 (xml 或 html)) 请求失败时将调用此方法。这个方法有三个参数：XMLHttpRequest 对象，错误信息，（可能）捕获的错误对象。通常情况下textStatus和errorThown只有其中一个有值
				try{
					var result = jQuery.parseJSON(XMLHttpRequest.responseText);
					callback(result);
				}catch(e){
					alert("submit error!");
				}
			}
	});
}

//先获取token，再上传文件
//TODO 待完善，跨域问题
function qiniu_upload(fileid, img_path, callback){
	callback({"name": img_path});
	return;
	if(callback==undefined){
		callback=function(result){};
	}
	var path = "/qiniu/uptoken";
	ajax_get(path, {"key": img_path}, function(result){
		if(result.err==0){
			var token = result.uptoken;
			var data = {"token": token, "key": img_path};
			jQuery.ajaxFileUpload({
				type : "POST",
				url:"http://up.qiniu.com/",//用于文件上传的服务器端请求地址
				secureuri:false,//一般设置为false
				fileElementId:fileid,//文件上传空间的id属性  <input type="file" id="file" name="file" />
				dataType: 'json',//返回值类型 一般设置为json
				dataType: 'json',
				//async:false,
				contentType: "application/json",
				success: function (result, textStatus){//请求成功后回调函数。这个方法有两个参数：服务器返回数据，返回状态。data类型由dataType决定
					callback(result);
				},
				error: function (XMLHttpRequest, textStatus, errorThrown){//默认: 自动判断 (xml 或 html)) 请求失败时将调用此方法。这个方法有三个参数：XMLHttpRequest 对象，错误信息，（可能）捕获的错误对象。通常情况下textStatus和errorThown只有其中一个有值
					try{
						var result = jQuery.parseJSON(XMLHttpRequest.responseText);
						callback(result);
					}catch(e){
						alert("upload error!");
					}
				}
			});
		}else{
			alert("get token error!");
		}
	});
}

function ajax_get(path, data, callback){
	if(callback==undefined){
		callback=function(result){};
	}
	$.ajax({
			type: "GET",
			url: path,
			async:false,
			data: data ,
			dataType: 'json',//返回值类型 一般设置为json
			success: function(msg){
				callback(msg);
			}
	});
}

//jsonp解决跨域问题
function jsonp_get(path, data, callback){
	if(callback==undefined){
		callback=function(result){};
	}
	$.ajax({
			type: "GET",
			url: path,
			async:false,
			data: data ,
			dataType: 'jsonp',
			jsonp: "callback",
			success: function(msg){
				var jsonObj = eval(msg);
				callback(jsonObj);
			}
	});
}

//将表单数据转化为JSON格式
(function($){
	$.fn.serializeJson=function(){
		var serializeObj={};
		var array=this.serializeArray();
		var str=this.serialize();
		$(array).each(function(){
			if(serializeObj[this.name]){
				if($.isArray(serializeObj[this.name])){
					serializeObj[this.name].push(this.value);
				}else{
					serializeObj[this.name]=[serializeObj[this.name],this.value];
				}
			}else{
				serializeObj[this.name]=this.value;	
			}
		});
		return serializeObj;
	};
})(jQuery);

function add_to_page(cur_url, s){
	if(cur_url.indexOf("?") > -1){
		cur_url += "&" + s;
	}else{
		cur_url += "?" + s;
	}
	window.location.href = cur_url;
}

function pagination(){
	var _total = $("#_total").val();
	var _index = $("#_index").val();
	var _display = 15;
	if(_total < _display){
		_display = _total;
	}
	if(_total > 1){
		$("#pagination").paginate({
			count 		: _total,
			start 		: _index,
			display     : _display,
			border					: false,
			text_color  			: '#79B5E3',
			background_color    	: 'none',	
			text_hover_color  		: '#2573AF',
			background_hover_color	: 'none', 
			images		: false,
			mouse		: 'press',
			onChange     			: function(page){
										var url = window.location.href;
										url = url.replace(/[?|&]page=\d+&/g, "?");
										url = url.replace(/[?|&]page=\d+/g, "");
										add_to_page(url, "page=" + page);
									  }
		});
		
		$(".jPag-pages").width($(".jPag-pages").width() + 15);
	}
}
