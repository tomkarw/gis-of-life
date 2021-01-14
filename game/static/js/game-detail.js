class Blob {
    constructor(x, y, color, age, energy) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.age = age;
        this.energy = energy;
    }
}

BLOB_SIZE = 10;
FRAME_URL = "http://127.0.0.1:8000/game/bbe04d48-6a57-48ce-a5e3-a1a0ffc43374/frame/"
FRAME_RATE = 1000;

document.addEventListener("DOMContentLoaded", (event) => {
    setInterval(processFrame, FRAME_RATE);
}, false);

function processFrame() {
    $.ajax({
        type: "GET",
        url: FRAME_URL,
        success: function (res) {
            drawFrame(res);
        }.bind(this),
        error: function (xhr, status, err) {
            console.error(xhr, status, err.toString());
        }.bind(this),
        async: false
    });
}

function drawFrame(data) {
    console.log(data.blobs)

    let canvas = document.getElementById('game-canvas');
    let ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // TODO: draw map

    for (let blob of data.blobs) {
        console.log(blob)
        ctx.fillStyle = blob.color;
        ctx.fillRect(blob.x, blob.y, BLOB_SIZE, BLOB_SIZE);
    }
}