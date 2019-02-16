
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>

<script type="text/javascript">
	var endpoint = '{% url "chart" %}'
	var labels = []
	var allOrders = []
	var mtgOrders = []
	var ygoOrders = []
	var pokemonOrders = []
	var dbsOrders = []
	var fowOrders = []
	var funkoOrders = []
	var sleevesOrders = []
	var suppliesOrders = []
	var nonFoilEnglishOrders = []
	var foilEnglishOrders = []
	var foilForeignOrders = []
	var nonFoilForeignOrders = []
	var boxesOrders = []
	var deckBoxOrders = []
	var averageOrders = ''
	var numberOfDays = ''
	var mtgAverageOrders = ''
	var mtgCount = ''
	var ygoCount = ''
	var pokemonCount = ''
	var dbsCount = ''
	var fowCount = ''
	var funkoCount = ''
	var sleevesCount = ''
	var suppliesCount = ''
	var nonFoilForeignCount = ''
	var foilForeignCount = ''
	var foilEnglishCount = ''
	var nonFoilEnglishCount = ''
	var boxesCount = ''
	var deckBoxCount = ''
	var rnaDates = ''
	$.ajax({
		method: 'GET',
		url: endpoint,
		success: function(data){
			labels = data.labels;
			allOrders = data.all_orders;
            mtgOrders = data.mtg;
            ygoOrders = data.ygo;
            pokemonOrders = data.pokemon;
            dbsOrders = data.dbs;
            fowOrders = data.fow;
            funkoOrders = data.funko;
            sleevesOrders = data.card_sleeves;
            suppliesOrders = data.supplies;
            nonFoilEnglishOrders = data.non_foil_english;
            foilEnglishOrders = data.foil_english;
            foilForeignOrders = data.foil_foreign;
            nonFoilForeignOrders = data.non_foil_foreign;
            boxesOrders = data.boxes;
            deckBoxOrders = data.deck_boxes;
            averageOrders = data.average;
            numberOfDays = data.number_of_days;
            mtgAverageOrders = data.mtg_average;
            mtgCount = data.mtg_count;
            ygoCount = data.ygo_count;
            pokemonCount = data.pokemon_count;
            dbsCount = data.dbs_count;
            fowCount = data.fow_count;
            funkoCount = data.funko_count;
            sleevesCount = data.sleeves_count;
            suppliesCount = data.supplies_count;
            nonFoilForeignCount = data.non_foil_foreign_count;
            foilForeignCount = data.foil_foreign_count;
            foilEnglishCount = data.foil_english_count;
            nonFoilEnglishCount = data.non_foil_english_count;
            boxesCount = data.boxes_count;
            deckBoxCount = data.deck_box_count;
            rnaDates = data.rna_dates;
			setChart();
		},


		error: function(error_data){
			console.log('Errors');
			console.log(error_data);
		}
	})

function setChart(){

	var ctx = document.getElementById("myChart").getContext('2d');
	var ctx2 = document.getElementById("myChart2").getContext('2d');
	var ctx3 = document.getElementById("myChart3").getContext('2d');
	var ctx4 = document.getElementById("myChart4").getContext('2d');

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


	var myChart = new Chart(ctx, {
	    type: 'line',
	    data: {
	        labels: labels,
	        datasets: [

	        {
	            label: 'foil english: ' + foilEnglishCount,
	            data: foilEnglishOrders,
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
	            label: 'foil foreign: ' + foilForeignCount,
	            data: foilForeignOrders,
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
	            label: 'non-foil foreign: ' + nonFoilForeignCount,
	            data: nonFoilForeignOrders,
	            backgroundColor: "darkgreen",
	            borderColor: "darkgreen",
	            borderWidth: 1,
	            fill: false,
	            pointBorderColor: "white",
                pointBorderWidth: 1,
                pointHoverRadius: 1,
                pointHoverBackgroundColor: "yellow",
                pointHoverBorderWidth: 2,
                pointRadius: 2,
                pointHitRadius: 10,
	        },

	        {
	            label: 'Boxes: ' + boxesCount,
	            data: boxesOrders,
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
	            text: 'Last 10,000 mtg orders - total quantities of irregular singles / boxes',
	            fontSize: 15,
	        }
	    }
	});

var myChart = new Chart(ctx2, {
	    type: 'line',
	    data: {
	        labels: labels,
	        datasets: [
	            {
	            label: 'fow: ' + fowCount,
	            data: fowOrders,
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

                {
                    label: 'ygo: ' + ygoCount,
                    data: ygoOrders,
                    backgroundColor: "gray",
                    borderColor: "gray",
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
                    label: 'pokemon: ' + pokemonCount,
                    data: pokemonOrders,
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
	            label: 'supplies: ' + suppliesCount,
	            data: suppliesOrders,
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
	            label: 'dbs: ' + dbsCount,
	            data: dbsOrders,
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
	            label: 'sleeves: ' + sleevesCount,
	            data: sleevesOrders,
	            backgroundColor: "pink",
	            borderColor: "pink",
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
	            label: 'deckboxes: ' + deckBoxCount,
	            data: deckBoxOrders,
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
	            label: 'funko: ' + funkoCount,
	            data: funkoOrders,
	            backgroundColor: "black",
	            borderColor: "black",
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
	            text: 'Last 10,000 non-mtg orders',
	            fontSize: 15,
	        }

	    }
	});

	var myChart = new Chart(ctx3, {
	    type: 'line',
	    data: {
	        labels: labels,
	        datasets: [

	        {
	            label: 'all orders',
	            data: allOrders,
	            backgroundColor: backgroudRGB,
	            borderColor: borderRGB,
	            borderWidth: 1,
	             pointRadius: 0,

	        },

	        {
	            label: `mtg Orders: ${mtgCount}`,
	            data: mtgOrders,
	            backgroundColor: 'blue',
	            borderColor: 'blue',
	            borderWidth: 1,
	             pointRadius: 0,
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
	            text: `Last 10,000 orders - Average(${averageOrders}), mtgAverage(${mtgAverageOrders}) across ${numberOfDays} days`,
	            fontSize: 15,
	        }
	    }
	});


	var myChart = new Chart(ctx4, {
	    type: 'line',
	    data: {
	        labels: labels,
	        datasets: [

	        {
	            label: `total cards: ${nonFoilEnglishCount}`,
	            data: nonFoilEnglishOrders,
	            backgroundColor: backgroudRGB,
	            borderColor: 'purple',
	            borderWidth: 1,
	            pointRadius: 0,

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
	            text: `total quantity of mtg cards ordered` ,
	            fontSize: 15,
	        }
	    }
	});
	}
	



</script>//