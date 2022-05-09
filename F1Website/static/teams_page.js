function season_dropdown(season){

    var url = 'http://127.0.0.1:8000/teams/'+season
    //window.location = url

    document.getElementById("season_dropdown").selectedIndex = 0
    let param = 'season='+ season
    team_points_season_chart(param)
}

function team_points_season_chart(param){
    $.ajax({
        method: 'GET',
        url: 'ajax/team-points-season-chart?' + param,
        success: function(results){
            console.log('Season Chart')
            console.log(results)
            
            // Destroys old chart to make new one
            let chartStatus = Chart.getChart("seasonChart");
            if (chartStatus != undefined) {
            chartStatus.destroy();
            }

            const ctx = document.getElementById('seasonChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: results.labels,
                    datasets: [{
                        label: "Points",
                        backgroundColor: 'blue',
                        data: results.data
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                }
            })
            
            console.log('Successful')
        },
        error: function(){
            console.log('Error')
        }
    })
}