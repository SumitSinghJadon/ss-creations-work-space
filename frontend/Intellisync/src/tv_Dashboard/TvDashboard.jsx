

import React, { useState, useEffect } from "react";
import {  useNavigate, useParams } from "react-router-dom";
import TvDashboard1 from "./TvDashboard1";
import TvDashboard2 from "./TvDashboard2";

const TvDashboard = () => {
  const [tvdisplay, setTvDisplay] = useState('tvone');
  const { line_id } = useParams();
  console.log('Line ID in TvDashboard:', line_id);

  useEffect(() => {
    let displaychange;

    if (tvdisplay === 'tvone') {
      displaychange = setInterval(() => {
        setTvDisplay('tvtwo');
      }, 15000); // 15 seconds
    } else if (tvdisplay === "tvtwo") {
      displaychange = setInterval(() => {
        setTvDisplay('tvone');
      }, 15000); // 15 seconds
    }

    return () => clearInterval(displaychange);
  }, [tvdisplay]);

//   const navigateToTvDashboard2 = () => {
//     navigate(`/tv/dashboard2/${line_id}`); // Navigate to TvDashboard2 with line_id
//   };

  return (
    <>
      {(tvdisplay === 'tvone') ? (<TvDashboard1  />) : (<TvDashboard2 line_id={line_id} />)}
    </>
  );
};

export default TvDashboard;
