import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

// const CarList = (props) => {
//   const positions = props.cars.map(function (car) {
//     <li>{car}</li>
//   })
//   return <ol>{positions}</ol>
// }

function App() {
  const [username, setUsername] = useState(0);
  const [cars, setCars] = useState([]);

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
        <p>Your cars:</p>
        <ol>
          {
            cars.map(car => {
              return <li>{car}</li>
            })
          }
        </ol>
      </header>
    </div>
  );
}

export default App;
