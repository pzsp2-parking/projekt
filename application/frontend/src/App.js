import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import './App.css';
import Login from './components/Login/Login';
import NewAccount from './components/NewAccount/NewAccount'
import Dashboard from './components/Dashboard/Dashboard';
import AddCar from './components/AddCar';
import Header from './components/Header';
import useToken from './components/useToken';

function App() {
  const { token, removeToken, setToken } = useToken();

  return (
    <BrowserRouter>
      <div className="App">
        {!token && token !== "" && token !== undefined?
        (
          <>
            <Routes>
              <Route exact path="/createAcc" element={<NewAccount setToken={setToken}/>}></Route>
              <Route path="*" element={<Login setToken={setToken}/>}></Route>
            </Routes>
          </>
        )
        :(
          <>
            <Routes>
              <Route exact path="/addCar" element={<div><Header token={removeToken}/><AddCar token={token} setToken={setToken}/></div>}></Route>
              <Route path="*" element={<div><Header token={removeToken}/><Dashboard token={token} setToken={setToken}/></div>}></Route>
            </Routes>
          </>
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;