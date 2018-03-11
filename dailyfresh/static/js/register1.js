$(function(){
    var error_name = true;
    var error_pwd = true;
    var error_cpwd = true;
    var error_email = true;
    var error_allow = false;

    //检查用户名
    function check_username(){
        var user_name = $('#user_name').val();
        var re = /^[a-zA-Z0-9_]{3,10}$/;
        if(user_name == ''){
            $('#user_name').next().html('用户名不能为空').show();
            return;
        }
        if(re.test(user_name) == true){

            error_name = false;
            $('#user_name').next().hide();
        }
        else{
            $('#user_name').next().html('用户名必须是3到10位的数字、字母、下划线').show();
        }
    }


     //检查密码
    function check_pwd(){
        var pwd = $('#pwd').val();
        var re = /^[a-zA-Z0-9_\.\$\*@!#]{6,16}$/;
        if(pwd == ''){
            $('#pwd').next().html('密码不能为空').show();
            return;
        }

        if(re.test(pwd) == true){
            error_pwd = false;
            $('#pwd').next().hide();
        }
        else{
            $('#pwd').next().html('密码必须是6到16位的数字、字母、下划线与.$*@!#').show();
        }
    }



    //确认密码
    function check_cpwd(){
        var pwd = $('#pwd').val();
        var cpwd = $('#cpwd').val();
        if(cpwd == ''){
            $('#cpwd').next().html('密码确认不能为空').show();
        }
        if(pwd == cpwd){
            error_cpwd = false;
        }
        else{
            $('#cpwd').next().html('两次密码不一样').show();
        }
    }


    //检查邮箱
    function check_email(){
        var email = $('#email').val();
        var re = /^[a-zA-Z0-9_]+@[\w]{2,3}\.(com|cn|org)$/;
        if(email == ''){
            $('#email').next().html('邮箱不能为空').show();
            return;
        }

        if(re.test(email) == true){
            error_email = false;
            $('#email').next().hide();
        }
        else{
            $('#email').next().html('必须是有效的邮箱').show();
        }
    }



    //用户名检查
    $('#user_name').blur(function(){
        check_username();
    });

    $('#user_name').focus(function(){
        $(this).next().hide();
    });


    //密码检查
    $('#pwd').blur(function(){
        check_pwd();
    });

    $('#pwd').focus(function(){
        $(this).next().hide();
    });


    //密码确认
    $('#cpwd').blur(function(){
        check_cpwd();
    });

    $('#cpwd').focus(function(){
        $(this).next().hide();
    });


    //邮箱检查
    $('#email').blur(function(){
        check_email();
    });

    $('#email').focus(function(){
        $(this).next().hide();
    });



    //协议检查
    $('#allow').click(function(){
        var state = $(this).prop('checked');
        if(state == true){
            error_allow = false;
            $('.error_tip2').hide();
        }
        else{
            error_allow = true;
            $('.error_tip2').html('请同意使用协议！').show();
        }
    });

    //提交注册信息
    $('.reg_form').submit(function(){
        check_username();
		check_pwd();
		check_cpwd();
		check_email();
        if(error_allow==false && error_pwd==false && error_name==false && error_cpwd==false && error_email==false)
        {
            return true;
        }
        else{
            return false;
        }
    });



});