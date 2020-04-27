/* Data Loading */
const aircraftType = JSON.parse(
  document.getElementById("aircraftType").textContent
);
const aircrafts = JSON.parse(document.getElementById("aircrafts").textContent);
const ACitems = JSON.parse(document.getElementById("JsonACitems").textContent);
jsonz = { A: "a", B: "b" };
/* Asyncronous events  */

/* functionality */

function populateRightMenu(data, displayData, dataName) {
  const menuList = document.getElementById("item_list");
  menuList.innerHTML = null; // clear existing data

  if (data === []) {
    menuList.innerHTML = '<li class="list-item">אין פריטים להצגה</li>';
    return;
  }

  for (let el of data) {
    const template = `<button type="button" data-id = ${el["id"]} 
    class="list-group-item list-group-item-action ${dataName}">${el[displayData]}</button>`;
    menuList.innerHTML += template;
  }
}

function deriveWeightAndBalanceData(serverData, desiredData) {
  /*
    Takes the JSON packet from the server and extracts the Weight and Balance data relevant to the specific request
    INPUT
    serverData - json packet from server
    desiredData - ???
    */
}

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

function populateLimitaions(fuelLimitaions) {
  /**
   * takes the calculation output from the server and displays it in the left side menu
   * INPUT
   * fuelLimitaions - fuel for takeoff and landing {"takeoff_fuel" : value , "landing_fuel" : value,
   * "units" : value , centrogram ???}
   * chartData - data to populate the weight-CG chart
   * OUTPUT
   * none
   *  */
  try {
    document.getElementById("takeoff_fuel").innerHTML =
      fuelLimitaions["takeoff_fuel"];
    document.getElementById("landing_fuel").innerHTML =
      fuelLimitaions["landing_fuel"];
    document.querySelectorAll(".units").forEach((element) => {
      element.innerHTML = fuelLimitaions["units"];
    });
  } catch (error) {
    document.getElementById("takeoff_fuel").innerHTML = "-";
    document.getElementById("landing_fuel").innerHTML = "-";
    document.querySelectorAll(".units").forEach((element) => {
      element.innerHTML = fuelLimitaions["units"];
    });
    console.error(error);
    alert("תקלה בחישוב התצורה");
  }
}

async function sendCalculationAndGetSolution(targetJson) {
  console.log("Creating data bundle");
  // createJsonResponse() TODO: edit this function
  console.log("Sending data");
  const response = await fetch("http://127.0.0.1:8000/receiveJSON", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(targetJson),
    credentials: "include",
    mode: "same-origin",
  }).then((response) => response.json());
  return await response;
}

/* event listeners */
document.addEventListener("DOMContentLoaded", () => {
  // Navbar buttons
  document.getElementById("tail_number").addEventListener("click", () => {
    document.getElementById("menu_headline").innerHTML = "מספרי זנב";
    populateRightMenu(aircrafts, "tailNumber", "aircraft");
  });

  document.getElementById("items").addEventListener("click", () => {
    document.getElementById("menu_headline").innerHTML = "פריטי משימה";
    populateRightMenu(ACitems, "itemName", "ACitems");
  });

  document.getElementById("presets").addEventListener("click", () => {
    document.getElementById("menu_headline").innerHTML = "פריסטים";
  });

  // Right menu buttons
  document.querySelectorAll(".aircraft").forEach((btn) => {});
  // Footer buttons

  document.getElementById("generatePDF").addEventListener("click", () => {});

  // Calculate button

  document.getElementById("calculate").addEventListener("click", () => {
    // TODO: bundle selections together into a JSON
    let button = document.getElementById("calculate");
    button.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> מחשב...';
    button.disabled = true;
    sendCalculationAndGetSolution(jsonz).then((answer) => {
      populateLimitaions(answer);
      button.innerHTML = "חשב!";
      button.disabled = false;
    });
  });

  let ctx = document.getElementById("fuelLimits");
  let scatterChart = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "מעטפת משקל -מ.כ",
          data: [
            {
              x: -10,
              y: 0,
            },
            {
              x: 0,
              y: 10,
            },
            {
              x: 10,
              y: 5,
            },
            {
              x: -5,
              y: 4,
            },
          ],
          pointBackgroundColor: "rgba(255,0,0,1)",
        },
      ],
    },
    options: {
      scales: {
        x: {
          type: "linear",
          position: "bottom",
        },
      },
    },
  });
});
