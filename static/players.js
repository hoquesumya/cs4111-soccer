
function get_players(){
    fetch('/allplayersquery')
    .then (response =>{
        window.location.href = "/players"
        //console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


