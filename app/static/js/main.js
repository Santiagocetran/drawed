document.addEventListener('DOMContentLoaded', function() {
    // Get the button element
    const sendArtButton = document.getElementById('send-art-btn');
    
    // Add click event listener
    sendArtButton.addEventListener('click', function() {
        console.log('I\'m Drawed button clicked!');
        // This is just a placeholder for now
        // Later, this will trigger the WebSocket event to send art
    });
});