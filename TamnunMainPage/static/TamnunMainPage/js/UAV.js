jsonz = { A: "a", B: "b" };
/* Asyncronous events  */

/* functionality */

/**
 * Displays buttons of selected type in RHS menu
 * @param {JSON} data - Json data revieved from backend
 * @param {string} displayData - Name of the item to be displayed in button
 * @param {string} dataName - class name to be added to button (identical to "data" name)
 */
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

function createItemDiscMenu(itemId, jsonKey) {
  let itemDiscMenu = document.getElementById("item_disc");
  itemDiscMenu.hidden = false;
  itemDiscMenu.innerHTML = `
  <item-disc name="${jsonKey}" data-id="${itemId}"></item-disc>
  `;
}
function deriveWeightAndBalanceData(serverData, desiredData) {}

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

/**
 * Populates the LHS menu in the server's response, displaying the limitations
 * and centrograms
 * @param {object<number>} fuelLimitaions - takeoff and landing limits
 */
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
/**
 * sends user selections (bundled in JSON format) to server side for calculation.
 * awaits the response and returns in in JSON format
 * @param {JSON} targetJson
 */
async function sendCalculationAndGetSolution(targetJson) {
  console.log("Creating data bundle");
  // createJsonResponse() TODO: edit this function
  console.log("Sending data");
  const response = await fetch("http://127.0.0.1:8000/Calc", {
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

    document.querySelectorAll(".aircraft").forEach((btn) => {
      btn.addEventListener("click", () => {
        createItemDiscMenu(btn.getAttribute("data-id"), "aircrafts");
      });
    });
  });

  document.getElementById("items").addEventListener("click", () => {
    document.getElementById("menu_headline").innerHTML = "פריטי משימה";
    populateRightMenu(ACitems, "itemName", "ACitems");

    document.querySelectorAll(".ACitems").forEach((btn) => {
      btn.addEventListener("click", () => {
        createItemDiscMenu(btn.getAttribute("data-id"), "ACitems");
      });
    });
  });

  document.getElementById("presets").addEventListener("click", () => {
    document.getElementById("menu_headline").innerHTML = "פריסטים";
  });
  // Footer buttons

  document.getElementById("generatePDF").addEventListener("click", () => {});

  // Calculate button

  document.getElementById("calculate").addEventListener("click", () => {
    let button = document.getElementById("calculate");
    // TODO: bundle selections together into a JSON
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
