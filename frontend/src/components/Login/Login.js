import { useState } from 'react';
import axios from 'axios';

import './Login.css'

function Login(props) {

  const [loginForm, setloginForm] = useState({
    login: "",
    password: ""
  })

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

        <button onClick={logMeIn}>Submit</button>
      </form>
    </div>
  );
}

export default Login;