
function setActiveAttribute( obj, n ){

    $(function () {
            $('#' + obj.id + ' li:nth-child(' + n + ') a').tab('show')
          })
}

function chooseActiveElement( obj ){
    let data = obj.getElementsByTagName('li');

    /* Make tab active if item as a foil or non-foil stock that is greater than 0. Hierarchy: clean > played > heavily played.
    Defaults to resotck tab if all variants show 0 for stock */

    if ( data[0].getAttribute('data-normal-stock') > 0  || data[0].getAttribute('data-foil-stock' ) > 0){
        setActiveAttribute(obj, 1);

    } else if ( data[1].getAttribute('data-normal-stock') > 0 || data[1].getAttribute('data-foil-stock' ) > 0){
        setActiveAttribute(obj, 2);

    } else if ( data[2].getAttribute('data-normal-stock') > 0 || data[2].getAttribute('data-foil-stock' ) > 0){
        setActiveAttribute(obj, 3);
    } else {
        setActiveAttribute(obj, 4);
    }

}

var docs = document.getElementsByClassName('condition-info');
var i;
for (i = 0; i < docs.length; i++){
    chooseActiveElement(docs[i]);
}
