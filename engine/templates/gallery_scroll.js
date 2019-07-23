


<script type='text/javascript'>

    var endpoint = "{% url 'hotlist' %}"
    $.ajax({
		method: 'GET',
		url: endpoint,
		success: function(data){
		    // Data set format = [[name, expansion, price, image], [name,...]]
            document.getElementById('gallery-image-1').setAttribute('src', data.cards[0][3]);
            document.getElementById('image-expansion').innerHTML = `${data.cards[0][1])};
            document.getElementById('gallery-image-2').setAttribute('src', data.cards[1][3]);
            document.getElementById('gallery-image-3').setAttribute('src', data.cards[2][3]);
		},

		error: function(error_message){
		    console.log('Errors:');
		    console.log(error_message);
		}
		})

</script>




