
// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Create initial data table for product
function populateConditionTable( is_active, condition, name, expansion, language, productId, normalStock, foilStock, normalPrice, foilPrice, userAuthenticated, normalOnly, foilOnly ){

    var parentId = `tabs-tabContent-${productId}`;
    var parentDiv = document.getElementById(parentId);

    var mainDiv = document.createElement("div");
    var id = `tab-${condition}-${productId}`;
    var itemRef = `clean-tab-${productId}`;
    mainDiv.setAttribute("id", id);
    mainDiv.setAttribute("role", "tabpanel");
    mainDiv.setAttribute("aria-labelledby", itemRef);

    if ( is_active === "true" ){
        mainDiv.setAttribute("class", "tab-pane fade show active");
    } else{
        mainDiv.setAttribute("class", "tab-pane fade show");
    }

    var table = document.createElement("table");
    table.setAttribute("class", "card-search-table table-responsive table-borderless");

    var body = document.createElement("tbody");

    if ( foilOnly !== false ){
        let normalRow = createConditionTableRow(condition, "Normal", normalStock, normalPrice, productId, name, expansion, language, userAuthenticated);
        body.appendChild(normalRow);
    }

    if ( condition !== 'restock' && normalOnly !== true){
        let foilRow = createConditionTableRow(condition, "Foil", foilStock, foilPrice, productId, name, expansion, language, userAuthenticated);
        body.appendChild(foilRow);
    }

    table.appendChild(body);

    mainDiv.appendChild(table);
    parentDiv.appendChild(mainDiv);
}

// Create row for data variants in condition / price data table
function createConditionTableRow(condition, printing, stock, price, productId, name, expansion, language, userAuthenticated){

    row = document.createElement("tr");
    td = document.createElement("td");
    if ( condition === "restock" ){
        const tdRestockNotice = document.createElement("td");

        const formButton = document.createElement("button");
        formButton.setAttribute("class", "btn btn-info btn-sm mr-1 restock-submit-form");
        formButton.setAttribute("type", "submit");
        if ( userAuthenticated ){
            formButton.setAttribute("id", `restock-button-submit-${productId}`)

        } else {
            formButton.setAttribute("id", `restock-button-login-${productId}`)
        }


        var formButtonText = document.createTextNode("Restock Alert ");
        formButton.appendChild(formButtonText);
        var buttonIcon1 = document.createElement("i");
        buttonIcon1.setAttribute("class", "material-icons");
        buttonIcon1Text = document.createTextNode('email');
        buttonIcon1.appendChild(buttonIcon1Text);
        formButton.appendChild(buttonIcon1);

        tdRestockNotice.appendChild(formButton);
        row.appendChild(tdRestockNotice);
    } else {
        tdSpan = document.createElement("span");
    tdSpan.setAttribute("style", "color: rgba(0, 0, 0, .4);");
    tdSpanText = document.createTextNode(printing);
    tdSpan.appendChild(tdSpanText);

    td.appendChild(tdSpan);
    row.appendChild(td);

    // Create form with price and quantity if item quantity > 0
    if (stock > 0){

        var tdPrice = document.createElement("td");
        var tdPriceSpan = document.createElement("span");
        tdPriceSpan.setAttribute("class", "mr-1");
        var tdPriceSpanText = document.createTextNode(`$${price} ` + '| ' + `qty. ${stock}`);
        tdPriceSpan.appendChild(tdPriceSpanText);
        tdPrice.appendChild(tdPriceSpan);
        row.appendChild(tdPrice);

        // Row Form Data
        var tdForm = document.createElement("td");
        var form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("class", "add-to-cart-form");
        form.setAttribute("data-url", `cart/add/${productId}`);

        // Get csrf token
        var csrfToken = getCookie("csrftoken");
        var inputElem = document.createElement('input');
        inputElem.type = 'hidden';
        inputElem.name = 'csrfmiddlewaretoken';
        inputElem.value = csrfToken;
        form.appendChild(inputElem);

        var formDiv = document.createElement('div');
        formDiv.setAttribute("class", "form-box");

        var formInput = document.createElement("input");
        formInput.setAttribute("class", "mr-1");
        formInput.setAttribute("size", 2);
        formInput.setAttribute("type", "number");
        formInput.setAttribute("name", "quantity");
        formInput.setAttribute("min", "1");
        formInput.setAttribute("max", stock);
        formDiv.appendChild(formInput);

        var printingInput = document.createElement("input");
        printingInput.setAttribute("type", "hidden");
        printingInput.setAttribute("name", "printing");
        printingInput.setAttribute("value", printing);
        form.appendChild(printingInput);

        var conditionInput = document.createElement("input");
        conditionInput.setAttribute("type", "hidden");
        conditionInput.setAttribute("name", "condition");
        conditionInput.setAttribute("value", condition);
        form.appendChild(conditionInput);

        var priceInput = document.createElement("input");
        priceInput.setAttribute("type", "hidden");
        priceInput.setAttribute("name", "price");
        priceInput.setAttribute("value", price);
        form.appendChild(priceInput);

        var nameInput = document.createElement("input");
        nameInput.setAttribute("type", "hidden");
        nameInput.setAttribute("name", "name");
        nameInput.setAttribute("value", name);
        form.appendChild(nameInput);

        var setInput = document.createElement("input");
        setInput.setAttribute("type", "hidden");
        setInput.setAttribute("name", "expansion");
        setInput.setAttribute("value", expansion);
        form.appendChild(setInput);

        var languageInput = document.createElement("input");
        languageInput.setAttribute("type", "hidden");
        languageInput.setAttribute("name", "language");
        languageInput.setAttribute("value", language);
        form.appendChild(languageInput);

        var maxQuantityInput = document.createElement("input");
        maxQuantityInput.setAttribute("type", "hidden");
        maxQuantityInput.setAttribute("name", "max_quantity");
        maxQuantityInput.setAttribute("value", stock);
        form.appendChild(maxQuantityInput);

        var formButton = document.createElement("button");
        formButton.setAttribute("class", "btn btn-success btn-sm mr-1");
        formButton.setAttribute("type", "submit");
        formButton.setAttribute("id", `add-to-cart-${printing}-${condition}-${productId}`);
        formButton.setAttribute("title", "");
        var buttonIcon1 = document.createElement("i");
        buttonIcon1.setAttribute("class", "material-icons");
        buttonIcon1Text = document.createTextNode('add');
        buttonIcon1.appendChild(buttonIcon1Text);
        formButton.appendChild(buttonIcon1);
        var buttonIcon2 = document.createElement("i");
        buttonIcon2.setAttribute("class", "material-icons");
        buttonIcon2Text = document.createTextNode('shopping_cart');
        buttonIcon2.appendChild(buttonIcon2Text);
        formButton.appendChild(buttonIcon2);
        formDiv.appendChild(formButton);
        form.appendChild(formDiv);
        form.appendChild(formDiv);
        tdForm.appendChild(form);
        row.appendChild(tdForm);

    } else{

        var tdOutOfStock = document.createElement("td");
        var tdSpan = document.createElement("span");
        tdSpanText = document.createTextNode("Out of Stock");
        tdSpan.appendChild(tdSpanText);
        tdOutOfStock.appendChild(tdSpan);
        row.appendChild(tdOutOfStock);


    };

    };


    return row
};

function createConditionTab(condition, conditionAbbreviation, normalStock, foilStock, productId, is_active){
    var li = document.createElement("li");
        li.setAttribute("class", "nav-item");
        li.setAttribute("data-normal-stock", normalStock);
        li.setAttribute("data-foil-stock", foilStock);

        var a = document.createElement("a");
        var id = `${condition}-tab-${productId}`;
        a.setAttribute("id", id);
        var itemRef = `tab-${condition}-${productId}`;
        a.setAttribute("href", "#" + itemRef);
        a.setAttribute("aria-controls", itemRef);
        a.setAttribute("data-toggle", "tab");
        a.setAttribute("role", "tab");
        a.setAttribute("aria-selected", "true");

        if (is_active === 'true'){
            a.setAttribute("class", "nav-link active");
        } else {
            a.setAttribute("class", "nav-link");
        };

        var span = document.createElement("span");
        var text = document.createTextNode(conditionAbbreviation);

        if ( normalStock <= 0 && foilStock <= 0 && condition !== "restock" ){
            span.setAttribute("style", "color: gray;");
            strikeThrough = document.createElement("strike");
            strikeThrough.appendChild(text);
            text = strikeThrough;
        };

        span.appendChild(text);
        a.appendChild(span);
        li.appendChild(a);
    return li

};

function conditionTab(condition, conditionAbbreviation, normalStock, foilStock, productId, is_active){
    var ul = document.getElementById(productId);
    li = createConditionTab(condition, conditionAbbreviation, normalStock, foilStock, productId, is_active);
    ul.appendChild(li);
};
