        let currentCamera = 'environment'; // Default to back camera
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const photoButton = document.getElementById('photoButton');
        const uploadButton = document.getElementById('uploadButton');
        const loadingAnimation = document.getElementById('loadingAnimation');
        const staticImage = document.getElementById('staticImage');
        const context = canvas.getContext('2d');
        let stream = null;
        let imageCapture = null;

        function getCameraStream() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            navigator.mediaDevices.getUserMedia({ video: { facingMode: currentCamera } })
                .then(function(s) {
                    stream = s;
                    video.srcObject = stream;
                    video.play();
                    const track = stream.getVideoTracks()[0];
                    imageCapture = new ImageCapture(track);
                }).catch(function(error) {
                    console.log("Error accessing camera: ", error);
                });
        }

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            getCameraStream();
        }

        function switchCamera() {
            currentCamera = (currentCamera === 'user') ? 'environment' : 'user';
            getCameraStream();
        }

        function toggleFlash() {
            if (!imageCapture) {
                console.log('No image capture support');
                return;
            }
            imageCapture.getPhotoCapabilities().then(function(capabilities) {
                if (capabilities.fillLightMode.includes('flash')) {
                    const settings = { fillLightMode: 'flash' };
                    imageCapture.takePhoto({photoSettings: settings}).then(blob => {
                        console.log('Flash activated and photo taken');
                    }).catch(error => console.error('Error taking photo with flash:', error));
                }
            });
        }

        photoButton.addEventListener('click', function() {
            captureImageAndSend();
        });

        function captureImageAndSend() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            photoButton.style.animation = 'none';
            const imageData = canvas.toDataURL('image/jpeg');
            sessionStorage.setItem('capturedImage', imageData); // Store captured image data
            displayImage(imageData);
            sendImageToServer(imageData);
        }

        function handleImageUpload(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageData = e.target.result;
                sessionStorage.setItem('capturedImage', imageData); // Store captured image data
                displayImage(imageData);
                sendImageToServer(imageData);
            };
            reader.readAsDataURL(file);
        }

        function sendImageToServer(imageData) {
            loadingAnimation.style.display = 'block'; // Show the loading animation
            fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData.split(',')[1] })  // Send only the base64 part
            })
            .then(response => response.json())
            .then(data => {
                sessionStorage.setItem('AIResponse', JSON.stringify(data));
                window.location.href = '/scan';  // Redirect to scan.html
            })
            .catch(err => {
                console.error('Error sending image:', err);
                loadingAnimation.style.display = 'none';  // Hide the loading animation on error
            });
        }

        function displayImage(dataUrl) {
            staticImage.src = dataUrl;
            staticImage.style.display = 'block';
            video.style.display = 'none'; // Turn off the camera
            if (stream) {
                stream.getTracks().forEach(track => track.stop()); // Stop the video stream
            }
        }

        function closePopup() {
            const popup = document.getElementById('popup');
            popup.style.display = 'none';
        }

        document.addEventListener('DOMContentLoaded', function () {
            const popup = document.getElementById('popup');
            if (!localStorage.getItem('popupShown')) {
                popup.style.display = 'block';
                localStorage.setItem('popupShown', 'true');
            }
        });