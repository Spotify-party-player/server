var running = false;
const urlParams = new URLSearchParams(window.location.search);
const roomId = urlParams.get('tag');

function search() {
    if (running) {
        return;
    }
    running = true;
    let name = $('#mainSearchBar').val();
    $.ajax({
        type: "get",
        url: "/tracks/" + name,
        success: function(response) {
            console.log(response);
            const html = `
            <tr>
                <th>${response.keys[1]}</th>
                <th>${response.keys[2]}</th>
            </tr>
            ${response.tracks.map(x => `
                <tr>
                <td>${x[1]}</td>
                <td>${x[2]}</td>
                <td onClick="addTrack('${x[0]}');">Add</td>
                </tr>
            `)}
            `
            $("#searchTable").html(html);
        },
        complete: function(r) {
            running = false;
        }
    });
}

function addTrack(trackId) {
    $.ajax({
        type: "post",
        url: "/room/" + roomId + "/track/" + trackId,
        success: function(response) {
            console.log(response);
        }
    });
    // socket.emit("add_song", {roomId, trackId});
}

var socket = io("/sockets");
socket.on('connected', function() {
    // socket.emit('my event', {data: 'I\'m connected!'});
    socket.emit('join', {roomId});
    console.log("kek");
});

socket.on('get_active', function(msg) {
    socket.emit('active', {roomId});
});

socket.on('update_list', function(response) {
    console.log(response);
    console.log(response.tracks[0][0]==response.currentlyPlaying)
    const html = `
    <tr>
        <th>${response.keys[1]}</th>
        <th>${response.keys[2]}</th>
        <th>${response.keys[3]}</th>
    </tr>
    ${response.tracks.map(x =>
        `
        <tr>
        ${x[0]!=response.currentlyPlaying ?
        `<td>${x[1]}</td>
        <td>${x[2]}</td>
        <td>${x[3]}</td>
        <td><strong><a onclick="playAsNext();">Next</a> (${response.skipCount}/${response.connectedCount})</strong></td>` :
        `<td> <strong>${x[1]}</strong></td>
        <td><strong>${x[2]}</strong></td>
        <td><strong>${x[3]}</strong></td>
        <td><strong><a onclick="skip();">Skip</a> (${response.skipCount}/${response.connectedCount})</strong></td>`}
        </tr>
        `)}
    `
    $("#playlistTable").html(html);
});

function skip() {
    socket.emit("skip", {roomId});
}
