// src/components/LogoutComponent.jsx
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import axios from 'axios';
import { removeTokens } from '../Redux/AuthSlice'; // Adjust the path to your authSlice
import { useNavigate } from 'react-router-dom';



const LogOut = () => {
  const dispatch = useDispatch();
  const accessToken = useSelector((state) => state.auth.access);
  const refreshToken = useSelector((state) => state.auth.refresh);
  const navigate = useNavigate();

  
  console.log("acc",accessToken)// Assuming state.auth.access holds the access token

  const handleLogout = async () => {
      // Dispatch action to remove tokens from Redux store
      dispatch(removeTokens());
      navigate('/');
  };

  return (
    <button onClick={handleLogout}>
      Logout
    </button>
  );
};

export default LogOut;
