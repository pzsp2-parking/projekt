import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [username, setUsername] = useState(0);
  const [cars, setCars] = useState(0);

  useEffect(() => {
    fetch('/api/example_client').then(res => res.json()).then(data => {
      setUsername(data.username);
      setCars(data.cars)
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Username: {username}</p>
        <p>Your cars: {cars}</p>
      </header>
    </div>
  );
}

export default App;
