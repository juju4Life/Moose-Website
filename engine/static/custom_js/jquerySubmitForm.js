
$(document).ready( function() {
    var $myForm = $(".add-to-cart-form");
    $myForm.submit( function( event ){
        event.preventDefault();
        var $formData = $myForm.serialize();
        var $thisURL = this.getAttribute("data-url") || window.location.href;
        var inputList = $(this).serializeArray();
        var data = {};

        inputList.forEach( function( input ) {
            data[input.name] = input.value;
        } );
        $.ajax({
            method: this.getAttribute("method"),
            url: $thisURL,
            data: data,
            success: handleSuccess,
            error: handleError,
        });

        function handleSuccess( data ){
            var id = "#" + data.id;
            $( function() {

                var tooltips = $( id ).tooltip({
                  position: {
                    my: "right top",
                    at: "right-5 top-50",
                    collision: "none"
                  },
                  content: data.message,
                  tooltipClass: "form-popup-tooltip",
                });


                tooltips.tooltip( "open" );

          } );
        };

        function handleError( err ){
            console.log(err);
        };


    })
});


$(document).ready( function(){
    var $myForm = $(".wishlist-submit-form");
    $myForm.submit( function( event ){
        event.preventDefault();

        var $formData = $myForm.serialize();
        var $thisURL = this.getAttribute("data-url") || window.location.href;
        var inputList = $(this).serializeArray();
        var data = {};

        inputList.forEach( function( input ) {
            data[input.name] = input.value;
        } );

        //console.log( $(this).find(":input") );
        $.ajax({
            method: this.getAttribute("method"),
            url: $thisURL,
            data: data,
            success: handleSuccess,
            error: handleError,
        });

        function handleSuccess( data ){
            var id = "#" + data.id;
            $( function() {
                var tooltips = $( id ).tooltip({
                  position: {
                    my: "left top",
                    at: "right+5 top-5",
                    collision: "none"
                  },
                  content: data.message,
                  tooltipClass: "form-popup-tooltip",
                });

                tooltips.tooltip( "open" );

          } );
        };

        function handleError( err ){
            console.log(err);
        };

    });
});


$(document).ready( function(){
    var $myForm = $(".restock-submit-form");
    $myForm.submit( function( event ){
        event.preventDefault();

        var $formData = $myForm.serialize();
        var $thisURL = this.getAttribute("data-url") || window.location.href;
        var inputList = $(this).serializeArray();
        var data = {};
        inputList.forEach( function(input) {
            data[input.name] = input.value;
        } );
        $.ajax({
            method: this.getAttribute("method"),
            url: $thisURL,
            data: data,
            success: handleSuccess,
            error: handleError,
        });

        function handleSuccess( data ){
            $('.loader-icon').fadeOut();
            var id = "#" + data.id;
            console.log(data);
             $( function() {
                var tooltips = $( id ).tooltip({
                  position: {
                    my: "right top",
                    at: "left+5 top-5",
                    collision: "none"
                  },
                  content: data.message,
                  tooltipClass: "form-popup-tooltip",
                });

                tooltips.tooltip( "open" );

          } );

        };

        function handleError( err ){
            console.log(err);
        };

    });
});


