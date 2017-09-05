
var signinHandle = function(resp){
    if(resp.success){
        var url = resp.redirect_url
        window.location = url
    }else{
        swal('Incorrect username or password. Signin fail!')
    }
}

var bindAction = function(){

    $('#id-btn-signin').on('click', function(event){
        var username = $('#id-input-username').val()
        var password = $('#id-input-password').val()
        var form = {
            username: username,
            password: password,
        }
        if(username=="" || password==""){
            event.preventDefault()
            swal('Username or password can\'t be empty')
        }else{
            event.preventDefault()
            api.post('/signin', form, signinHandle)
        }
    })

    $('.comment-reply-btn').on('click', function(){
        var self = $(this)
        if(self.text()=='Reply'){
            self.text('Cancel')
        }
        else{
            self.text('Reply')
        }
        self.closest('.comment').find('.comment-reply-form').slideToggle()
    })
}

var _main = function(){
    bindAction()
}


$(document).ready(function(){
    _main()
})