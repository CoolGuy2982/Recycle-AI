//const googleMapsApiKey = "{{ google_maps_api_key }}";
window.onload = function() {
    const data = JSON.parse(sessionStorage.getItem('AIResponse'));
    const analysisResult = document.getElementById('analysis-result');
    if (data) {
        analysisResult.innerHTML = data.result ? formatBoldAndNewLine(data.result) : 'No results found.';
        displayMap(data.locations);
        displayYouTubeVideos(data.videoIDs);
        sessionStorage.removeItem('AIResponse'); // Clean up after displaying
    } else {
        analysisResult.innerHTML = 'No results to display. Please capture an image first.';
    }
};

function formatBoldAndNewLine(text) {
    return text.replace(/\*\*(.*?)\*\*/g, '<br><strong>$1</strong><br>');
}

function displayMap(addresses) {
    const mapContainer = document.getElementById('map-container');
    mapContainer.innerHTML = '';
    addresses.forEach(address => {
        const mapFrame = document.createElement('iframe');
        mapFrame.style.width = '100%';
        mapFrame.style.height = '250px';
        mapFrame.style.borderRadius = '24px';
        mapFrame.style.border = 'none';
        mapFrame.loading = 'lazy';
        mapFrame.allowFullscreen = true;
        mapFrame.src = `https://www.google.com/maps/embed/v1/place?key=${googleMapsApiKey}&q=${encodeURIComponent(address)}`;
        mapContainer.appendChild(mapFrame);
    });
}

function displayYouTubeVideos(videoIDs) {
    const videoContainer = document.getElementById('video-container');
    videoContainer.innerHTML = '';
    videoIDs.forEach(id => {
        const iframeContainer = document.createElement('div');
        iframeContainer.className = 'video-frame-container';
        const iframe = document.createElement('iframe');
        iframe.src = `https://www.youtube.com/embed/${id}`;
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        iframe.allowFullscreen = true;
        iframeContainer.appendChild(iframe);
        videoContainer.appendChild(iframeContainer);
    });
}
