;
var user_login_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        $(".login_wrap .do-login").click(function(){
            var btn_target = $(this)
            if(btn_target.hasClass('disabled')){
                 common_ops.alert("正在处理!!请不要重复提交~~");
                 return;
            }
            var login_name = $('.login_wrap input[name="login_name"]').val();
            var login_pwd = $('.login_wrap input[name="login_pwd"]').val();
            if(login_name == undefined || login_name == ""){
                common_ops.alert("请输入正确的登录用户名~~" );
                return
            }
            if(login_pwd == undefined || login_pwd == ""){
                common_ops.alert("请输入正确的密码~~" );
                return
            }
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl('/user/login'),
                type:"POST",
                data:{
                    'login_name':login_name,
                    'login_pwd':login_pwd
                },
                dataType:'json',
                success:function(res){
                    if(res.code == 200){
                        window.location.href = common_ops.buildUrl('/')
                    }
                }
            })
        })
    }

}

$(function(event){
    user_login_ops.init();
});