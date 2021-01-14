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
FRAME_RATE = 1000;

document.addEventListener("DOMContentLoaded", (event) => {
    setInterval(processFrame, FRAME_RATE);
}, false);

function processFrame() {
    console.log(`http://127.0.0.1:8000/game/${token}/frame/`)
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

function drawFrame(data) {

    let canvas = document.getElementById('game-canvas');
    let ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // TODO: draw map
    console.log(data.map)
    for (let y = 0; y < data.map.length; y++) {
        for (let x = 0; x < data.map.length; x++) {
            switch (data.map[y][x]) {
                case -1:
                    ctx.fillStyle = 'rgb(0, 0, 100)';
                    break;
                case 0.5:
                    ctx.fillStyle = 'rgb(0, 0, 0)';
                    break;
                case 1:
                    ctx.fillStyle = 'rgb(0, 100, 0)';
                    break;
            }

            ctx.fillRect(x * BLOB_SIZE, y * BLOB_SIZE, BLOB_SIZE, BLOB_SIZE);
        }
    }

    for (let blob of data.blobs) {
        ctx.fillStyle = blob.color;
        ctx.fillRect(blob.x * BLOB_SIZE, blob.y * BLOB_SIZE, BLOB_SIZE, BLOB_SIZE);
    }
}