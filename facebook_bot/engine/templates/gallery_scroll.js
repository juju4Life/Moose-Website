


<script type='text/javascript'>

    var endpoint = "{% url 'hotlist' %}"

    $.ajax({
		method: 'GET',
		url: endpoint,
		success: function(data){
		    // Data set format = [[name, expansion, price, image], [name,...]]
		    var imageData = function(position){
            index = parseInt(position) - 1
            document.getElementById(`gallery-image-${position}`).setAttribute('src', data.cards[index][3]);
            document.getElementById(`image-info-${position}`).innerHTML = `${data.cards[index][1]}: ${data.cards[0][0]}`;
            document.getElementById(`image-price-${position}`).innerHTML = `$${data.cards[index][2]}`;
    }
            imageData(1)
            imageData(2)
            imageData(3)


		},

		error: function(error_message){
		    console.log('Errors:');
		    console.log(error_message);
		}
		})

</script>




