import React, { useState, useEffect } from 'react';

// Custom function to fetch data from a given endpoint
function fetchData(endpoint, setData, setError, setIsLoading) {
  fetch(endpoint)
    .then((response) => {
      console.log('Response received');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log('Data received:', data);
      setData(data);
    })
    .catch((error) => {
      console.error('Error fetching data:', error);
      setError(error);
    })
    .finally(() => {
      setIsLoading(false);
    });
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Effect: Fetching token and user info...');
    fetchData('/api/user-info', (data) => {
      if (data.access_token) {
        setToken(data.access_token);
      }
      if (data.user_info) {
        setUser(data.user_info);
      }
      setIsAuthenticated(!!(data.access_token || data.user_info));
    }, setError, setIsLoading);
  }, []);

  console.log('Render: isAuthenticated =', isAuthenticated);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!isAuthenticated) {
    return <div><a href="http://localhost:5000">Log in</a></div>;
  }

  return (
    <div>
      {user && (
        <div>
          <h3>User Information:</h3>
          <p>Name: {user.display_name}</p>
          <p>Followers: {user.followers.total}</p>
          <pre>{JSON.stringify(user, null, 2)}</pre>
        </div>
      )}
      {/* protected content goes here */}
    </div>
  );
}

export default App;
