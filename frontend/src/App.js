import React, { useState, useEffect } from 'react';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // eslint-disable-next-line
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Add isLoading state

  useEffect(() => {
    console.log('Effect: Fetching token and user info...');

    // Make a GET request to your Flask API to fetch the token and user info
    fetch('/api/user-info')
      .then((response) => {
        console.log('Response received');
        return response.json();
      })
      .then((data) => {
        console.log('Data received:', data);

        if (data && data.access_token) {
          console.log('Token received from Flask:', data.access_token);
          // Token received from Flask, store it in local state
          setToken(data.access_token);
        }

        if (data && data.user_info) {
          console.log('User info received:', data.user_info);
          // User info received from Flask, store it in local state
          setUser(data.user_info);
        }

        // Set isAuthenticated to true if either token or user_info is available
        if (data && (data.access_token || data.user_info)) {
          setIsAuthenticated(true);
        }

        // Set isLoading to false when authentication data is received
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setIsLoading(false); // Handle loading state even on error
      });
  }, []);

  console.log('Render: isAuthenticated =', isAuthenticated);

  if (isLoading) {
    // Render loading spinner or progress bar while data is being fetched
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return (
      <div>
        <a href="http://localhost:5000">Log in</a>
      </div>
    );
  }

  // If the user is authenticated and user information is available, you can display it
  return (
    <div>
      {user && (
        <div>
          <h3>User Information:</h3>
          <p>Name: {user.display_name}</p>
          <p>Email: {user.email}</p>
        </div>
      )}
      {/* protected content goes here */}
    </div>
  );
}

export default App;
