import { React, useState, useEffect } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import axios from 'axios';
import DateTimePicker from 'react-datetime-picker';

import ChargeChart from './ChargeChart'


function CarDetails(props) {

  const navigate = useNavigate();
	const {state} = useLocation();

  const [newDate, setNewDate] = useState({
    leaveDate: new Date(Date.now() + 8 * (60 * 60 * 1000))
  })

  const [currCharging, setCurrCharging] = useState([{x: Date.now(), y: 50}])
  const [history, setHistory] = useState(null)
  const [histElem, setHistElem] = useState(0)

  const getCurrCharging = () => {
    axios({
      method: "POST",
      url:`/api/getCurrCharging`,
			headers: {
        Authorization: 'Bearer ' + props.token
      },
      data:{
        vin: state.vin
      }
    })
      .then(response => {
        setCurrCharging(
          response.data.currCharging)
      }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })
  }

  useEffect(() => {
    axios({
      method: "POST",
      url:`/api/getDetails`,
			headers: {
        Authorization: 'Bearer ' + props.token
      },
      data:{
        vin: state.vin
      }
    })
      .then(response => {
        setNewDate({
					leaveDate: new Date(response.data.leaveDate)})
        setCurrCharging(
          response.data.currCharging)
        setHistory(
          response.data.history)
      }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })
  }, [props, state.vin]);

  function changeLeaveDate(event) {
    axios({
      method: "POST",
      url:"/api/changeLeaveDate",
      headers: {
        Authorization: 'Bearer ' + props.token
      },
      data:{
        vin: state.vin,
        leaveDate: (newDate.leaveDate).toISOString()
      }
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })

    event.preventDefault()
  }
  
  // setInterval(getCurrCharging, 5000)

  function close(event) {
    // clearInterval(intervalId)
    navigate("/dashboard");

    event.preventDefault()
  }

  return (
    <div className="login-wrapper">
      <h1>Parking details</h1>
      {state.parked &&
      <div>
        Parked: {currCharging[0].x} <br />
        Charged from {currCharging[0].y}% to {currCharging.at(-1).y}%
        <ChargeChart chargeData={currCharging} />
        <p />
        <form>
          <p>Planned charging until:<br />
          <DateTimePicker onChange={(date) => setNewDate(prevNote => ({
                              ...prevNote, leaveDate: date
                            })
                          )}
                          selected={newDate.leaveDate}
                          name="leaveDate"
                          value={newDate.leaveDate} />
          <button type="button" class="btn btn-success" onClick={changeLeaveDate}>Change</button>
          </p>
        </form>
      </div>
      }

      {history &&
        <div>
          <h5>Historical charging details</h5>
          <button type="button" class="btn btn-info" onClick={() => setHistElem((histElem - 1 + history.length) % history.length)}>{'<'}</button>
          <button type="button" class="btn btn-info" onClick={() => setHistElem((histElem + 1) % history.length)}>{'>'}</button>
          <div>
            Parked: {(history[histElem]).records[0].x} <br />
            Left: {(history[histElem]).leave} <br />
            Charged from {(history[histElem]).records[0].y}% to {(history[histElem]).records.at(-1).y}%
            <ChargeChart chargeData={(history[histElem]).records} />
            <br />
          </div>
        </div>
      }

      <p><button type="button" class="btn btn-primary" onClick={close}>Close</button></p>
    </div>
  );
}

export default CarDetails;