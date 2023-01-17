import { useState, useEffect } from 'react';
import axios from 'axios';

import MapGrid from './ParkMap/ParkMap';

function EmpPage(props) {

  const [carpark, setCarpark] = useState()
	const [parkMap, setParkMap] = useState()
  const [parkedCars, setParkedCars] = useState([])

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

      {parkMap &&
        <MapGrid parkMap={parkMap} />
      }
    </div>
  )
}

export default EmpPage;