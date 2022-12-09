import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

import './Dashboard.css';

// TODO: Add functions for parking

function details(event) {

}

function leave(event) {

}

function park(event) {

}

const CarTable = (props) => {
  const positions = props.cars.map(car => {
    return (
      <tr>
        <td>{car.reg_no}</td>
        <td>{car.brand}</td>
        <td>{car.model}</td>
        <td>{car.parked ? 'Yes' : 'No'}</td>
        <td>{car.parked &&
          <button type="button" class="btn btn-link" onClick={details}>Details</button>}
        </td>
        <td>{car.parked ?
          (<button type="button" class="btn btn-danger" onClick={leave}>Leave</button>)
          :(<button type="button" class="btn btn-success" onClick={park}>Park</button>)}
        </td>
      </tr>
    )
  })
  return (
    <table class="table>">
      <thead>
        <tr>
          <th style={{width: '30%'}}>Registration nr</th>
          <th style={{width: '15%'}}>Brand</th>
          <th style={{width: '15%'}}>Model</th>
          <th style={{width: '15%'}}>Parked</th>
          <th style={{width: '15%'}}>Details</th>
          <th style={{width: '20%'}}>Change</th>
        </tr>
      </thead>
      <tbody>{positions}</tbody>
    </table>
  )
}

export default function Dashboard(props) {

  const navigate = useNavigate();

  const [clientData, setClientData] = useState(null)

  function addCar(event) {
    navigate("/addCar");
  }

  useEffect(() => {
    axios({
      method: "GET",
      url:"/api/client_data",
      headers: {
        Authorization: 'Bearer ' + props.token
      }
    })
    .then((response) => {
      const res =response.data
      res.access_token && props.setToken(res.access_token)
      setClientData(({
        username: res.username,
        cars: res.cars}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })
  }, []);

  return (
    <div className='Dashboard'>
      {clientData &&
        <div>
          <p>Username: {clientData.username}</p>
          <p>Your cars:</p>
          <CarTable cars={clientData.cars} />
        </div>
      }
      <button type="button" class="btn btn-success" onClick={addCar}>Add car</button>
    </div>
  );
}
