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

    var tbodyRef = document.getElementById('blobs-list').getElementsByTagName('tbody')[0];
    tbodyRef.innerHTML = "";

    blobs.sort((a, b) => a.age < b.age);

    $('#blob-count').text(blobs.length);
    let avg_age = blobs.reduce((acc, blob) => acc + blob.age, 0) / blobs.length;
    $('#blob-avg-age').text(Math.round(avg_age * 100) / 100);
    let avg_energy = blobs.reduce((acc, blob) => acc + blob.energy, 0) / blobs.length;
    $('#blob-avg-energy').text(Math.round(avg_energy * 100) / 100);

    for (let blob of blobs) {
        ctx.fillStyle = blob.color;
        ctx.fillRect(blob.x * BLOB_SIZE, blob.y * BLOB_SIZE, BLOB_SIZE, BLOB_SIZE);

        var newRow = tbodyRef.insertRow();
        var newCell = newRow.insertCell();
        var newDiv = document.createElement("div");
        newDiv.style.backgroundColor = blob.color;
        newDiv.style.width = BLOB_SIZE + "px";
        newDiv.style.height = BLOB_SIZE + "px";
        newCell.appendChild(newDiv);
        var newCell = newRow.insertCell();
        var newText = document.createTextNode(blob.age);
        newCell.appendChild(newText);
        var newCell = newRow.insertCell();
        var newText = document.createTextNode(blob.energy);
        newCell.appendChild(newText);
    }
}