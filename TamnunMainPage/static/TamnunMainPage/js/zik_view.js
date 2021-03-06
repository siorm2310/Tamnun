class ItemMenu extends HTMLElement {
    constructor() {
        super();

        this.innerHTML = menuItems
    }
    // Fires when an instance was inserted into the document
      connectedCallback() {
    }

    // Fires when an instance was removed from the document
    disconnectedCallback() {
    }

    // Fires when an attribute was added, removed, or updated
    attributeChangedCallback(attrName, oldVal, newVal) {
    }

    // Fires when an element is moved to a new document
    adoptedCallback() {
    }
}

// Registers custom element
window.customElements.define('item-menu', ItemMenu);