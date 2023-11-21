//outer event listener ensures that the script runs after the webpage was loaded
document.addEventListener("DOMContentLoaded", function() {
    //only executed when we are currently in the 'players' webpage
    const currentUrl = window.location.pathname; 
    if (currentUrl === '/p/players') {
        //get references to attribute and value dropdowns
        const attributeDropdown = document.getElementById('attributeDropdown');
        const valueDropdown = document.getElementById('valueDropdown');

        //define values for each attribute
        const attributeValues = {
            competition: ['La Liga', 'World Cup', 'English Premier League'],
            team: ['Barcelona', 'Real Madrid', 'Brazil', 'Argentina', 'Manchester City'],
            position: ['Forward', 'Defender', 'Midfielder', 'Goalkeeper']
        };

        //this function populates the valueDropdown based on the selected attribute
        function populateValues() {
            const selectedAttribute = attributeDropdown.value;
            valueDropdown.innerHTML = '';

            attributeValues[selectedAttribute].forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                valueDropdown.appendChild(option);
            });
        }

        //event listener for changes in the attributeDropdown
        attributeDropdown.addEventListener('change', populateValues);

        //initial population of valueDropdown based on the default selected attribute
        populateValues();
    }
});

function filterPlayers() {
    //sets up input to send to python server
    const requestData = {
        arg1: attributeDropdown.value,
        arg2: valueDropdown.value
    };
    
    //filtering logic is handled in python based on user input of filter attribute and attribute value
    //perform api call
    fetch('p/filteringlogic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Update the UI with filtered players
        window.location.href = "p/filteredplayers"
    })
    .catch(error => {
        console.error('Error filtering players:', error);
    });
}