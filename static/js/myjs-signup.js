
var signupHandle = function(resp){
    if(resp.success){
        var url = resp.redirect_url
        window.location = url
    }else{
        swal('Username exists. Signup fail!')
    }
}

var bindAction = function(){
    var formatCheck = function(form){
        var ul = form.username.length
        var pl = form.password.length
        if(ul < 3 || ul > 8){
            swal('Username must be 3-8 characters')
            return false
        }

        if(pl < 3 || pl > 8){
            swal('Password must be 3-8 characters')
            return false
        }
        return true
    }

    $('#id-btn-signup').on('click', function(event){
        event.preventDefault()
        var username = $('#id-input-username').val()
        var password = $('#id-input-password').val()
        var form = {
            username: username,
            password: password,
        }
        if(formatCheck(form)){
            log('up api')
            api.post('/signup', form, signupHandle)
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