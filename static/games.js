
function get_games(){
    fetch('/allgamesquery')
    .then (response =>{
        window.location.replace("/games")
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


