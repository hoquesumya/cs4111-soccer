function get_playerstats(button) {
    var playerName = button.textContent.trim();
    console.log(playerName);
    fetch('/playerstats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(playerName)
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        // Handle the received data here, for example:
        console.log("Received data:", data);
        // Redirect to performancestats only after handling the data
        window.location.href = "/performancestats"
    })
    .catch(error => {
        console.log(error);
    });
}