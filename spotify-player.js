// spotify-player.js

// Initialize the Spotify player
window.onSpotifyWebPlaybackSDKReady = () => {
    const token = accessToken; // Replace with the user's access token
    
    const player = new Spotify.Player({
        name: 'Playlist Generator',
        getOAuthToken: cb => { cb(token); }
    });
    
    // Error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });
    
    // Playback status updates
    player.addListener('player_state_changed', state => { console.log(state); });
    
    // Ready
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
        
        // Set the Spotify player to your specified div element
        const playerDiv = document.getElementById('spotify-player');
        playerDiv.appendChild(player._options.getContainer());
        
        // Play a track (optional)
        player.play({ uris: ['spotify:track:TRACK_URI'] });
    });
    
    // Connect to the Spotify player
    player.connect().then(success => {
        if (success) {
            console.log('Connected to Spotify player');
        }
    });
};
