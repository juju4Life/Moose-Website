
$(document).ready( function() {
    var $myForm = $(".add-to-cart-form");
    $myForm.submit( function( event ){

        event.preventDefault();
        // var $formData = $myForm.serialize();

        let $thisURL = this.getAttribute("data-url") || window.location.href;
        let inputList = $(this).serializeArray();
        let data = {};
        let cookie = getCookie("csrftoken");

        inputList.forEach( function( input ) {
            data[input.name] = input.value;
        } )

        $.ajax({
            method: this.getAttribute("method"),
            url: $thisURL,
            type: 'POST',
            headers: {
                'X-CSRFTOKEN': cookie,
            },
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

        // let $formData = $myForm.serialize();
        let $thisURL = this.getAttribute("data-url") || window.location.href;
        let inputList = $(this).serializeArray();
        let data = {};
        let cookie = getCookie("csrftoken");

        inputList.forEach( function( input ) {
            data[input.name] = input.value;
        } );

        $.ajax({
            method: this.getAttribute("method"),
            url: $thisURL,
            data: data,
            type: 'POST',
            headers: {
                'X-CSRFTOKEN': cookie,
            },
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
        let cookie = getCookie("csrftoken");

        inputList.forEach( function(input) {
            data[input.name] = input.value;
        } );
        $.ajax({
            method: this.getAttribute("method"),
            url: $thisURL,
            data: data,
            type: 'POST',
            headers: {
                'X-CSRFTOKEN': cookie,
            },
            success: handleSuccess,
            error: handleError,
        });

        function handleSuccess( data ){
            $('.loader-icon').fadeOut();
            let id = "#" + data.id;
             $( function() {
                const tooltips = $( id ).tooltip({
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

        }

        function handleError( err ){
            console.log(err);
        }

    });
});


