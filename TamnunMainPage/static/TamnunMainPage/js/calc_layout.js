/* Data Loading */
const items_data = ['A', 'B', 'C', 'D'] 

const dataReceived = $.getJSON('http://127.0.0.1:8000/json', (json_response) => {
    // Asyncronous request - front-end always listening for incoming data
    // const parsedJson = JSON.parse(json_response)  // const because it is a data packet from the server and should not be changed
    // TODO: make sure JSON response is from correct source in production
});

/* functionality */
function populateItemList(items_data) {
  /* Takes the relevant array derived from user selections and popuplates the RHS menu
  input - dictionary of items
  output - none */

  const menuList = document.getElementById("item_list");
  menuList.innerHTML = null; // clear existing data

  if (jQuery.isEmptyObject(items_data)) {
    // No items
    menuList.innerHTML = "אין פריטים להצגה";
  } else {
    for (var key in items_data) {
      let item = document.createElement("button");
      item.setAttribute("class", "list-group-item");
      item.setAttribute("type", "button");
      item.innerHTML = key; // display the name of the item and not the content(the data itself)
      menuList.appendChild(item);
    }
  }
    return;
};

function deriveWeightAndBalanceData(serverData, desiredData){
    /*
    Takes the JSON packet from the server and extracts the Weight and Balance data relevant to the specific request
    INPUT
    serverData - json packet from server
    desiredData - ???
    */
};

function createJsonResponse(configs, tailNums) {
    /**
     * Takes the sum of user selections and creates a JSON object to pass to the back end.
     * INPUT
     * configs - the data regarding the items chosen and derivatives (id + position)
     * tailNums - data regarding the chosen tail numbers chosen by the user
     * OUTPUT
     * dataPacket - JSON object containing the imputs in the agreed upon data stracture (definition of the front - back API)
     * 
     */

     return dataPacket;
}

function populateLimitaions(fuelLimitaions, chartData) {
  /**
   * takes the calculation output from the server and displays it in the left side menu
   * INPUT
   * fuelLimitaions - fuel for takeoff and landing
   * chartData - data to populate the weight-CG chart
   * OUTPUT
   * none
   *  */  
};

/* event listeners */
document.addEventListener('DOMContentLoaded', () => {

    // Navbar buttons
    document.getElementById('tail_number').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "מספרי זנב";

        try {
            populateItemList(dataReceived.responseJSON['tailNumbers'][0]);   
               
        } catch (error) {
            console.error(error);
            populateItemList({});
        }

    });

    document.getElementById('envelopes').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHclsTML = "מעטפות";
    });

    document.getElementById('items').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "פריטי משימה";
        try {
            populateItemList(dataReceived.responseJSON['items'][0]);   
               
        } catch (error) {
            console.error(error);
            populateItemList({});
        }
    });

    document.getElementById('fuelflow').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "מהלכי דלק";
    });

    document.getElementById('presets').addEventListener('click', () => {
        document.getElementById("menu_headline").innerHTML = "פריסטים";
    });

    // Footer buttons

    document.getElementById('generatePDF').addEventListener('click', () => {
    });

    // Calculate button 

    document.getElementById('calculate').addEventListener('click', () => {
    });
});