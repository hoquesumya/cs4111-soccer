function get_playerstats(button) {
    //gets player name as text from player button
    var playerName = button.textContent.trim();
    console.log(playerName);
    //perform api call with relevant input
    fetch('p/playerstats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(playerName)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received data:", data);
        //redirect to new performancestats webpage
        window.location.href = "p/performancestats"
    })
    .catch(error => {
        console.log(error);
    });
}