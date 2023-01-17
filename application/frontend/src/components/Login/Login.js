import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

import './Login.css'

function Login(props) {

  const navigate = useNavigate();

  const [loginForm, setloginForm] = useState({
    login: "",
    password: ""
  })

  // <Login setToken={setToken} />
  function createAcc(event) {
    navigate("/createAcc");
  }

  function logMeIn(event) {
    axios({
      method: "POST",
      url:"/api/token",
      data:{
        login: loginForm.login,
        password: loginForm.password
        }
    })
    .then((response) => {
      props.setToken(response.data.access_token)
      if (response.data.account_type === "cli")
        navigate("/dashboard");
      else
        navigate("/empPage");
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })

    setloginForm(({
      login: "",
      password: ""}))

    event.preventDefault()
  }

  function handleChange(event) { 
    const {value, name} = event.target
    setloginForm(prevNote => ({
        ...prevNote, [name]: value})
    )}

  return (
    <div className="login-wrapper">
      <h1>Login</h1>
      <form>
        <p>
          <input onChange={handleChange} 
                type="login"
                text={loginForm.login} 
                name="login" 
                placeholder="Login" 
                value={loginForm.login} />
        </p>
        <p>
          <input onChange={handleChange} 
                type="password"
                text={loginForm.password} 
                name="password" 
                placeholder="Password" 
                value={loginForm.password} />
        </p>

        <p><button type="button" class="btn btn-success" onClick={logMeIn}>Login</button></p>

        <p><button type="button" class="btn btn-link" onClick={createAcc}>New account</button></p>
      </form>
    </div>
  );
}

export default Login;