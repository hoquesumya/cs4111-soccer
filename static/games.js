//this is a basic api call to get the g/games page
function get_games(){
    fetch('g/allgamesquery')
    .then (response =>{
        window.location.href = "g/games"
        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}


