document.addEventListener('DOMContentLoaded', ()=>{
    
    document.querySelectorAll('#edit-button').forEach(edit => {
        edit.onclick = function(){
            display_edit(edit.dataset.id);
        }
    })

    document.querySelectorAll('#like-button').forEach(like => {
        like.onclick = function(){
            like_post(like.dataset.id)
        }
    })

})

function display_edit(id){

    const elements = document.querySelectorAll('#edit-button')
    for(let i =0; i<elements.length; i++){
        elements[i].style.display = 'none'
    }
    
    const body = document.querySelector(`#post-body-${id}`).innerHTML

    document.querySelector(`#edit-space-${id}`).innerHTML = 
    `<form id="edit-form-${id}" onsubmit="return false">
    <div class="form-group">
        <textarea class="form-control" id="post-body-${id}">${body}</textarea>
    </div>
    <button type="submit" class="btn btn-primary btn-sm" >Save</button>
    </form>`
    document.querySelector(`#edit-form-${id}`).addEventListener('submit', ()=>editPost(id))
}


function editPost(id){

 
    let csrftoken = getCookie('csrftoken');
    
    const edited_body = document.querySelector(`#post-body-${id}`).value
    fetch('/edit',{
        method: 'POST',
        body: JSON.stringify({
            id: id,
            body: edited_body,
        }),
        headers: { "X-CSRFToken": csrftoken },
        

    })

    document.querySelector(`#edit-space-${id}`).innerHTML = edited_body

    const elements = document.querySelectorAll('#edit-button')
    for(let i =0; i<elements.length; i++){
        elements[i].style.display = 'block'
    }
}


function like_post(id){

    fetch('/like',{
        method:'POST',
        body: id
        
    })
    .then(response => response.json())
    .then(result =>{
        document.querySelector(`#like-count-${id}`).innerHTML = `Likes: ${result.like_count}`
    })
}

   // The following function are copying from 
    // https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }