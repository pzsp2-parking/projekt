import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

import './NewAccount.css'

function NewAccount(props) {

  const navigate = useNavigate();

  const [newAccForm, setNewAccForm] = useState({
    username: "",
    password: "",
    repeat_password: "",
    email: "",
    phone_nr: ""
  })

  function createNewAcc(event) {
    axios({
      method: "POST",
      url:"/api/newAcc",
      data:{
        username: newAccForm.username,
        password: newAccForm.password,
        email: newAccForm.email,
        phone_nr: newAccForm.phone_nr
        }
    })
    .then((response) => {
      props.setToken(response.data.access_token)
      navigate("/dashboard");
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })

    setNewAccForm(prevNote => ({
      ...prevNote, password: "", repeat_password: ""}))

    event.preventDefault()
  }

  function handleChange(event) { 
    const {value, name} = event.target
    setNewAccForm(prevNote => ({
        ...prevNote, [name]: value})
    )}

  function cancel(event) {
    navigate("/");
  }

  return (
    <div className="login-wrapper">
      <h1>Create Account</h1>
      <form>
        <p>
          <input onChange={handleChange} 
                type="username"
                text={newAccForm.username} 
                name="username" 
                placeholder="Username" 
                value={newAccForm.username} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="password"
                text={newAccForm.password} 
                name="password" 
                placeholder="Password" 
                value={newAccForm.password} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="password"
                text={newAccForm.repeat_password} 
                name="repeat_password" 
                placeholder="Repeat password" 
                value={newAccForm.repeat_password} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="email"
                text={newAccForm.email} 
                name="email" 
                placeholder="Email" 
                value={newAccForm.email} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="phone_nr"
                text={newAccForm.phone_nr} 
                name="phone_nr" 
                placeholder="Phone nr" 
                value={newAccForm.phone_nr} />
        </p>

        <p>
          <button type="button" class="btn btn-success" onClick={createNewAcc}>Submit</button>
          <button type="button" class="btn btn-danger" onClick={cancel}>Cancel</button>
        </p>

        {/* <p><button type="button" class="btn btn-link" onClick={createAcc}>New account</button></p> */}
      </form>
    </div>
  );
}

export default NewAccount;