//this is a basic api call to produce the competitions webpage
function get_competition(){
    fetch('/competition')
    .then (response =>{
        window.location.href = "/comp"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


