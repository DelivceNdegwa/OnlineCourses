// filename.js
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const host = window.location.host;
const path = "/ws/notifications/";  // Add a leading slash to the path

const socket = new WebSocket(`${protocol}://${host}${path}`);

socket.onopen = (event) => {
    console.log('WebSocket connection opened');
};

socket.onmessage = (event) => {
    let socketdata = JSON.parse(event.data);
    let notification = socketdata.data;

    // console.log(notification);
    alert(notification)
};

socket.onclose = (event) => {
    console.log('WebSocket connection closed');
};
