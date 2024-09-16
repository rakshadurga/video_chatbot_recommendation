document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('video');
    const resultDiv = document.getElementById('result');
    const speakButton = document.getElementById('speakButton');

    // Access the webcam video stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoElement.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing webcam: ", err);
        });

    // Handle button click for song recommendation
    speakButton.addEventListener('click', () => {
        resultDiv.textContent = "Listening for genre...";
        
        fetch('/get_recommendation')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `Recommended Song: <strong>${data.song}</strong> by ${data.artist} <br> <a href="${data.url}" target="_blank">Listen on Spotify</a>`;
                } else {
                    resultDiv.textContent = "No recommendation available.";
                }
            })
            .catch(error => {
                console.error("Error fetching recommendation: ", error);
                resultDiv.textContent = "An error occurred.";
            });
    });
});
