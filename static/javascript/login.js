$(function(){
	
	$('#switch_qlogin').click(function(){
		$('#switch_login').removeClass("switch_btn_focus").addClass('switch_btn');
		$('#switch_qlogin').removeClass("switch_btn").addClass('switch_btn_focus');
		$('#switch_bottom').animate({left:'0px',width:'70px'});
		$('#qlogin').css('display','none');
		$('#web_qr_login').css('display','block');
		
		});
	$('#switch_login').click(function(){
		
		$('#switch_login').removeClass("switch_btn").addClass('switch_btn_focus');
		$('#switch_qlogin').removeClass("switch_btn_focus").addClass('switch_btn');
		$('#switch_bottom').animate({left:'154px',width:'70px'});
		
		$('#qlogin').css('display','block');
		$('#web_qr_login').css('display','none');
		});
if(getParam("a")=='0')
{
	$('#switch_login').trigger('click');
}

	});
	
function logintab(){
	scrollTo(0);
	$('#switch_qlogin').removeClass("switch_btn_focus").addClass('switch_btn');
	$('#switch_login').removeClass("switch_btn").addClass('switch_btn_focus');
	$('#switch_bottom').animate({left:'154px',width:'96px'});
	$('#qlogin').css('display','none');
	$('#web_qr_login').css('display','block');
	
}


//根据参数名获得该参数 pname等于想要的参数名 
function getParam(pname) { 
    var params = location.search.substr(1); // 获取参数 平且去掉？ 
    var ArrParam = params.split('&'); 
    if (ArrParam.length == 1) { 
        //只有一个参数的情况 
        return params.split('=')[1]; 
    } 
    else { 
         //多个参数参数的情况 
        for (var i = 0; i < ArrParam.length; i++) { 
            if (ArrParam[i].split('=')[0] == pname) { 
                return ArrParam[i].split('=')[1]; 
            } 
        } 
    } 
}  


var reMethod = "GET",
	pwdmin = 6;

$(document).ready(function() {

        
        
          
        


           
        $("#license").change(function(){
        var filepath=$("#license").val();
        if (filepath =="")
        {
            $('#userCue').html("<font color='red'><b>请选择营业执照图片</b></font>");
            return false;
        }
        var extstart=filepath.lastIndexOf(".");
        var ext = filepath.substring(extstart, filepath.length).toUpperCase();
        if (ext != ".BMP" && ext !=".PNG" && ext!=".GIF" && ext!=".JPG" && ext !=".JPEG" || ext=="")
          {
             $('#userCue').html("<font color='red'><b>图片格式限于bmp/png/gif/jpg/jgeg</b></font>");
             $("#license").val("");
             return false;
          }
          var file_size = 0;
          if ($.browser.msie) {
                    var img = new Image();
                    img.src = filepath;
                    while (true) {
                        if (img.fileSize > 0) {
                            if (img.fileSize > 2 * 1024 * 1024) {
                                //alert("图片不大于2MB。");
                                $(this).val("")
                                $("#userCue").html("<font color='red'><b>图片格式限于bmp/png/gif/jpg/jgeg</b></font>");
                                $("#license").val("");
                                return false;
                            } else {
                                //var num03 = img.fileSize / 1024;
                                //num04 = num03.toFixed(2)
                                //$("#fileSize").text(num04 + "KB");
                            }
                            break;
                        }
                    }
                } else {
                    file_size = this.files[0].size;
                    var size = file_size / 1024;
                    if (size > 2048) {
                        //alert("上传的图片大小不能超过2M！");
                        $('#userCue').html("<font color='red'><b>图片大小不得大于2M</b></font>");
                        $(this).val("")
                    } else {
                        var num01 = file_size / 1024;
                        num02 = num01.toFixed(2);
                        //$("#fileSize").text(num02 + " KB");
                    }
                }
                return true;
                })

        var email_state=false;
        $("#email").focus(function(){
        if (email_state==false){
        $("#email").val("");
        
        $('#userCue').html("<font color='red'><b>请填写公网邮箱</b></font>");
        }
        })



        $("#email").keyup(function(){
            //if($(this).val()==''){
              //          $('#userCue').html("<font color='red'><b>邮箱不能为空</b></font>");
                //        $("#email").focus();
                        
            //}
            //else{
              if (/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test($(this).val()) == false) {
                        $('#userCue').html("<font color='red'><b>邮箱格式不正确</b></font>");
                        //$("#email").focus();
                        //$(this).val("");
                        //return false;
               }

               else {
                        //$('#email_info').text('');
                        //$('#email_info').append('<img src=/static/images/onSuccess.gif/>');
                        email_state = true;
                        $('#userCue').html("<font color='black'><b>邮箱格式正确</b></font>");
                        return true;
                    }


            //}
         })

        var phone_state=false;
        $("#phone").focus(function(){
        if (phone_state==false){
        $("#phone").val("");
        $('#userCue').html("<font color='red'><b>请输入11位手机号码或者区号+电话号码</b></font>");
        }
        })



        $("#phone").keyup(function(){
            //if($(this).val()==''){
              //          $('#userCue').html("<font color='red'><b>请输入电话号码</b></font>");
                //        $("#phone").focus();
            //}
            //else{
              if (/^(1[3578][0-9]{9})$/.test($(this).val()) == false) {
                        $('#userCue').html("<font color='red'><b>格式不对，请输入正确手机号码</b></font>");
                        //$("#phone").focus();
               }

               else {
                        //$('#phone_info').text('');
                        //$('#phone_info').append('<img src=/static/images/onSuccess.gif/>');
                        $('#userCue').html("<font color='black'><b>格式正确</b></font>");
                        phone_state = true;
                        return true;
                    }


            //}
         })

        var passwd_state=false;
        $("#passwd").focus(function(){
            
             if(passwd_state==false){
                  $("#passwd").val('');
                  $('#userCue').html("<font color='red'><b>请输入6-18位的密码</b></font>");
              }
        })        

        $("#passwd").keyup(function(){
             //if($(this).val()==''){
                  //$("#passwd").focus();
               //   $('#userCue').html("<font color='red'><b>密码不能为空</b></font>");
             //}
             //else 
             //{             
                if ($(this).val().length<6 || $(this).val().length>18)
               {
                    //$('#passwd').focus();
		    $('#userCue').html("<font color='red'><b>密码为6-18位的字符</b></font>");
               }
               else{
                  $('#userCue').html("<font color='black'><b>格式正确</b></font>");
                passwd_state=true; 
                }
             //}
        })

       var passwd2_state=false;
       $("#passwd2").focus(function(){
             if(passwd2_state==false)
               $("#passwd2").val('');
                  $('#userCue').html("<font color='red'><b>请重复输入密码</b></font>");


       })
       
       $("#passwd2").keyup(function(){
             //if($("#passwd2").val()=="")
             //{
               //$(this).val("");
               //$("#userCue").html("<font color='red'><b>重复密码不能为空</b></font>");
               //$("#passwd2").focus();  
             //}
             //else{
                 if($("#passwd2").val()!=$("#passwd").val())
                 {
                    //$('#passwd2').focus();
		    $('#userCue').html("<font color='red'><b>两次密码不一致</b></font>");
                 }
                 else
                 {
		    $('#userCue').html("<font color='black'><b>两次密码一致</b></font>");
                     passwd2_state=true;
                 }
            // } 
            
       })
 
       

        var user_state=false;
        $("#user").focus(function(){
            
             if(user_state==false){
                  $("#user").val("");
                  $('#userCue').html("<font color='red'><b>请输入6-10位的字符</b></font>");
              }
        })        

        $("#user").keyup(function(){
             //if($("#user").val()==''){
                  //$('#userCue').html("<font color='red'><b>用户名不能为空</b></font>");
             //}
             //else 
             //{             
                if ($("#user").val().length<6 || $("#user").val().length>10)
               {
                    
		    $('#userCue').html("<font color='red'><b>用户名为6-10位的字符</b></font>");
               }
               else{
                $('#userCue').html("<font color='black'><b>格式正确</b></font>");
                user_state=true; 
                }
             //}
        })

        var company_state=false;
        $("#company").focus(function(){
            
             if(company_state==false){
                  $("#company").val("");
                  $('#userCue').html("<font color='red'><b>请输入店铺名</b></font>");
              }
        })        

        $("#company").keyup(function(){
             //if($("#company").val()==''){
                  //$("#company").focus();
                  //$("#userCue").html("<font color='red'><b>公司名不能为空</b></font>");
             //}
             //else 
             //{             
                if ($("#company").val().length<2)
               {
                    //$('#company').focus();
		    $('#userCue').html("<font color='red'><b>店铺名太短</b></font>");
               }
               else{
                   $('#userCue').html("<font color='black'><b>店铺名正确</b></font>");
                company_state=true; 
                }
             //}
        })







        



















	$('#reg').click(function() {

		if ($('#user').val() == "") {
			$('#user').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×用户名不能为空</b></font>");
			return false;
		}



		if ($('#user').val().length < 4 || $('#user').val().length > 16) {

			$('#user').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×用户名位4-16字符</b></font>");
			return false;

		}
		


		if ($('#passwd').val().length < pwdmin) {
			$('#passwd').focus();
			$('#userCue').html("<font color='red'><b>×密码不能小于" + pwdmin + "位</b></font>");
			return false;
		}
		if ($('#passwd2').val() != $('#passwd').val()) {
			$('#passwd2').focus();
			$('#userCue').html("<font color='red'><b>×两次密码不一致！</b></font>");
			return false;
		}
                
                if ($('#phone').val() == "") {
			$('#phone').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×电话不能为空</b></font>");
			return false;
		}
                
                if ($('#email').val() == "") {
			$('#email').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×邮箱不能为空</b></font>");
			return false;
		}
                  
                if ($('#company').val() == "") {
			$('#company').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×公司名不能为空</b></font>");
			return false;
		}
		
                if ($('#license').val() == "") {
			$('#license').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×营业执照不能为空</b></font>");
			return false;
		}
		$('#regUser').submit();
	});
	

});
