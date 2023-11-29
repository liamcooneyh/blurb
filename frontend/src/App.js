import React, { useState, useEffect } from 'react';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);

  useEffect(() => {
    console.log('Effect: Fetching token...'); // Debug statement

    // Make a GET request to your Flask API to fetch the token
    fetch('/api/get-token')
      .then((response) => {
        console.log('Response received'); // Debug statement
        return response.json();
      })
      .then((data) => {
        console.log('Token data received:', data); // Debug statement

        if (data && data.access_token) {
          console.log('Token received from Flask:', data.access_token); // Debug statement
          // Token received from Flask, store it in local state
          setToken(data.access_token);
          setIsAuthenticated(true);
        }
      })
      .catch((error) => {
        console.error('Error fetching token:', error); // Debug statement
      });
  }, []);

  console.log('Render: isAuthenticated =', isAuthenticated); // Debug statement

  if (!isAuthenticated) {
    return <div>
            <a href="http://localhost:5000">Log in</a>
          </div>;
  }

  // If the user is authenticated, you can show the protected content
  return (
    <div>
      <h1>Testing changes</h1>
      {/* Your protected content goes here */}
    </div>
  );
}

export default App;
