import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

function AddCar(props) {

  const navigate = useNavigate();

  const [newCarForm, setNewCarForm] = useState({
    vin: "",
    reg_no: "",
    model: "",
    brand: "",
    capacity: ""
  })

  function createNewCar(event) {
    axios({
      method: "POST",
      url:"/api/addCar",
      headers: {
        Authorization: 'Bearer ' + props.token
      },
      data:{
        vin: newCarForm.vin,
        reg_no: newCarForm.reg_no,
        model: newCarForm.model,
        brand: newCarForm.brand,
        capacity: newCarForm.capacity
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

  function handleChange(event) { 
    const {value, name} = event.target
    setNewCarForm(prevNote => ({
        ...prevNote, [name]: value})
    )}

  function cancel(event) {
    navigate("/dashboard");
  }

  return (
    <div className="login-wrapper">
      <h1>Add new car</h1>
      <form>
        <p>
          <input onChange={handleChange} 
                type="vin"
                text={newCarForm.vin} 
                name="vin" 
                placeholder="VIN" 
                value={newCarForm.vin} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="reg_no"
                text={newCarForm.reg_no} 
                name="reg_no" 
                placeholder="Registration nr" 
                value={newCarForm.reg_no} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="brand"
                text={newCarForm.brand} 
                name="brand" 
                placeholder="Brand" 
                value={newCarForm.brand} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="model"
                text={newCarForm.model} 
                name="model" 
                placeholder="Model" 
                value={newCarForm.model} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="capacity"
                text={newCarForm.capacity} 
                name="capacity" 
                placeholder="Capacity" 
                value={newCarForm.capacity} />
        </p>

        <p>
          <button type="button" class="btn btn-success" onClick={createNewCar}>Add</button>
          <button type="button" class="btn btn-danger" onClick={cancel}>Cancel</button>
        </p>
      </form>
    </div>
  );
}

export default AddCar;