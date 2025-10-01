class Popup {
    constructor(title, options = {}) {
        this.title = title;
        this.dark = options.dark || false;
        this.formSubmission = options.formSubmission || false;
        this.centered = options.centered || false;
        this.closeable = options.closeable || true;
        this.animation = options.animation || true;
        this.container = document.createElement('div');
        this.content = document.createElement(this.formSubmission ? 'form' : 'div');

        if (this.formSubmission) {
            this.content.setAttribute('method', 'POST');
        }

        // bind methods
        this.hide = this.hide.bind(this);
        this.show = this.show.bind(this);
    }

    initialize() {
        // clear old content
        this.content.innerHTML = '';

        // set classes
        this.container.classList.add('popup');
        this.content.classList.add('popup-content');

        if (this.centered) {
            this.content.classList.add('center');
        }
        if (!this.animation) {
            this.container.style.animation = 'none';
            this.content.style.animation = 'none';
        }
        if (this.dark) this.content.classList.add('bg-dark');

        // load content
        const closeNode = button('', 'close', this.hide);
        const titleNode = document.createElement('h3');
        titleNode.innerHTML = this.title;

        if (this.closeable) this.content.appendChild(closeNode);
        this.content.appendChild(titleNode);
        this.content.appendChild(document.createElement('hr'));

        for (const el of this.getContent()) {
            this.content.appendChild(el);
        }

        // append elements
        document.body.appendChild(this.container);
        this.container.appendChild(this.content);
    }

    async reload() {
        // clear old content
        this.content.innerHTML = '';

        // load content
        const closeNode = button('', 'close', this.hide);
        const titleNode = document.createElement('h3');
        titleNode.innerHTML = this.title;

        if (this.closeable) this.content.appendChild(closeNode);
        this.content.appendChild(titleNode);
        this.content.appendChild(document.createElement('hr'));

        for (const el of this.getContent()) {
            this.content.appendChild(el);
        }
    }

    isVisible() {
        return this.container.classList.contains('show');
    }

    show() {
        this.container.classList.add('show');
    }

    hide() {
        this.container.classList.remove('show');
    }

    toggle() {
        this.isVisible() ? this.hide() : this.show();
    }

    getContent() {
        throw new Error("method must be implemented.");
    }
}

class PopupHeaderList extends Popup {
    constructor(headers = {}) {
        super("Benutzerdefinierte Header", { dark: false, centered: true, animation: true });
        this.headers = headers;
        this.contentTable = null;
    }

    getHeaders() {
        return this.headers;
    }

    deleteHeader(key) {
        delete this.headers[key];
        this.reload();
    }

    addHeader(key, value) {
        if (String(key).length == 0) {
            return false;
        }

        this.headers[key] = value;
        this.reload();
        return true;
    }

    reload() {
        let tableRows = [];
        for (let key in this.headers) {
            if (this.headers.hasOwnProperty(key)) {
                let value = this.headers[key];
                let deleteBtn = iconButton("", ['fa', 'fa-trash'], 'danger', () => this.deleteHeader(key));

                tableRows.push([
                    key,
                    value,
                    deleteBtn
                ]);
            }
        }
        this.contentTable = table(["Schlüssel", "Wert", "Aktion"], tableRows);

        const headerBtn = document.getElementById("btn-header");
        headerBtn.value = headerBtn.value.split('(')[0] + '(' + Object.keys(this.headers).length + ')';
        super.reload();
    }

    getContent() {
        const keyInput = textInput("Key", "", false, 256);
        const valueInput = textInput("Value", "", false, 8192);
        const addBtn =  iconButton("Hinzufügen", ['fa', 'fa-plus', 'fa-2xs'], 'success', () => {
            if (this.addHeader(keyInput.value, valueInput.value)) {
                keyInput.value = "";
                valueInput.value = "";
            }
        });

        if (!this.contentTable)
            this.contentTable = table(["Schlüssel", "Wert", "Aktion"], []);

        return [keyInput, valueInput, addBtn, this.contentTable];
    }
}

class AuthenticationTablePopup extends Popup {
    constructor() {
        super("Authentication Table", {
            centered: true,
            closeable: true
        });
        this.initialize();
    }

    getContent() {
        const elements = [];

        const table = document.createElement("table");
        table.classList.add("table");

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        ["Column", "Type", "Default", "Primary Key"].forEach(h => {
            const th = document.createElement("th");
            th.textContent = h;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");

        const columns = [
            {
                name: "id",
                type: "int(11)",
                default_value: "AUTO_INCREMENT",
                primary: true
            },
            {
                name: "user",
                type: "varchar(8)",
                default_value: "NOT NULL",
                primary: false
            },
            {
                name: "auth_key",
                type: "varchar(36)",
                default_value: "uuid()",
                primary: false
            }
        ];

        columns.forEach(col => {
            const tr = document.createElement("tr");

            const tdName = document.createElement("td");
            tdName.textContent = col.name;
            tr.appendChild(tdName);

            const tdType = document.createElement("td");
            tdType.textContent = col.type;
            tr.appendChild(tdType);

            const tdDefault = document.createElement("td");
            tdDefault.textContent = col.default_value;
            tr.appendChild(tdDefault);

            const tdPrimary = document.createElement("td");
            tdPrimary.textContent = col.primary ? "✔" : "";
            tr.appendChild(tdPrimary);

            tbody.appendChild(tr);
        });

        table.appendChild(tbody);
        elements.push(table);

        elements.push(document.createElement('hr'));
        elements.push(button("DDL ansehen", ["primary"], () => {
            document.location.href = '/static/documentation/authentication_table.ddl'
         }, false));

        return elements;
    }
}


/**
    input-creation functions
*/

function button(text, style, onclick = null, submit = false) {
    const node = document.createElement('button');
    node.innerHTML = text;
    node.type = submit ? 'submit' : 'button';
    node.classList.add('btn', `btn-${style}`, 'sp-btm');

    if (onclick) node.addEventListener('click', onclick);

    return node;
}

function iconButton(text, classList, style, onclick = null) {
    const node = document.createElement('button');
    const ico = document.createElement('i');

    classList.forEach(c => ico.classList.add(c));
    node.appendChild(ico);

    node.innerHTML += ` ${text}`;
    node.type = 'button';
    node.classList.add('btn', `btn-${style}`, 'sp-btm');

    if (onclick) node.addEventListener('click', onclick);

    return node;
}

function textButton(text, onclick = null, href = null) {
    const node = document.createElement('a');
    node.innerHTML = text;
    if (onclick) node.addEventListener('click', onclick);
    if (href) node.href = href;

    return node;
}

function createSelectionButton(text, iconClass, route, callback) {
    const button = iconButton(text, ['fa', iconClass], 'info');
    button.addEventListener('click', () => {
        new PopupSelection(route, callback).show();
    });
    return button;
}

function selectInput(options = [], selectedValue = '') {
    const node = document.createElement('select');
    node.classList.add('form-select', 'sp-btm');

    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option.value;
        opt.innerHTML = option.text;
        if (option.value === selectedValue) {
            opt.selected = true;
        }
        node.appendChild(opt);
    });

    return node;
}

function textInput(placeholder = '', value = '', required = false, maxLength = 255) {
    const node = document.createElement('input');
    node.type = 'text';
    node.placeholder = placeholder;
    node.maxLength = maxLength;
    node.value = value;
    node.classList.add('form-control', 'sp-btm');

    if (required) {
        node.required = true;
    }

    return node;
}

function createFileElement(file, index, dragStart, dragOver, drop) {
    let node;

    if (file.type.startsWith('image')) {
        node = document.createElement('img');
        //node.src = 'data:image/png;base64,' + file.data;
        node.src = (!file.data.startsWith('data:') ? 'data:image/png;base64,' + file.data : file.data);
    } else if (file.type.startsWith('video')) {
        node = document.createElement('video');
        //node.src = 'data:video/mp4;base64,' + file.data;
        node.src = (file.data.startsWith('data:') ? 'data:video/mp4;base64,' + file.data : file.data);
        node.controls = true;
    } else if (file.type.startsWith('audio')) {
        node = document.createElement('audio');
        //node.src = 'data:audio/mp3;base64,' + file.data;
        node.src = (file.data.startsWith('data:') ? 'data:audio/mp3;base64,' + file.data : file.data);
        node.controls = true;
    }
    node.classList.add('draggable');
    node.setAttribute('draggable', true);
    node.addEventListener('dragstart', dragStart);
    node.addEventListener('dragover', dragOver);
    node.addEventListener('drop', drop);
    return node;
}

function table(headers, rows) {
    let table = document.createElement('table');
    table.classList.add('table', 'sp-btm');

    let thead = document.createElement('thead');
    let headerRow = document.createElement('tr');
    headers.forEach(header => {
        let th = document.createElement('th');
        th.innerText = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    let tbody = document.createElement('tbody');
    rows.forEach(rowData => {
        let row = document.createElement('tr');
        rowData.forEach(cellData => {
            let td = document.createElement('td');

            if (Array.isArray(cellData)) {
                // Falls cellData eine Liste ist, Buttons korrekt einfügen
                cellData.forEach(el => td.appendChild(el));
            } else if (cellData instanceof HTMLElement) {
                td.appendChild(cellData);
            } else {
                td.innerText = cellData;
            }
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    return table;
}