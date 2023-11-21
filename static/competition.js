
var hidden = true

//this is a basic api call to produce the competitions webpage
function get_competition(){
    fetch('/en/competition')
    .then (response =>{
        window.location.href="/en/comp"

        console.log("data are:")  
    })
    
    .catch(error =>{
        console.log(error)
    })

}

function  handleCompetition(names){
    console.log("names are:")
    console.log(names)
    var ul = document.getElementById("comp_name")
    console.log(ul)
    for (var i = 0; i < names.name.length; i++) {
        var name = names.name[i];
        list_creation(name,names.date[i],ul,i)
    
    }
}
/* create list elements*/
function list_creation(name,all_date,ul,i){
    var li = document.createElement('li');
        li.setAttribute("id","per_list")
        
        var button = document.createElement('button')
        button.setAttribute('class', 'btn border border-white p-6 comp_divider')
        button.setAttribute('onclick',`handlesimple(${i})`)

        var div = document.createElement("div")
        var div1 = document.createElement("div")
        div1.setAttribute("id", i)
        div1.setAttribute("class", "dropdown")
        
        div1.style.display="none"
        div.setAttribute("id", "list_comp")

       
        var sub_ul = document.createElement("ul")
        sub_ul.setAttribute("id","all_list")
        var sub_l1=document.createElement("li")
        var sub_l2=document.createElement("li")
        var sub_l3=document.createElement("li")

        sub_l1.appendChild(document.createTextNode(name))
        sub_l2.appendChild(document.createTextNode(all_date[0]))
        sub_l3.appendChild(document.createTextNode(all_date[1]))
        sub_ul.appendChild(sub_l1)
        sub_ul.appendChild(sub_l2)
        sub_ul.appendChild(sub_l3)

        div.appendChild(sub_ul)


        //li.appendChild(document.createTextNode(name));
        button.append(div)
       
        handleToogle(div1, name, all_date[0],all_date[1])

        button.append(div1)


        li.appendChild(button)

        ul.appendChild(li);

}

function handlesimple(n){
    var div = document.getElementById(n);
    hidden = !hidden; 
    div.style.display="block"
   /* if (hidden) {
        div.style.display = "none";
    } else {
        div.style.display = "block";
    }
    console.log(hidden)*/
    

}
function handleToogle(div1,name,start_date,end_date){
    var choice = ['Teams','Players']
    var button = document.createElement("button")
    button.setAttribute("class", "btn btn-secondary dropdown-toggle");
    button.setAttribute("type","button") ;
    button.setAttribute("id","dropdownMenuButton1");
    button.setAttribute("data-bs-toggle","dropdown");
    button.setAttribute("aria-expanded","false");
    button.textContent="Dropdown";

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
        b1.setAttribute("onclick",`handleSql(${i}, '${name}', '${start_date}','${end_date}')`)
        
        //append to list
        li1.appendChild(b1)
        ul.appendChild(li1)
    }
    div1.appendChild(button);
    div1.appendChild(ul)

}
function handleSql(type,name,start_date,end_date){
    console.log(name,start_date,end_date)
    if (type == 0)
        console.log("find query for teams")
    
    fetch('/en/competition-sql-query',{
        method:"POST",
        body:JSON.stringify({
            "type":type,
            "comp-name":name,
            "start-date":start_date,
            "end-date":end_date
        }),

        headers:{
            "Content-type": "application/json; charset=UTF-8"
        }

    })
    .then (response =>{
       return response.json() 
    })
    .then(json => {
        
       var rcv_date;
       if (type==0 || type==1)
            rcv_date =json[0].query_result
        else{
                console.log(json.game_id)
        }
        
        
        var d = document.getElementById("sql-query")
        d.style.display="block"
        
        if (type==0 || type==1){
            var ul = document.getElementById("start-q-list")
            if (ul){
                d.removeChild(ul)
            }
            ul = document.createElement("ul")
            ul.setAttribute("id","start-q-list")
            var table = document.getElementById("sql-t")
            if (table && table.parentNode===d){
                d.removeChild(table)
            }
            
            console.log(rcv_date.length)
            
            for (var i =0;i<rcv_date.length;i++){
                var li = document.createElement("li")
                li.textContent = rcv_date[i]
                ul.append(li)   
            }
           
            d.appendChild(ul)
        }
        //else game table 
       /* else{
            var table = document.getElementById("sql-t")
            if (table){
                d.removeChild(table)
            }
            table = document.createElement("table")
            table.setAttribute("id","sql-t")
            var head_list = ["Game_id  ","Game_location  ","Game_date  "]
            
            //var thead=table.createTHead();
            var thead = document.createElement("thead")
            //var row = thead.insertRow();
            var row = document.createElement("tr")

            ul = document.getElementById("start-q-list")
            if (ul && ul.parentNode===d){
                d.removeChild(ul)
            }
            console.log(row)
            for (var i =0;i<head_list.length;i++){
                var th1= document.createElement("th")
                th1.setAttribute("scope","col")
                th1.innerHTML=head_list[i]
                row.appendChild(th1)

            }
           
           thead.appendChild(row)
           table.appendChild(thead)
           fill_table(table,json)
           d.appendChild(table)
           
        }*/
    })
    .catch(error =>{
        console.log(error)
    })
}

/*function fill_table(d,json){


    var tbody = document.createElement("tbody")

    var id = json.game_id
    var date=json.game_date
    var location=json.game_location
    for (var i=0;i <id.length;i++){
        var row = document.createElement("tr")
        
        var td1= document.createElement("td")
        td1.innerText=id[i]
        row.appendChild(td1)

        var td2 = document.createElement("td")
        td2.innerText=location[i]
        row.appendChild(td2)

        var td3 = document.createElement("td")
        td3.innerText=date[i]
        row.appendChild(td3)

        tbody.appendChild(row)

    }

    d.appendChild(tbody)


}*/
function handleSqlDiv(){
    var div = document.getElementById("sql-query")
    div.style.display="none"
}



