
function get_players(){
    fetch('/allplayersquery')
    .then (response =>{
        window.location.replace("/players")
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


