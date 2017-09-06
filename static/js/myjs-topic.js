


var bindEventCommentSubmit = function(){
    $('#id-comment-submit').on('click', function(event){
        var content = $('#id-comment-content').val()
        if(content.length < 4){
            event.preventDefault()
            swal('Your reply must be longer than 4 characters')
        }
    })
}


var bindEventCommentReply = function(){
    $('.comment-reply-submit').on('click', function(event){
        var self = $(this)
        var content = self.parent().find('textarea').val()
        if(content.length < 4){
            event.preventDefault()
            swal('Your reply must be longer than 4 characters')
        }
    })
}

var bindEventReplyBtnToggle =function(){
    $('.comment-reply-btn').on('click', function(){
        var self = $(this)
        log('reply btn')
        if(self.text()=='Reply'){
            self.text('Cancel')
        }
        else{
            self.text('Reply')
        }
        self.closest('.li-comment').find('.comment-reply-form').slideToggle()
    })
}

var bindEventCommentLike = function(){
    $('.comment-like-icon').on('click', function(event){
        event.preventDefault()
        var self = $(this)
        var comment_id = self.closest('.li-comment').data('id')
        var response = function(resp){
            if(resp.success){
                var delta = resp.data.delta
                var tag_like_icon = self.closest('.comment-btn-like').find('.comment-like-icon')
                var tag_like_num = self.closest('.comment-btn-like').find('.comment-like-num')
                if(tag_like_icon.hasClass('like-icon-unhit')){
                    tag_like_icon.removeClass('like-icon-unhit')
                }else{
                    tag_like_icon.addClass('like-icon-unhit')
                }
                var updated_like_num = parseInt(tag_like_num.text()) + delta
                tag_like_num.text(String(updated_like_num))
            }
        }
        api.post('/api/comment/like', {comment_id: comment_id}, response)
    })
}

var bindEventTopicFavor = function(){
    $('.topic-favor-btn').on('click', function(event){
        var self = $(this)
        var topic_id = self.closest('.topic-info').data('id')
                log('outout')
        var response = function(resp){
            if(resp.success){
                if(r.data.delta){
                    log('jifjeoluch')
                    self.val('Remove from favorite')
                }else{
                    self.val('Add as favorite')
                }
            }
        }
        api.post('/api/topic/favor', {topic_id: topic_id}, response)
    })
}


var _main = function(){
    bindEventTopicFavor()
    bindEventCommentReply()
    bindEventCommentLike()
    bindEventReplyBtnToggle()
    bindEventCommentSubmit()
}


$(document).ready(function(){
    _main()
})