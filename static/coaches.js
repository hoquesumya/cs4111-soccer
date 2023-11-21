function get_coaches(){
    fetch('/coachesquery')
    .then (response =>{
        window.location.href = "/coaches"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


