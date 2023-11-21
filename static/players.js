//this is a basic api call to produce the p/players webpage
function get_players(){
    fetch('p/allplayersquery')
    .then (response =>{
        window.location.href = "p/players"
        //console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


