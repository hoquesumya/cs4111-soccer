

function get_competition(){
    fetch('/competition')
    .then (response =>{
        console.log("data are:")
        return response.json()    
    })
    .then(data=>{
        console.log(data)
        var ul = document.getElementById("comp_name")
        
        

        //window.location.replace(" http://127.0.0.1:8111/competition")
    })
    .catch(error =>{
        console.log(error)
    })
}


