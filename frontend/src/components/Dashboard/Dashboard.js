import React, { useEffect, useState } from 'react';
import axios from 'axios';

import './Dashboard.css';

const CarList = (props) => {
  const positions = props.cars.map(car => {
    return <li>{car}</li>
  })
  return <ol>{positions}</ol>
}

export default function Dashboard(props) {
  const [clientData, setClientData] = useState(null)

  useEffect(() => {
    axios({
      method: "GET",
      url:"/api/example_client",
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
          <CarList cars={clientData.cars} />
        </div>
      }
    </div>
  );
}
