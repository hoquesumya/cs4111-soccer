
function get_news(){
    fetch('/newsquery')
    .then (response =>{
        window.location.href = "/news"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


