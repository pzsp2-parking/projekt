import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import axios from 'axios';
import DateTimePicker from 'react-datetime-picker';

const Charging = (props) => {
  const positions = props.charging.map((charge) => {
    return (
      <p><b>Date:</b> {charge.time} <b>Charge level:</b> {charge.charge_level}</p>
    )
  })
  return (
    <div>{positions}</div>
  )
}

function CarDetails(props) {

  const navigate = useNavigate();
	const {state} = useLocation();

  const [newDate, setNewDate] = useState({
    leaveDate: new Date(Date.now() + 8 * (60 * 60 * 1000))
  })

  const [currCharging, setCurrCharging] = useState([])
  const [history, setHistory] = useState([])

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
      <form>
        <p>
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
      {currCharging &&
        <div>
          <h5>Current charging details</h5>
          <Charging charging={currCharging} />
        </div>
      }

      {history &&
        <div>
          <h5>Historical charging details</h5>
          <Charging charging={history} />
        </div>
      }

      <p><button type="button" class="btn btn-primary" onClick={close}>Close</button></p>
    </div>
  );
}

export default CarDetails;