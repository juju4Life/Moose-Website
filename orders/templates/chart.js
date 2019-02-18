
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
	var releaseEvents = ''
	var banListUpdate = ''
	var tcgPlayerKickback = ''
	var special = ''
	var pieChart = []
	var pieChart2 = []
	var sumEnglishPrice = ''
	var sumForeignPrice = ''
	var sumFoilForeignPrice = ''
	var sumFoilEnglishPrice = ''
	var boxesPrice = ''
	var sumMtgPrice = ''
	var sumYgoPrice = ''
	var sumPokemonPrice = ''
	var sumDbsPrice = ''
	var sumFowPrice = ''
	var sumDeckBoxesPrice = ''
	var sumCardSleevesPrice = ''
	var sumSuppliesPrice = ''
	var sumFunkoPrice = ''
	var gross = ''
	var refunds = ''
	var sumOtherPrice = ''
	var mtgSinglesTotal = ''
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
            releaseEvents = data.release_events;
            banListUpdate = data.ban_list_update;
            tcgPlayerKickback = data.tcg_player_kickback;
            special = data.special;
            pieChart = data.pie_chart;
            pieChart2 = data.pie_chart_2;
            sumEnglishPrice = data.sum_english_price;
            sumForeignPrice = data.sum_foreign_price;
            sumFoilForeignPrice = data.sum_foreign_foil_price;
            sumFoilEnglishPrice = data.sum_english_foil_price;
            sumBoxesPrice = data.sum_boxes_price;
            sumMtgPrice = data.sum_mtg_price;
            sumYgoPrice = data.sum_ygo_price;
            sumPokemonPrice = data.sum_pokemon_price;
            sumDbsPrice = data.sum_dbs_price;
            sumFowPrice = data.sum_fow_price;
            sumDeckBoxesPrice = data.sum_deckboxes_price;
            sumCardSleevesPrice = data.sum_card_sleeves_price;
            sumSuppliesPrice = data.sum_supplies_price;
            sumFunkoPrice = data.sum_funko_price;
            gross = data.gross;
            refunds = data.refunds;
            sumOtherPrice = data.sum_other_price;
            mtgSinglesTotal = nonFoilEnglishCount + foilEnglishCount + nonFoilForeignCount + foilForeignCount
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
	var ctx5 = document.getElementById("myChart5").getContext('2d');
	var ctx6 = document.getElementById("myChart6").getContext('2d');

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

	        {
	            label: 'release events',
	            data: releaseEvents,
	            backgroundColor: 'green',
	            borderColor: 'green',
	            borderWidth: 1,
	             type: 'scatter',
	        },

	        {
	            label: 'ban-list updates',
	            data: banListUpdate,
	            backgroundColor: 'red',
	            borderColor: 'red',
	            borderWidth: 1,
	             type: 'scatter',
	        },

	        {
	            label: 'tcgplayer kickback',
	            data: tcgPlayerKickback,
	            backgroundColor: 'purple',
	            borderColor: 'purple',
	            borderWidth: 1,
	             type: 'scatter',
	        },

	        {
	            label: 'special',
	            data: special,
	            backgroundColor: 'lightblue',
	            borderColor: 'lightblue',
	            borderWidth: 1,
	             type: 'scatter',
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
	            label: `${mtgSinglesTotal} total cards`,
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
	            text: `Last 10,000 mtg orders - average of ${(mtgSinglesTotal / 10000).toFixed(1)} cards per order` ,
	            fontSize: 15,
	        }
	    }
	});

	var myChart = new Chart(ctx5, {
	    type: 'pie',
	    data: {
	        labels: [
	            `mtg ${sumMtgPrice} | ${pieChart[0]}%`,
	            `pokemon ${sumPokemonPrice} | ${pieChart[1]}%`,
	            `yugioh ${sumYgoPrice} | ${pieChart[2]}%`,
	            `dbs ${sumDbsPrice} | ${pieChart[3]}%`,
	            `fow ${sumFowPrice} | ${pieChart[4]}%`,
	            `deckboxes ${sumDeckBoxesPrice} | ${pieChart[5]}%`,
	            `card sleeves ${sumCardSleevesPrice} | ${pieChart[6]}%`,
	            `supplies ${sumSuppliesPrice} | ${pieChart[7]}%`,
	            `funko ${sumFunkoPrice} | ${pieChart[8]}%`,

	        ],
	        datasets: [
                {
                    data: pieChart,
                    backgroundColor: ['green', 'blue', 'purple', 'red', 'orange', 'pink', 'yellow', 'lightblue', 'maroon'],
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
	            text: `Last 10,000 orders - total sales $${gross}` ,
	            fontSize: 15,
	        },

	        animation: {animateScale: true}
	    }
	});


	var myChart = new Chart(ctx6, {
	    type: 'pie',
	    data: {
	        labels: [
	            `non-foil english ${sumEnglishPrice} | ${pieChart2[0]}%`,
	            `foil english ${sumFoilEnglishPrice} | ${pieChart2[1]}%`,
	            `non-foil foreign ${sumForeignPrice} | ${pieChart2[2]}%`,
	            `foil foreign ${sumFoilForeignPrice} | ${pieChart2[3]}%`,
	            `Booster Boxes ${sumBoxesPrice} | ${pieChart2[4]}%`,
	            `Other -${sumOtherPrice} | ${pieChart2[5]}%`,

	        ],
	        datasets: [
                {
                    data: pieChart2,
                    backgroundColor: ['blue', 'purple', 'yellow', 'red', 'orange', 'black',],
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
	            text: `Last 10,000 mtg orders - total: ${sumMtgPrice} (Refunds -${refunds})` ,
	            fontSize: 15,
	        },

	        animation: {animateScale: true}
	    }
	});
	}
	



</script>//