// Data Loading
const items_data = ['A', 'B', 'C', 'D'] 
// TODO: create http response from Djnago to mimic data sent

const parsedJson = $.getJSON('http://127.0.0.1:8000/json', (json_response) => {
    // const parsedJson = JSON.parse(json_response)  // const because it is a data packet from the server and should not be changed
    // TODO: make sure JSON response is from correct source
});

// functionality
function populateItemList(items_data) {
  // Takes the relevant array derived from user selections and popuplates the RHS menu
  // input - array of items
  // output - none

  if (items_data.length == 0) {
    // No items
    menuList.innerHTML = "אין פריטים להצגה";
  } else {
    for (i = 0; i < items_data.length; i++) {
      let item = document.createElement("button");
      item.setAttribute("class", "list-group-item");
      item.setAttribute("type", "button");
      item.innerHTML = items_data[i];
      menuList.appendChild(item);
    }
  }
};



// event listeners
document.addEventListener('DOMContentLoaded', () => {

    // Navbar buttons
    document.getElementById('tail_number').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "מספרי זנב";
        let menuList = document.getElementById("item_list");
    });

    document.getElementById('envelopes').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "מעטפות";
    });

    document.getElementById('items').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "פריטי משימה";
    });

    document.getElementById('fuelflow').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "מהלכי דלק";
    });

    document.getElementById('presets').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "פריסטים";
    });

    // Footer buttons

    
});