import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import axios from 'axios';
import DateTimePicker from 'react-datetime-picker'
import Select from 'react-select'

function Park(props) {

  const navigate = useNavigate();
	const {state} = useLocation();

  const [parkForm, setParkForm] = useState({
    parking: "",
    chosenCharger: "",
    leaveDatetime: new Date(Date.now() + 8 * (60 * 60 * 1000)),
    currentCharge: ""
  })

	const [carparks, setCarparks] = useState([])
	const [parkMap, setParkMap] = useState()

	useEffect(() => {
    axios({
      method: "POST",
      url:`/api/carparks`,
			headers: {
        Authorization: 'Bearer ' + props.token
      }
    })
      .then(response => {
        setCarparks(
					response.data.parks)
      }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })
  }, [props.token]);

  function doPark(event) {
    axios({
      method: "POST",
      url:"/api/park",
      headers: {
        Authorization: 'Bearer ' + props.token
      },
      data: {
				vin: state.vin, 
        parking: parkForm.parking,
        chosenCharger: parkForm.chosenCharger,
        leaveDatetime: (parkForm.leaveDatetime).toISOString(),
        currentCharge: parkForm.currentCharge
			}
    })
    .then(() => {
      navigate("/dashboard");
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
			}
    })

    event.preventDefault()
  }

  function getMap(parkId) {
    axios({
      method: "POST",
      url:"/api/getMap",
      headers: {
        Authorization: 'Bearer ' + props.token
      },
      data: {
				parkId: parkId
			}
    })
    .then((response) => {
      setParkMap(response.data.parkMap)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
			}
    })
  }

  function handleChange(event) { 
    const {value, name} = event.target
    setParkForm(prevNote => ({
        ...prevNote, [name]: value})
    )}

  function cancel(event) {
    navigate("/dashboard");
  }

  return (
    <div className="login-wrapper">
      <h1>Park</h1>
      <form>
        <p>
					<Select
						options={(carparks).map(opt => ({ label: opt.address, value: opt.id }))}
						isClearable
						placeholder={"Wybierz parking"}
						onChange={(opt) => {
							setParkForm(prevNote => ({
									...prevNote, parking: opt.value
								})
							);
              getMap(opt.value)
            }}
          />
        </p>
          
        {parkMap &&
          <p>{parkMap.split('\n').map(row => <>{row}<br /></>)}</p>
        }

        <p>
          <input onChange={handleChange} 
                type="text"
                text={parkForm.chosenCharger} 
                name="chosenCharger" 
                placeholder="Chosen charger" 
                value={parkForm.chosenCharger} />
        </p>
        <p>
				<DateTimePicker onChange={(date) => setParkForm(prevNote => ({
														...prevNote, leaveDatetime: date
													})
												)}
												selected={parkForm.leaveDatetime}
												name="leaveDatetime"
												value={parkForm.leaveDatetime} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="text"
                text={parkForm.currentCharge} 
                name="currentCharge" 
                placeholder="Current charge level" 
                value={parkForm.currentCharge} />
        </p>

        <p>
          <button type="button" class="btn btn-success" onClick={doPark}>Park</button>
          <button type="button" class="btn btn-danger" onClick={cancel}>Cancel</button>
        </p>
      </form>
    </div>
  );
}

export default Park;