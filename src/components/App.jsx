import React, { useState, useEffect } from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom"; // Заменили Link на NavLink
import "../css/app.css";
import axios from "axios";

function App() {
  const navigate = useNavigate();
  const [userDetails, setUserDetails] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem('userId');
    if (userId) {
      axios.get(`http://127.0.0.1:8000/api/v1/users/${userId}/`)
        .then(response => {
          setUserDetails({
            first_name: response.data.first_name,
            last_name: response.data.last_name,
          });
        })
        .catch(error => {
          console.error('Error getting User Data:', error);
          localStorage.removeItem('userId');
          navigate('/login');
        });
    } else {
      navigate('/login'); // Редирект на страницу логина, если userId нет в localStorage
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('userId');
    setUserDetails(null);
    navigate('/login');
  };

  return (
    <div className="app-container">
      <div className="side-bar">
        <div className="user-profile">
          <img
            className="user-avatar"
            src="https://avatars.githubusercontent.com/aksmaxn4?s=120"
            alt="Something"
          />
          <h3>
            {userDetails ? `${userDetails.first_name} ${userDetails.last_name}` : 'Loading...'}
          </h3>
        </div>
        <div className="menu upper">
          <nav>
            <ul>
              <li>
                <NavLink to={`/clients`} activeClassName="active">
                  Clients
                </NavLink>
              </li>
              <li>
                <NavLink to={`/assignments`} activeClassName="active">
                  Assignments
                </NavLink>
              </li>
              <li>
                <NavLink to={`/community`} activeClassName="active">
                  Community
                </NavLink>
              </li>
              {/* <li>
                <NavLink to={`/storage`} activeClassName="active">
                  Storage
                </NavLink>
              </li> */}
            </ul>
          </nav>
        </div>
        <div className="menu lower">
          <nav>
            <ul>
              <li>
                <NavLink to={`/settings`} activeClassName="active">
                  Settings
                </NavLink>
              </li>
              {/* <li>
                <NavLink to={`/support`} activeClassName="active">
                  Support
                </NavLink>
              </li> */}
              <li>
                <a onClick={handleLogout}>
                  Logout
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
}

export default App;
