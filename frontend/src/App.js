import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Add isLoading state
  const [recentlyPlayed, setRecentlyPlayed] = useState([])

  useEffect(() => {
    const api_url = (`${API_BASE_URL}/v1/api/get-token`);

    fetch(api_url)
      .then(response => response.json())
      .then(data => {
        const accessToken = data.access_token;
        setToken(accessToken);
        console.log('Access Token: ', accessToken);

        setIsAuthenticated(true);
        return accessToken;
      });
    }, []); 

  
    // useEffect(() => {
    //   const api_url = (`${API_BASE_URL}/v1/api/recently-played`);
      
    //   fetch(api_url)
    //     .then(response => response.json());
    //     console.log(response);
    // }, []);
  

  if (!isAuthenticated) {
    return <div><a href="http://localhost:5000">Log in</a></div>;
  };

  return (
    <div>
      {user && (
        <div>
          <h1>Authenticated</h1>
        </div>
      )}
    </div>
  );
}

export default App;