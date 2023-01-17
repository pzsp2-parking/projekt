import { useState, useEffect } from 'react';
import axios from 'axios';

import MapGrid from './ParkMap/ParkMap';
import ChargeChart from './ChargeChart';

function getDetails(vin, token, setSelectedCar) {
  axios({
    method: "POST",
    url:`/api/getCurrCharging`,
    headers: {
      Authorization: 'Bearer ' + token
    },
    data:{
      vin: vin
    }
  })
    .then(response => {
      setSelectedCar({
        currCharging: response.data.currCharging,
        leaveDatetime: response.data.leaveDatetime
      })
    }).catch((error) => {
    if (error.response) {
      console.log(error.response)
      console.log(error.response.status)
      console.log(error.response.headers)
    }
  })
}

const CarTable = (props) => {
  const positions = props.cars.map((car, index) => {
    return (
      <tr>
        <td>{car.reg_no}</td>
        <td>{car.brand}</td>
        <td>{car.model}</td>
        <td><button type="button" class="btn btn-light" onClick={() => getDetails(car.vin, props.token, props.setSelectedCar)}>Charging details</button>
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
          <th>Details</th>
        </tr>
      </thead>
      <tbody>{positions}</tbody>
    </table>
  )
}

function EmpPage(props) {

  const [carpark, setCarpark] = useState()
	const [parkMap, setParkMap] = useState()
  const [parkedCars, setParkedCars] = useState([])
  const [selectedCar, setSelectedCar] = useState({
    currCharging: [],
    leaveDatetime: Date.now()
  })

  useEffect(() => {
    axios({
      method: "POST",
      url:`/api/empData`,
			headers: {
        Authorization: 'Bearer ' + props.token
      }
    })
      .then(response => {
        setCarpark(
					response.data.parkAddress
        )
        setParkMap(
          response.data.parkMap
        )
        setParkedCars(
          response.data.cars
        )
      }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })
  }, [props.token]);

  return(
    <div>
      {carpark &&
        <h2>Parking: {carpark}</h2>
      }
      <button type="button" class="btn btn-link">Charging and income data (Grafana)</button>

      {parkMap &&
        <div style={{display: 'block', marginLeft: 'auto', marginRight: 'auto', width: '25%'}}>
          <MapGrid parkMap={parkMap} />
        </div>
      }

      <p />

      {selectedCar.currCharging.length > 0 &&
        <div style={{display: 'block', marginLeft: 'auto', marginRight: 'auto', width: '40%'}}>
          Parked: {selectedCar.currCharging[0].x} <br />
          Planned charging until: {selectedCar.leaveDatetime}<br />
          Charged from {selectedCar.currCharging[0].y}% to {selectedCar.currCharging.at(-1).y}%
          <ChargeChart chargeData={selectedCar.currCharging} />
        </div>
      }

      <div>
        <CarTable cars={parkedCars} token={props.token} setSelectedCar={setSelectedCar} />
      </div>
    </div>
  )
}

export default EmpPage;