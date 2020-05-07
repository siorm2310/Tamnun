const aircraftType = JSON.parse(
  document.getElementById("aircraftType").textContent
);
const aircrafts = JSON.parse(document.getElementById("aircrafts").textContent);
const ACitems = JSON.parse(document.getElementById("JsonACitems").textContent);

const objectHolder = {
  aircraftType: aircraftType,
  aircrafts: aircrafts,
  ACitems: ACitems,
};

function getObjectById(dataId, targetJsonString) {
  const targetJson = objectHolder[targetJsonString];
  const extractedObject = targetJson.find((obj) => {
    return obj["id"] == dataId;
  });
  if (extractedObject === undefined) {
    console.warn(`No object with id : ${dataId} in ${targetJsonString}`);
    return null;
  }
  return extractedObject;
}

class ItemDisc extends HTMLElement {
  constructor() {
    super();

    switch (this.getAttribute("name")) {
      case "aircrafts":
        var selectedObject = getObjectById(
          this.getAttribute("data-id"),
          "aircrafts"
        );
        this.innerHTML = `
        <div class="form-row">
        <strong>משקל:</strong>
        <input
          type="number"
          step="0.01"
          name=""
          id="weight_default"
          class="form-control"
        />
      </div>
      <div class="form-row">
        <strong>מיקום:</strong>
        <input
          type="number"
          step="0.01"
          name=""
          id="cgx_default"
          class="form-control"
        />
      </div>
      <div class="form-row">
        <input
          class="form-check-input"
          type="checkbox"
          value=""
          id="derivative"
        />
        <label class="form-check-label" for="derivative">
          נגזרת?
        </label>
      </div>
      <button class="btn btn-primary id="add_to_config">הוסף לתצורה</button>
        `;
        break;

      case "ACitems":
        var selectedObject = getObjectById(
          this.getAttribute("data-id"),
          "ACitems"
        );
        this.innerHTML = `
        <div class="form-row">
        <strong>משקל:</strong>
        <input
          type="number"
          step="0.01"
          name=""
          id="weight_default"
          class="form-control"
        />
        <input
          type="number"
          step="0.01"
          name=""
          id="weight_delta"
          class="form-control"
        />
        <input
          type="number"
          step="0.01"
          name=""
          id="weight_user"
          class="form-control"
        />
      </div>
      <div class="form-row">
        <strong>מיקום:</strong>
        <input
          type="number"
          step="0.01"
          name=""
          id="cgx_default"
          class="form-control"
        />
        <input
          type="number"
          step="0.01"
          name=""
          id="cgx_delta"
          class="form-control"
        />
        <input
          type="number"
          step="0.01"
          name=""
          id="cgx_user"
          class="form-control"
        />
      </div>
      <div class="form-row">
        <input
          class="form-check-input"
          type="checkbox"
          value=""
          id="derivative"
        />
        <label class="form-check-label" for="derivative">
          נגזרת?
        </label>
      </div>
      <button class="btn btn-primary id="add_to_config"">הוסף לתצורה</button>
        `;
        break;
    }
  }
}

window.customElements.define("item-disc", ItemDisc);
