function send_request(param) {
    $.ajax({
        method: 'GET',
        url: 'ajax/race-history?' + param,
        success: function(results) {
            update_table(results);
            console.log('Successful')
        },
        error: function() {
            console.log('error')
        }
    });
}

function resetSelect(keep){
    if (keep == 1){
        document.getElementById("Circuit").selectedIndex = 0
        document.getElementById("Constructor").selectedIndex = 0
        document.getElementById("Status").selectedIndex = 0
    }
    else if (keep == 2){
        document.getElementById("Season").selectedIndex = 0
        document.getElementById("Constructor").selectedIndex = 0
        document.getElementById("Status").selectedIndex = 0
    }
    else if (keep == 3){
        document.getElementById("Season").selectedIndex = 0
        document.getElementById("Circuit").selectedIndex = 0
        document.getElementById("Status").selectedIndex = 0
    }
    else if (keep == 4) {
        document.getElementById("Season").selectedIndex = 0
        document.getElementById("Circuit").selectedIndex = 0
        document.getElementById("Constructor").selectedIndex = 0
    }
}

function season(season){
    resetSelect(1)
    let param = 'season='+ season
    send_request(param)
}

function circuit_id(circuit_id){
    resetSelect('2')
    let param = 'circuit_id='+ circuit_id
    send_request(param)
}

function team_id(team_id){
    resetSelect('3')
    let param = 'team_id='+ team_id
    send_request(param)
}

function status(status){
    resetSelect('4')
    let param = 'status='+ status
    send_request(param)
}

function update_table(data){
    let row;
    let all_rows = '';

    // console.log(data)

    Object.keys(data).forEach(key => {
        console.log(data[key])
        elem = data[key];
        row = '<tr><td>' + elem['season'] + '</td>' + '<td>' + elem['round'] + '</td>'  + '<td>' + elem['circuit_id'] + '</td>' + '<td>' + elem['date'] + '</td>' + '<td>' + elem['team_id'] + '</td>' + '<td>' + elem['position'] + '</td>' + '<td>' + elem['points'] + '</td>' + '<td>' + elem['status'] + '</td>' + '</tr>'
        all_rows = all_rows + row;
    });

    $('#myTable tbody').html(all_rows)
}