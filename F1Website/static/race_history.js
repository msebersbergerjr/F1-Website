function send_request(param) {
    $.ajax({
        method: 'GET',
        url: 'ajax/race-history?' + param,
        beforeSend: function(){
            console.log('before send');
        },
        success: function(results) {
            update_table(results);
            console.log('after send')
        },
        error: function() {
            console.log('error')
        }
    });
}

function all(){
    let param = 'all=True'
    send_request
}

function season(season){
    let param = 'season='+ season
    send_request(param)
}

function circuit_id(circuit_id){
    let param = 'circuit_id='+ circuit_id
    send_request(param)
}

function team_id(team_id){
    let param = 'team_id='+ team_id
    send_request(param)
}

function status(status){
    let param = 'status='+ status
    send_request(param)
}

function update_table(data){
    let row;
    let all_rows = '';

    console.log(data)

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = '<tr><td>' + elem['season'] + '</td>' + '<td>' + elem['round'] + '</td>'  + '<td>' + elem['circuit_id'] + '</td>' + '<td>' + elem['date'] + '</td>' + '<td>' + elem['team_id'] + '</td>' + '<td>' + elem['position'] + '</td>' + '<td>' + elem['points'] + '</td>' + '<td>' + elem['status'] + '</td>' + '<td>' + elem['true_time'] + '</td>' + '</tr>'
        all_rows = all_rows + row;
    });

    $('#myTable tbody').html(all_rows)
}