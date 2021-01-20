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
FRAME_RATE = 250;

document.addEventListener("DOMContentLoaded", (event) => {
    setInterval(processFrame, FRAME_RATE);
}, false);

function processFrame() {
    $.ajax({
        type: "GET",
        url: `http://127.0.0.1:8000/game/${token}/frame/`,
        success: function (res) {
            drawFrame(res);
        }.bind(this),
        error: function (xhr, status, err) {
            console.error(xhr, status, err.toString());
        }.bind(this),
        async: false
    });
}

function drawFrame(blobs) {

    let canvas = document.getElementById('game-canvas');
    let ctx = canvas.getContext('2d');

    let img = document.getElementById("game-img");
    ctx.drawImage(img, 0, 0, width * BLOB_SIZE, height * BLOB_SIZE);

    for (let blob of blobs) {
        ctx.fillStyle = blob.color;
        ctx.fillRect(blob.x * BLOB_SIZE, blob.y * BLOB_SIZE, BLOB_SIZE, BLOB_SIZE);
    }
}