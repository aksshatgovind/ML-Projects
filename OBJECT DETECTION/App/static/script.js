document.getElementById('od-button').addEventListener('click', function() {
    // Open the object detection app in a frame
    const frame = document.createElement('iframe');
    frame.src = '/video_feed';  // Updated to use Flask route
    frame.style.width = '100%';
    frame.style.height = '600px';
    frame.style.border = 'none';
    document.querySelector('main').appendChild(frame);
});
