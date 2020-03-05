/**
 * Created by Administrator on 2020/2/29.
 */

$(function(){

    $('.delete').click(function(){

        // 获取对应要删除的文章编号
        var articleid = $(this).attr('articleid')



        // 发送ajax请求，删除的文章
        $.ajax({
            url: '/blog/'+articleid+'/artical_delete/',
            type:'GET',
            success:function(response){
                alert('删除成功')
            },
            error:function(){
                console.log('请求失败')
            }
        })

    })
})





