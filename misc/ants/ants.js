class Blob {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
    }
}

function random_color() {
    let r = Math.round(Math.random() * 255);
    let g = Math.round(Math.random() * 255);
    let b = Math.round(Math.random() * 255);
    return {
        "r": r,
        "g": g,
        "b": b
    }
}

function random_int(min, max) {
    return Math.round(Math.random() * (max - min) + min)
}

MAP_WIDTH = 1000;
MAP_HEIGHT = 500;
BLOB_SIZE = 10;
blobs = []

document.addEventListener("DOMContentLoaded", (event) => {
    for (let i = 0; i < 100; i++) {
        let x = Math.round(Math.random() * MAP_WIDTH);
        let y = Math.round(Math.random() * MAP_HEIGHT);
        let color = random_color()
        blobs.push(new Blob(x, y, color))
    }

    let canvas = document.getElementById('game-canvas');
    let ctx = canvas.getContext('2d');

    for (let blob of blobs) {
        ctx.fillStyle = `rgb(${blob.color.r}, ${blob.color.g}, ${blob.color.b})`;
        ctx.fillRect(blob.x, blob.y, BLOB_SIZE, BLOB_SIZE);
    }

    let game_loop = setInterval(drawBlobs, 250);
}, false);


function drawBlobs() {
    let canvas = document.getElementById('game-canvas');
    let ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let blob of blobs) {

        blob.x += random_int(-10, 10);
        blob.y += random_int(-10, 10);

        ctx.fillStyle = `rgb(${blob.color.r}, ${blob.color.g}, ${blob.color.b})`;
        ctx.fillRect(blob.x, blob.y, BLOB_SIZE, BLOB_SIZE);
    }
}