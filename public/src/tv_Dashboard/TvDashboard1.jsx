import axios from 'axios';
import React, { useEffect, useState } from 'react';
import favicon from "./favicon.ico"
import DjangoConfig from '../config/Config';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { useLocation } from 'react-router-dom';
const TvDashboard1 = () => {
  const [time, setTime] = useState('');
  const [formulasData, setFormulasDate] = useState({})
  const [planData,setPlanData] = useState({})
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  // console.log('Line ID in TvDashboard1:', line_id);


  const updateTime = () => {
    const now = new Date();
    let hours = now.getHours();
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    const hoursStr = hours.toString().padStart(2, '0');
    setTime(`${hoursStr}:${minutes}:${seconds} ${ampm}`);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const queryParams = new URLSearchParams(location.search);
        const line_id = queryParams.get('line_id');
        const response = await axios.get(`${DjangoConfig.apiUrl}/rtqm/sewing_tv_dashboard/?line_id=${line_id}`, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        setFormulasDate(response.data.formulas);
        setPlanData(response.data.plan_data)
        console.log("sewing tv data", response.data)
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  let percentage = 0
  return (
    <section id="dashboard" className="text-white bg-black pb-1">
      <header>
        <nav className="bg-[#070F2B] border-2 border-gray-600 w-full h-16 flex items-center">
          <div className="w-1/5 h-full flex items-center justify-center border-r border-black">
            <a className="flex items-center justify-center" href="#" style={{ cursor: 'pointer' }}>
              <img src={favicon} alt="logo" className="mr- w-10" />
              <span className="text-goldenrod text-2xl font-semibold mb-2">IntelliSYNC</span>
            </a>
          </div>
          <div className="w-3/5 h-full flex items-center justify-center border-r border-black">
            <span className="text-goldenrod text-3xl font-bold">Sewing Dashboard</span>
          </div>
          <div className="w-1/5 h-full flex items-center justify-center">
            <div id="time" className="text-goldenrod text-2xl font-bold mt-6 ml-10">{time}</div>
          </div>
        </nav>

        <div className="bg-black border border-gray-500 w-full h-7vh flex justify-between pt-2 pb-2 items-center mt-1">
          <div className="w-1/5 h-full flex items-center justify-center border-r border-black">
            <span className="text-white text-2xl font-semibold">{planData.line}</span>
          </div>|
          <div className="w-1/5 h-full flex items-center justify-center border-r border-black">
            <span className="text-white text-2xl font-semibold">{planData.buyer}</span>
          </div>|
          <div className="w-1/5 h-full flex items-center justify-center border-r border-black">
            <span className="text-white text-2xl font-semibold"> {planData.style}</span>
          </div>|
          <div className="w-1/5 h-full flex items-center justify-center border-r border-black">
            <span className="text-white text-2xl font-semibold"> {planData.color}</span>
          </div>|
          <div className="w-1/5 h-full flex items-center justify-center">
            <span className="text-white text-2xl font-semibold">Hour No</span>
          </div>
        </div>

        <div className="flex h-[79vh] w-full mt-1">
          <div className="w-1/3 h-full flex flex-col">
            <div className="border-2  border-gray-500 w-full pl-3 flex flex-col items-start justify-evenly h-[64vh]">
             <div className='w-full flex justify-between items-center'>
                <div className="text-chocolate text-white text-xl font-semibold">Day Target</div>
                <div className='font-bold text-7xl pr-6'>00</div>
              </div> 

              <div className='w-full flex justify-between items-center'>
                <div className="text-chocolate text-white text-xl font-semibold">Real Time Target</div>
                <div className='font-bold pr-6 text-7xl'>00</div>
              </div>

              <div className='w-full flex justify-between items-center'>
                <div className="text-chocolate text-white text-xl font-semibold">Difference</div>
                <div className='font-bold pr-6 text-7xl'>00</div>
              </div>

              <div className='w-full flex justify-between items-center'>
                <div className="text-chocolate text-white text-xl font-semibold">Alter Balance</div>
                <div className='font-bold pr-6 text-7xl'>{formulasData.alter_balance || '00'}</div>
              </div>

              <div className='w-full flex justify-between items-center'>
                <div className="text-chocolate text-white text-xl font-semibold">Actual</div>
                <div className='font-bold text-7xl pr-6'>{formulasData.actual_pass || '00'}</div>
              </div>

            </div>

            <div className="border-2 border-gray-500 w-full h-[12vh] mt-1 flex justify-between items-center ">
              <span className="text-chocolate text-white text-2xl font-semibold pl-3">WIP&nbsp;:&nbsp;</span>
              <span className='font-bold text-7xl pr-5'>{formulasData.wip || '00'}</span>
              
            </div>
          </div>

          <div className="w-[45%] h-full flex flex-col ml-3">

            <div className="flex w-full h-[64vh]">

              <div className="border-2 border-gray-500 w-1/2 h-full">
                <span className="text-chocolate text-whitetext-white text-2xl font-semibold p-5">RFT%</span>
                <div className='text-center mt-4'>
                  <h2 className='font-bold text-8xl text-white pt-4'>{formulasData.rft_percentage || '00'}</h2>
                </div>
                <div style={{ width: 180, height: 180 }}  className='ml-10 mt-6'>
                <CircularProgressbar
                    value={formulasData.rft_percentage}
                    text={`${formulasData.rft_percentage || '00'}%`}
                    background
                    backgroundPadding={6}
                    styles={{
                        backgroundColor: "#3e98c7",
                        textColor: "#fff",
                        pathColor: "#fff",
                        trailColor: "transparent"
                    }}
                />
                    
                </div>
              </div>

              <div className="border-2 border-gray-500 w-1/2 h-full ml-3 ">
                <span className="text-chocolate text-whitetext-white text-2xl font-semibold p-5">EFF%</span>
                <div className='font-bold text-8xl text-center text-white pt-4 mt-4'>{formulasData.eff_percentage}</div>
                <div style={{ width: 180, height: 180 }}  className='ml-10 mt-6'>
                <CircularProgressbar
                  value={formulasData.eff_percentage}
                  text={`${formulasData.eff_percentage || '00'}%`}
                  styles={{
                    // Rotation of path and trail, in number of turns (0-1)
                    rotation: 0.25,

                    // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                    strokeLinecap: 'butt',

                    // Text size
                    textSize: '16px',

                    // How long animation takes to go from one percentage to another, in seconds
                    pathTransitionDuration: 0.5,

                    // Can specify path transition in more detail, or remove it entirely
                    // pathTransition: 'none',

                    // Colors
                    pathColor: `rgba(62, 152, 199, ${percentage / 100})`,
                    textColor: '#fff',
                    trailColor: '#d6d6d6',
                    backgroundColor: '#3e98c7',
                  }}
                />;
                </div>
              </div>

            </div>

            <div className="flex w-full h-[12vh] mt-1">
              <div className="border-2 border-gray-500 w-1/2 h-full flex justify-between items-center">
                <div className="text-chocolate text-whitetext-white text-sm font-semibold pl-2">Manpower Tailor</div>
                <div className='font-bold text-7xl  text-white pr-5'>00</div>
              </div>
              <div className="border-2 border-gray-500 w-1/2 h-full ml-3 flex justify-between items-center">
                <div className="text-chocolate text-white  text-sm font-semibold pl-2">Manpower Helper</div>
                <div className='font-bold text-7xl  text-white pr-5'>00</div>
              </div>
            </div>
          </div>

          <div className="w-1/5 h-full ml-3 flex flex-col">
            <div className="border-2 border-gray-500 w-full h-[39vh] ">
              <span className="text-chocolate  text-white text-2xl font-semibold p-4">DHU%</span>
              <div>
                <h2 className='font-bold text-6xl text-white text-center pt-4 mt-10'>{formulasData.dhu_percentage || '00'}</h2>
              </div>
            </div>

            <div className="border-2 border-gray-500 w-full h-[37vh] mt-1">
              <div>
                <span className="text-chocolate text-2xl text-white font-semibold p-4">Defective%</span>
                <h2 className='font-bold text-6xl text-white mt-10 text-center'>{formulasData.defective_percentage || '00'}</h2>
              </div>
            </div>
          </div>
        </div>
      </header>
    </section >
  );
};

export default TvDashboard1;
