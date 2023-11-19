
function get_games(){
    fetch('/allgamesquery')
    .then (response =>{
        window.location.href = "/games"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


