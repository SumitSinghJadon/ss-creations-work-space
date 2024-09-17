import React, { useState, useEffect } from 'react';
import { Player } from '@lottiefiles/react-lottie-player';
import loginAnimation from '../assets/animation.json';
import { FaEye, FaEyeSlash, FaUser, FaLock } from 'react-icons/fa';
import { LuScanFace } from "react-icons/lu";
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { useSelector } from 'react-redux';
import { setTokens } from '../Redux/AuthSlice';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { toast } from 'react-toastify';

const Login = () => {
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [input, setInput] = useState({ username: "", password: "" })
  const [error, setError] = useState('');
  const [Units, setUnits] = useState([]);
  const [selectedUnit, setSelectedUnit] = useState(null);
  const dispatch = useDispatch();

  const { access } = useSelector((state) => state.auth);

  console.log("accessToken", access);


  const handleRoleChange = (event) => {
    setSelectedUnit(event.target.value);
  };
  console.log("Selected Unit:", selectedUnit);



  const handleInput = (e) => {
    let name = e.target.name;
    let value = e.target.value;

    setInput(values => ({ ...values, [name]: value }));
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
      if(selectedUnit != null ){ 
        try {
          const url = 'http://127.0.0.1:8000/api/login/';
          const response = await axios.post(url, input);

          // Extract tokens from the response
          const { access, refresh } = response.data;

          // Log the tokens for debugging
          console.log("Response data:", response.data);
          console.log("Access Token:", access);
          console.log("Refresh Token:", refresh);

          // Save tokens in Redux
          dispatch(setTokens({ "access": access, "refresh": refresh , "unit_id": selectedUnit}));

          // Clear input fields
          setInput({
            username: "",
            password: "",
          });

          // Provide user feedback (consider replacing alert with a more user-friendly UI notification)
          alert("Login successful");
          console.log("Login");

        

        } catch (error) {
          // Provide a more specific error message
          setError(error.response ? error.response.data.message : 'Invalid credentials');
          toast.error('Invalid credentials')
        }
      }
      else{
        console.log("Please Select Unit")
        toast.error("Please Select Unit")
        
      }

  };

  //===========================Axios Unit Get start====================================================================== 

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/unit/')
      .then(response => {
        setUnits(response.data.Units || []);

      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  // ======================================Axios Unit Get end======================================================================


  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };
  return (
    <div className="relative min-h-screen flex items-center justify-center">
      <div className="background absolute inset-0 z-0">
        {[...Array(15)].map((_, i) => (
          <span key={i}></span>
        ))}
      </div>

      <div className="relative z-10 h-auto md:mx-11  bg-[#f6f0f082] rounded-3xl shadow-2xl flex flex-col md:flex-row max-w-4xl w-full">
        <div className="w-full md:border-8 border-indigo-300 bg- md:bg-white md:rounded-3xl md:w-1/2 flex items-center justify-center">
          <Player autoplay loop src={loginAnimation} className='w-40 md:w-auto' />
        </div>
        <div className="w-full md:w-1/2 p-8 flex rounded-tr-3xl rounded-br-3xl flex-col items-center justify-center bg-[#f6f0f004]">
          <h1 className="text-4xl font-ibm-plex-sans font-bold mb-6 text-transparent bg-clip-text gradient-text">
            IntelliSYNC
          </h1>
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Welcome Back!🙋🏻‍♂️</h2>
          <p className="text-lg text-gray-600 mb-6">We’re glad to see you again.</p>
          <div className="space-y-6 w-full">
            <div className="relative">
              <FaUser className="absolute left-4 top-3 text-gray-500" />
              <input
                type="text"
                name='username'
                placeholder="Username"
                className="pl-12 w-full h-12 p-4 border border-gray-300 bg-white rounded-lg shadow-sm placeholder-gray-500 focus:outline-none focus:border-blue-500 transition duration-300 ease-in-out hover:bg-gray-50"
                value={input.username}
                onChange={handleInput}
                required
              />
            </div>
            <div className="relative">
              <FaLock className="absolute left-4 top-3 text-gray-500" />
              <input
                type={passwordVisible ? 'text' : 'password'}
                name='password'
                placeholder="Password"
                className="pl-12 w-full h-12 p-4 border border-gray-300 bg-white rounded-lg shadow-sm placeholder-gray-500 focus:outline-none focus:border-blue-500 transition duration-300 ease-in-out hover:bg-gray-50"
                value={input.password}
                onChange={handleInput}
                required
              />
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="absolute right-4 top-3 text-gray-500"
              >
                {passwordVisible ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>

            <FormControl fullWidth variant="outlined" className="h-12">
              <InputLabel id="Unit-select-label">Unit</InputLabel>
              <Select
                labelId="Unit-select-label"
                id="Unit-select"
                value={selectedUnit}
                onChange={handleRoleChange}
                label="Unit"
                style={{ backgroundColor: 'white' }}
              >
                {Units.map((unit) => (
                  <MenuItem key={unit.id} value={unit.id}>{unit.name}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <button
              onClick={handleSubmit}
              className="w-full shadow-lg h-12 bg-gradient-to-r from-orange-400 to-blue-600 text-white font-bold rounded-lg hover:scale-95 hover:duration-700 hover:shadow-lg transition duration-300 ease-in-out"
            >
              Login
            </button>
            <div className="text-center mt-4">
              <a href="/forgot-password" className="text-blue-600 hover:underline">Forgot Password?</a>
            </div>
          </div>
          <div className="text-gray-600 mt-6 text-center">
            <div className="flex items-center justify-center space-x-4 mb-4">
              <hr className="w-1/3 border-gray-800" />
              <span className="text-gray-500">or</span>
              <hr className="w-1/3 border-gray-800" />
            </div>
            <p className="flex items-center justify-center space-x-2">
              <LuScanFace className="text-teal-500 text-xl" />
              <span>Login with Face ID</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
