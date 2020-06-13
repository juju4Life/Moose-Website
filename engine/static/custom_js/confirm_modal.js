
$( function() {
    $( ".dialog-confirm-data" ).dialog({
        autoOpen: false,
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
      buttons: {
        "Confirm": function() {
          $( this ).dialog( "close" );
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });

    $(".confirm-button").click(function( e ) {
        e.preventDefault();
        $('.dialog-confirm-data').dialog('open');
    });

} );