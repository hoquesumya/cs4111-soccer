var hidden = true
function get_teams(){
    fetch('/tm/team-info')
    .then (response =>{
       window.location.replace("/tm/teams")
       
    })

    .catch(error =>{
        console.log(error)
    })
}


function  handleTeams(teams_info){
    console.log("names are:")
    console.log(teams_info)
    var ul = document.getElementById("team_name")
    console.log(ul)
    for (var i = 0; i < teams_info.id.length; i++) {
        var team_name = teams_info.team_name[i];
        var team_id = teams_info.id[i]
        var total_players = teams_info.total_players[i]
        var total_coaches = teams_info.total_coaches[i]

        list_creation_Team(team_name,total_players,total_coaches,ul,i, team_id)
    
    }
}
function list_creation_Team(team_name,total_players,total_coaches,ul,i, team_id){
    var li = document.createElement('li');
    li.setAttribute("id","per_list_team");


    var button = document.createElement('button')
    button.setAttribute('class', 'btn border border-white p-6 comp_divider')
    button.setAttribute('onclick',`handlesimpleTeam(${i})`)

    var div = document.createElement("div")
    var div1 = document.createElement("div")
    div1.setAttribute("id", `drop${i}`)
    div1.setAttribute("class", "dropdown team_drop")
        
    div1.style.display="none"
    div.setAttribute("id", "list_comp_team")

       
    var sub_ul = document.createElement("ul")
    sub_ul.setAttribute("id","all_list_team")
    var sub_l1=document.createElement("li")
    var sub_l2=document.createElement("li")
    var sub_l3=document.createElement("li")

    sub_l1.appendChild(document.createTextNode(team_name))
    sub_l2.appendChild(document.createTextNode(total_coaches))
    sub_l3.appendChild(document.createTextNode(total_players))
    sub_ul.appendChild(sub_l1)
    sub_ul.appendChild(sub_l2)
    sub_ul.appendChild(sub_l3)

    div.appendChild(sub_ul)


        //li.appendChild(document.createTextNode(name));
    button.append(div)
       
    handleToogleTeam(div1, team_id)

    button.append(div1)
    li.appendChild(button)

    ul.appendChild(li);

}

function handlesimpleTeam(n){
    var div = document.getElementById(`drop${n}`);
    hidden = !hidden; 
    div.style.display="block"
}

function handleToogleTeam(div1,team_id){
    var choice = [ 'Coaches']
    var button = document.createElement("button")
    button.setAttribute("class", "btn btn-secondary dropdown-toggle");
    button.setAttribute("type","button") ;
    button.setAttribute("id","dropdownMenuButton1");
    button.setAttribute("data-bs-toggle","dropdown");
    button.setAttribute("aria-expanded","false");
    button.textContent="Team_Related_Info";

    //setting <ul>node
    var ul = document.createElement("ul");
    ul.setAttribute("class", "dropdown-menu");
    ul.setAttribute("aria-labelledby","dropdownMenuButton1");
    //setting all <li>
    for (var i=0;i <choice.length; i++){
        var li1 = document.createElement("li");
        li1.setAttribute("id",choice[i]);
       //create button for each list
        var b1= document.createElement("button");
        b1.setAttribute("class","btn border border-white p-2 b-competition");
        b1.style.borderRadius = "20px";
        b1.textContent=choice[i]
        b1.setAttribute("onclick",`handleSqlTeam(${i}, ${team_id})`)
        
        //append to list
        li1.appendChild(b1)
        ul.appendChild(li1)
    }
    div1.appendChild(button);
    div1.appendChild(ul)

}
function handleSqlTeam(index,team_id){
    
    fetch('/tm/team-sql-query',{
        method:"POST",
        body:JSON.stringify({
            "team_id":team_id
        }),

        headers:{
            "Content-type": "application/json; charset=UTF-8"
        }

    })
    .then (response =>{
        return response.json() 
     })
     .then(json=>{
        console.log(json.res)

        var d = document.getElementById("sql-query-team")
        d.style.display="block"
        var ul = document.getElementById("sql-l")
        if (ul){
            d.removeChild(ul)
        }
        ul = document.createElement("ul")
        ul.setAttribute("id","sql-l")
        for (var i=0;i<json.res.length;i++){
            var li = document.createElement("li")
            li.innerText=json.res[i]
            ul.append(li)
        }
        d.appendChild(ul)

     })

}

function handleSqlDivTeams(){
    var div = document.getElementById("sql-query-team")
    div.style.display="none"
}



   
