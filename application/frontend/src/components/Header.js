import { useNavigate } from "react-router-dom";
import axios from "axios";

function Header(props) {

  const navigate = useNavigate();

  function logMeOut() {
    axios({
      method: "POST",
      url:"/api/logout",
    })
    .then((response) => {
       props.token()
       navigate("/");
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

    return(
      <header className="App-header">
        <img src={'./logo.png'} className="App-logo" alt="logo"/>
        <button type="button" class="btn btn-light" style={{float: 'right',}} onClick={logMeOut}> 
            Logout
        </button>
      </header>
    )
}

export default Header;
