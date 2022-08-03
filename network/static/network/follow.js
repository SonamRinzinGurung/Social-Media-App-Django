document.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('#follow-button').forEach(follow=>{
        follow.onclick = ()=>{
            follow_toggle(follow.dataset.id)
        }
    })
})


function follow_toggle(id){
    fetch('/follow',{
        method:'POST',
        body:id
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector('#followers').innerHTML = result.total_followers

        if(result.is_follower === true){
            document.querySelector('#follow-button').innerHTML = 'UnFollow'
        }else{
            document.querySelector('#follow-button').innerHTML = 'Follow'
        }
    })
}