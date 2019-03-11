
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>

<script type="text/javascript">
	var endpoint = '{% url "chart_inventory" %}'
	var dates = []
	var englishFoils = []
	var englishFoilsAvg = []
	var english = []
	var englishAvg = []
	var foreignFoils = []
	var foreignFoilsAvg = []
	var foreign = []
	var foreignAvg = []
	var pokemon = []
	var pokemonAvg = []
	$.ajax({
		method: 'GET',
		url: endpoint,
		success: function(data){
			dates = data.dates;
			englishFoils = data.foil_orders;
			englishFoilsAvg = data.foil_orders_avg;
			english = data.english_orders;
			englishAvg = data.english_orders_avg;
			foreignFoils = data.foreign_foil_orders;
			foreignFoilsAvg = data.foreign_foil_orders_avg;
			foreign = data.foreign_orders;
			foreignAvg = data.foreign_orders_avg;
			pokemon = data.pokemon_orders;
			pokemonAvg = data.pokemon_orders_avg;
			setChart();
		},

		error: function(error_data){
			console.log('Errors');
			console.log(error_data);
		}
	})

function setChart(){

	var graph_foils = document.getElementById("foils").getContext('2d');

	var backgroudRGB = [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ];

	var borderRGB = [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ];


	var myChart = new Chart(graph_foils, {
	    type: 'line',
	    data: {
	        labels: dates,
	        datasets: [

	        {
	            label: `English Foils ${englishFoilsAvg} cards per day`,
	            data: englishFoils,
	            backgroundColor: "purple",
	            borderColor: "purple",
	            borderWidth: 1,
	            fill: false,
	            pointBorderColor: "white",
                pointBorderWidth: 1,
                pointHoverRadius: 2,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
	        },

	        {
	            label: `Foreign Foils ${foreignFoilsAvg} cards per day`,
	            data: foreignFoils,
	            backgroundColor: "red",
	            borderColor: "red",
	            borderWidth: 1,
	            fill: false,
	            pointBorderColor: "white",
                pointBorderWidth: 1,
                pointHoverRadius: 2,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
	        },

	        {
	            label: `Foreign non-foil ${foreignAvg} cards per day`,
	            data: foreign,
	            backgroundColor: "green",
	            borderColor: "green",
	            borderWidth: 1,
	            fill: false,
	            pointBorderColor: "white",
                pointBorderWidth: 1,
                pointHoverRadius: 2,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
	        },

	        {
	            label: `English Non-foil ${englishAvg} cards per day`,
	            data: english,
	            backgroundColor: "blue",
	            borderColor: "blue",
	            borderWidth: 1,
	            fill: false,
	            pointBorderColor: "white",
                pointBorderWidth: 1,
                pointHoverRadius: 2,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
	        },

	        {
	            label: `Pokemon ${pokemonAvg} cards per day`,
	            data: pokemon,
	            backgroundColor: "orange",
	            borderColor: "orange",
	            borderWidth: 1,
	            fill: false,
	            pointBorderColor: "white",
                pointBorderWidth: 1,
                pointHoverRadius: 2,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
	        },

	        ]
	    },
	    options: {
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero:true
	                }
	            }]
	        },

	        title: {
	            display: true,
	            text: "Ratio % of cards sold within it's category",
	            fontSize: 15,
	        }
	    }
	});

	}




</script>//