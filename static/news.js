//this is a basic api call to produce the n/news webpage
function get_news(){
    fetch('n/newsquery')
    .then (response =>{
        window.location.href = "n/news"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


