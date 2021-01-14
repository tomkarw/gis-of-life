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
FRAME_URL = "http://127.0.0.1:8000/game/796b6367-99f6-4a2c-9a8f-85e42bd8df3a/frame/"

document.addEventListener("DOMContentLoaded", (event) => {
    let game_loop = setInterval(processFrame, 250);
}, false);

function processFrame() {
    let crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

    console.log(crf_token);

    $.ajax({
        type: "GET",
        url: FRAME_URL,
        success: function (res) {
            drawFrame(res);
        }.bind(this),
        error: function (xhr, status, err) {
            alert("Error: Something went wrong.");
            console.error(xhr, status, err.toString());
        }.bind(this),
        async: false
    });
}

function drawFrame(data) {
    let canvas = document.getElementById('game-canvas');
    let ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw map

    for (let blob of data.blobs) {
        ctx.fillStyle = blob.color;
        ctx.fillRect(blob.x, blob.y, BLOB_SIZE, BLOB_SIZE); // TODO: blob.x * BLOB_SIZE
    }
}