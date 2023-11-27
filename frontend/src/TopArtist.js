// frontend/src/TopArtist.js

import React, { useEffect, useState } from 'react';

function TopArtist() {
  const [topArtist, setTopArtist] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchTopArtist() {
      try {
        // Update the URL to where your Flask backend is hosted, if necessary
        const response = await fetch('http://localhost:5000/landing');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setTopArtist(data.top_artist);
      } catch (error) {
        console.error('Error fetching top artist:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTopArtist();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Your Top Artist</h1>
      {topArtist ? <p>{topArtist}</p> : <p>No top artist found</p>}
    </div>
  );
}

export default TopArtist;
