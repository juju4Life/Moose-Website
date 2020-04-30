
function jqueryDialogBox(boxId, buttonId){
    $( function() {
        $( boxId ).dialog({
          autoOpen: false,
          position: { my: "left top", at: "right top", of: buttonId },
          show: {
            effect: "drop",
          },
          hide: {
            effect: "drop",
          }
      });

    $( buttonId ).on( "click", function() {
      $( boxId ).dialog( "open" );
    });
  } );
};