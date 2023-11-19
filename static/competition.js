
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


