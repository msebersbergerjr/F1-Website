function update_chart(param){
    $.ajax({
        method: 'GET',
        url: 'ajax/driver-chart?' + param,
        success: function(results){
            console.log(results)
            
            // Destroys old chart to make new one
            let chartStatus = Chart.getChart("myChart");
            if (chartStatus != undefined) {
            chartStatus.destroy();
            }

            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: results.labels,
                    datasets: [{
                        label: "Track Speed",
                        backgroundColor: 'blue',
                        data: results.data
                    }]
                },
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                    scales:{
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value, index, ticks){
                                    return results.status
                                }
                            }
                        }
                    }
                }
            })
        },
        
        error: function(){
            console.log('error')
        }
    });
}

function circuit_id_chart(circuit_id){
    let param = 'circuit_id='+ circuit_id
    update_chart(param)
}