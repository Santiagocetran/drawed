document.addEventListener('DOMContentLoaded', function() {
    // Socket.io connection
    const socket = io();
    
    // DOM elements
    const sendArtButton = document.getElementById('send-art-btn');
    const messagesContainer = document.querySelector('.messages-container');
    
    // Connect to socket.io
    socket.on('connect', function() {
        console.log('Connected to server');
    });
    
    // Handle connection errors
    socket.on('connect_error', function(error) {
        console.error('Connection error:', error);
    });
    
    // Handle status messages from server
    socket.on('status', function(data) {
        console.log('Status:', data.message);
    });
    
    // Handle error messages from server
    socket.on('error', function(data) {
        console.error('Server error:', data.message);
        // You might want to display this to the user
    });
    
    // Handle new artwork messages
    socket.on('new_art', function(data) {
        console.log('New artwork received:', data);
        
        // Create a new message element
        const messageEl = document.createElement('div');
        messageEl.className = 'art-message';
        messageEl.dataset.messageId = data.message_id;
        
        // Create artwork container
        const artworkEl = document.createElement('div');
        artworkEl.className = 'artwork-container';
        
        // Create image element
        const imgEl = document.createElement('img');
        imgEl.src = data.artwork.file_path;
        imgEl.alt = data.artwork.title;
        imgEl.className = 'artwork-image';
        
        // Create title element
        const titleEl = document.createElement('div');
        titleEl.className = 'artwork-title';
        titleEl.textContent = data.artwork.title;
        
        // Create user info element
        const userEl = document.createElement('div');
        userEl.className = 'message-user-info';
        userEl.textContent = `Shared by ${data.display_name}`;
        
        // Create timestamp element
        const timeEl = document.createElement('div');
        timeEl.className = 'message-timestamp';
        const messageDate = new Date(data.timestamp);
        timeEl.textContent = messageDate.toLocaleTimeString();
        
        // Assemble the message
        artworkEl.appendChild(imgEl);
        artworkEl.appendChild(titleEl);
        messageEl.appendChild(artworkEl);
        messageEl.appendChild(userEl);
        messageEl.appendChild(timeEl);
        
        // Add to the messages container
        messagesContainer.appendChild(messageEl);
        
        // Scroll to the bottom of the messages container
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Mark this message as seen
        socket.emit('mark_seen', { message_id: data.message_id });
    });
    
    // Add click event listener to the "I'm Drawed" button
    sendArtButton.addEventListener('click', function() {
        console.log('I\'m Drawed button clicked');
        
        // Disable button temporarily to prevent spam
        sendArtButton.disabled = true;
        
        // Add visual feedback that the button is clicked
        sendArtButton.classList.add('clicked');
        
        // Send websocket event to get random artwork
        socket.emit('send_art', {});
        
        // Re-enable button after a delay
        setTimeout(function() {
            sendArtButton.disabled = false;
            sendArtButton.classList.remove('clicked');
        }, 2000); // 2 second delay
    });
});