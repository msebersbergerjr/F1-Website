$(document).ready(function(){
    console.log('Initial Load')
    team_lineup('season=2021')
    team_points_season_chart('season=2021')
})

function season_dropdown(season){

    var url = 'http://127.0.0.1:8000/teams/'+season
    //window.location = url

    document.getElementById("season_dropdown").selectedIndex = 0
    let param = 'season='+ season
    team_lineup(param)
    team_points_season_chart(param)
}

function team_lineup(param){
    $.ajax({
        method: 'GET',
        url: 'ajax/teams-page?' + param,
        success: function(results){
            console.log('Teams Page')
            console.log(results)
            $('#season-header').html(results['year'] + ' TEAMS')
            let all = ''
            for(team in results['teams']){
                // console.log(results['teams'][team]['team_name'])
                // console.log(results['teams'][team]['points'])
                a_tag = '<a href="'+results['teams'][team]['team_id']+'">'
                card = '<div class="card" id="'+results['teams'][team]['team_id']+'">'
                card_body = '<div class="card-body row">'
                card_col = '<div class="col-12 card-title">'
                card_pos = '<div class="card-position">' + results['teams'][team]['points'] + '<span class="card-name">'+results['teams'][team]['team_name']+'</span>'

                all = all + a_tag + card + card_body + card_col + card_pos

                for(driver in results['teams'][team]['drivers']){
                    // console.log(results['teams'][team]['drivers'][driver]['givenName'])
                    card_driver = '<span class="card-name">'+results['teams'][team]['drivers'][driver]['givenName'] + ' ' + results['teams'][team]['drivers'][driver]['familyName']+'</span>'
                    all = all  + card_driver
                }
                end = '</div> </div> </div> </div> </a>'

                all = all + end
            }
            $('#teams-page').html(all)
        }
    })
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