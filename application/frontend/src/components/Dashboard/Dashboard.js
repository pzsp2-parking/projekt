import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

import './Dashboard.css';

function details(vin, navigate) {
  navigate("/details", {state: {vin: vin}})
}

function leave(token, cars, index, setClientData) {
  axios({
    method: "POST",
    url:"/api/leave",
    headers: {
      Authorization: 'Bearer ' + token
    },
    data:{
      vin: cars[index].vin
    }
  }).then(() => {
    cars[index].parked = !cars[index].parked
    setClientData(prevNote => ({
      ...prevNote, cars: cars
    }))
  }).catch((error) => {
    if (error.response) {
      console.log(error.response)
      console.log(error.response.status)
      console.log(error.response.headers)
    }
  })
}

function park(vin, navigate) {
  navigate("/park", {state: {vin: vin}})
}

const CarTable = (props) => {
  const positions = props.cars.map((car, index) => {
    return (
      <tr>
        <td>{car.reg_no}</td>
        <td>{car.brand}</td>
        <td>{car.model}</td>
        <td>{car.parked ? 'Yes' : 'No'}</td>
        <td>{car.parked &&
          <button type="button" class="btn btn-link" onClick={() => details(car.vin, props.navigate)}>Details</button>}
        </td>
        <td>{car.parked ?
          (<button type="button" class="btn btn-danger" onClick={() => leave(props.token, props.cars, index, props.setClientData)}>Leave</button>)
          :(<button type="button" class="btn btn-success" onClick={() => park(car.vin, props.navigate)}>Park</button>)}
        </td>
      </tr>
    )
  })
  return (
    <table class="table">
      <thead>
        <tr>
          <th>Registration nr</th>
          <th>Brand</th>
          <th>Model</th>
          <th>Parked</th>
          <th>Details</th>
          <th>Change</th>
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
  }, [props]);

  return (
    <div className='Dashboard'>
      {clientData &&
        <div>
          <CarTable cars={clientData.cars} token={props.token} navigate={navigate} setClientData={setClientData} />
        </div>
      }
      <button type="button" class="btn btn-success" onClick={addCar}>Add car</button>
    </div>
  );
}
