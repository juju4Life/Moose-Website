

function autocomplete(tags, tagId){
    $( function() {
    var availableTags = tags;
    $( tagId ).autocomplete({
      source: availableTags
    });
  } );
};

