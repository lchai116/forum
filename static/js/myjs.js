var log = function(){
    console.log(arguments)
}
var api = {}
api.ajax = function(url, method, form, callback){
    request = {
        url: url,
        type: method,
        data: form,
        success: function(response){
            log('success')
            r = JSON.parse(response)
            callback(r)
        },
        error: function(err){
            r = {
                success: false,
                message: 'error',
            }
            callback(r)
        },
    }
    $.ajax(request)
}

api.post = function(url, form, response){
    api.ajax(url, 'post', form, response)
}

var getTime = function(){
    var time_s = arguments[0] || 0
    var t, y, mon, d, h, min, s
    t = time_s? new Date(time_s * 1000): Date()
    y = t.getFullYear()
    mon = t.getMonth() + 1
    d = t.getDate()
    h = t.getHours()
    min = t.getMinutes()
    s = t.getSeconds()
    return y + '-' + mon + '-' + d + ' ' + (h<10?'0'+h:h) + ':' + (min<10?'0'+min:min) + ':' + s
}

var time_tags = $('time')

log(time_tags)

for(var i = 0; i < time_tags.length; i++){
    var ts = $(time_tags[i])
    var fmt_t = getTime(ts.text())
    ts.text(fmt_t)
}


