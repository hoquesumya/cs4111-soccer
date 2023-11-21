//this is a basic api call to produce the c/coaches webpage
function get_coaches(){
    fetch('c/coachesquery')
    .then (response =>{
        window.location.href = "c/coaches"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


