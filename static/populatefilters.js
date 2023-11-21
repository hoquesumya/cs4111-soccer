document.addEventListener("DOMContentLoaded", function() {
    const currentUrl = window.location.pathname; // Gets the current URL path
    if (currentUrl === '/players') {
        //get references to attribute and value dropdowns
        const attributeDropdown = document.getElementById('attributeDropdown');
        const valueDropdown = document.getElementById('valueDropdown');

        //define values for each attribute
        const attributeValues = {
            //age: ['< 25', '>= 25'],
            //height: ['< 1.80 m', '>= 1.80 m'],
            //weight: ['< 100 Kg', '>= 100 Kg'],
            competition: ['La Liga', 'World Cup', 'English Premier League'],
            team: ['Barcelona', 'Real Madrid', 'Brazil', 'Argentina', 'Manchester City'],
            position: ['Forward', 'Defender', 'Midfielder', 'Goalkeeper']
        };

        //this function populates the valueDropdown based on the selected attribute
        function populateValues() {
            const selectedAttribute = attributeDropdown.value;
            valueDropdown.innerHTML = ''; // Clear previous options

            attributeValues[selectedAttribute].forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                valueDropdown.appendChild(option);
            });
        }

        //event listener for changes in the attributeDropdown
        attributeDropdown.addEventListener('change', populateValues);

        // Initial population of valueDropdown based on the default selected attribute
        populateValues();
    }
});

function filterPlayers() {
    const requestData = {
        arg1: attributeDropdown.value,
        arg2: valueDropdown.value
    };
    
    //const selectedAttribute = ;
    //const selectedValue = ;

    // Logic to filter players based on the selected attribute and value
    // This is where you will apply the filtering logic to display the relevant players
    // You might fetch data from the server based on the selected attribute and value
    // Or filter the existing list of players displayed on the page
    // Example: Fetch players based on selected attribute and value
    fetch('/filteringlogic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        //body: JSON.stringify(selectedAttribute, selectedValue)
        body: JSON.stringify(requestData)
    })
    //fetch(`/filteredPlayers?attribute=${selectedAttribute}&value=${selectedValue}`)
    .then(response => response.json())
    .then(data => {
        // Handle the response data and update the UI to display filtered players
        //console.log('Filtered players:', data);
        // Update the UI with filtered players
        window.location.href = "/filteredplayers"
    })
    .catch(error => {
        console.error('Error filtering players:', error);
    });
}