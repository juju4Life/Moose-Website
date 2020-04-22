
// Create data table for condition / price select
function populateConditionTable(is_active, condition, productId, normalStock, foilStock, normalPrice, foilPrice){
    var parentId = `tabs-tabContent-${productId}`;
    var parentDiv = document.getElementById(parentId);

    var mainDiv = document.createElement("div");
    var id = `tab-${condition}-${productId}`;
    var itemRef = `clean-tab-${productId}`;
    mainDiv.setAttribute("id", id);
    mainDiv.setAttribute("role", "tabpanel");
    mainDiv.setAttribute("aria-labelledby", itemRef);

    if (is_active == "true"){
        mainDiv.setAttribute("class", "tab-pane fade show active");
    } else{
        mainDiv.setAttribute("class", "tab-pane fade show");
    };

    var table = document.createElement("table");
    table.setAttribute("class", "card-search-table");

    var body = document.createElement("tbody");
    var normalRow = createConditionTableRow("Normal", normalStock, normalPrice, productId);
    var foilRow = createConditionTableRow("Foil", foilStock, foilPrice, productId);
    body.appendChild(normalRow);
    body.appendChild(foilRow);
    table.appendChild(body);

    mainDiv.appendChild(table);
    parentDiv.appendChild(mainDiv);
};

// Create row for data variants in condition / price data table
function createConditionTableRow(printing, stock, price, productId){
    row = document.createElement("tr");

    td = document.createElement("td");

    tdSpan = document.createElement("span");
    tdSpan.setAttribute("style", "color: rgba(0, 0, 0, .4);");
    tdSpanText = document.createTextNode(printing);
    tdSpan.appendChild(tdSpanText);

    td.appendChild(tdSpan);
    row.appendChild(td);
    if (stock > 0){
        var tdPrice = document.createElement("td");
        var tdPriceSpan = document.createElement("span");
        tdPriceSpan.setAttribute("class", "mr-1");
        var tdPriceSpanText = document.createTextNode("$" + price);
        tdPriceSpan.appendChild(tdPriceSpanText);
        tdPrice.appendChild(tdPriceSpan);
        row.appendChild(tdPrice);

        var tdStock = document.createElement("td");
        var tdStockSpan = document.createElement("span");
        tdStockSpan.setAttribute("class", "mr-1");
        var tdStockSpanText = document.createTextNode("qty. " + stock);
        tdStockSpan.appendChild(tdStockSpanText);
        tdStock.appendChild(tdStockSpan);
        row.appendChild(tdStock);

        // Row Form Data
        var tdForm = document.createElement("td");
        var form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("action", "{% url 'add_to_cart' " + productId + " %}");
        // form += '{% csrf_token %}';
        var formDiv = document.createElement('div');
        formDiv.setAttribute("class", "form-box");
        formInput = document.createElement("input");
        formInput.setAttribute("class", "mr-1");
        formInput.setAttribute("size", 2);
        formInput.setAttribute("type", "number");
        formInput.setAttribute("name", "quantity");
        formInput.setAttribute("min", 1);
        formInput.setAttribute("max", stock);
        formDiv.appendChild(formInput);
        var formButton = document.createElement("button");
        formButton.setAttribute("class", "btn btn-success btn-sm mr-1");
        formButton.setAttribute("type", "submit");
        var buttonIcon1 = document.createElement("i");
        buttonIcon1.setAttribute("class", "material-icons");
        buttonIcon1Text = document.createTextNode('add');
        buttonIcon1.appendChild(buttonIcon1Text);
        formButton.appendChild(buttonIcon1);
        console.log(buttonIcon1);
        var buttonIcon2 = document.createElement("i");
        buttonIcon2.setAttribute("class", "material-icons");
        buttonIcon2Text = document.createTextNode('shopping_cart');
        buttonIcon2.appendChild(buttonIcon2Text);
        formButton.appendChild(buttonIcon2);
        console.log(buttonIcon2);
        formDiv.appendChild(formButton);
        form.appendChild(formDiv);
        form.appendChild(formDiv);
        tdForm.appendChild(form);
        row.appendChild(tdForm);
    } else{
        var tdOutOfStock = document.createElement("td");
        var tdSpan = document.createElement("span");
        // tdSpan.setAttribute("class", "mr-1");
        tdSpanText = document.createTextNode("Out of Stock");
        tdSpan.appendChild(tdSpanText);
        tdOutOfStock.appendChild(tdSpan);
        row.appendChild(tdOutOfStock);

        var tdRestockNotice = document.createElement("td");
        var form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("action", "#");
        // form += '{% csrf_token %}';
        var formButton = document.createElement("button");
        formButton.setAttribute("class", "btn btn-info btn-sm mr-1");
        formButton.setAttribute("type", "submit");
        var formButtonText = document.createTextNode("Restock Alert ");
        formButton.appendChild(formButtonText);
        var buttonIcon1 = document.createElement("i");
        buttonIcon1.setAttribute("class", "material-icons");
        buttonIcon1Text = document.createTextNode('email');
        buttonIcon1.appendChild(buttonIcon1Text);
        formButton.appendChild(buttonIcon1);
        form.appendChild(formButton);
        tdRestockNotice.appendChild(form);
        row.appendChild(tdRestockNotice);
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

        if (is_active == 'true'){
            a.setAttribute("class", "nav-link active");
        } else {
            a.setAttribute("class", "nav-link");
        };

        var span = document.createElement("span");
        var text = document.createTextNode(conditionAbbreviation);
        if (normalStock <= 0 && foilStock <= 0){
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
