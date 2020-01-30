function createRoom() {
    window.location.href = "/signin";
}

function joinRoom() {
    let id = $("#mainSearchBar").val();
    window.location.href = "/room?tag=" + id;
}
