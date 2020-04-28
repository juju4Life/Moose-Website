function createAccordion(className){
$( function() {
$( "." + className ).accordion({
  collapsible: true,
  active: false,
  heightStyle: "content",
});
} );
};