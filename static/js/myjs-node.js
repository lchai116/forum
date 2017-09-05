var bindAction = function(){

    $('#id-topic-submit').on('click', function(event){
        var title = $('#id-input-title').val()
        var content = $('#id-topic-content').val()
        if(title.length < 4 || content.length < 4){
            event.preventDefault()
            swal('Title or content must be longer than 4 characters')
        }
    })
}

var _main = function(){
    bindAction()
}


$(document).ready(function(){
    _main()
})