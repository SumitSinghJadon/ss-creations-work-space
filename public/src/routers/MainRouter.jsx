import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from '../pages/auth/Login';
import MainDashboard from '../pages/auth/MainDashboard';
import Dashboard from '../pages/auth/Dashboard';
import RTQMRouter from './RTQMRouter';
import Header from '../components/Header';
import MastersRouter from './MastersRouter';
import QmsTabRouter from './QmsTabRouter';
import PlaningRouter from './PlaningRouter';
import AudioLoader from '../utils/Loader';
import ExcelShow from '../pages/RTQM/ExcelShow';
import InputRouter from './InputRouter';
import TvRouter from './TvRouter';


const MainRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="end-line-login" element={<Login />} />


        <Route path="/dashboard/*" element={<Header/>}>
        <Route index path="home" element={<Dashboard />} />

          <Route path="rtqm/*" element={<RTQMRouter />} />
          <Route path="master/*" element={<MastersRouter/>}/>
          <Route path="planing/*" element={<PlaningRouter/>}/>
          <Route path="loader/" element={<AudioLoader/>}/>
        </Route>
        
        <Route path="qms-tab/*" element={<QmsTabRouter/>}/>
        <Route path="input-master/*" element={<InputRouter/>}/>

        <Route path="tv/*" element={<TvRouter/>}/>


        <Route path="excel-show" element={<ExcelShow/>}/>

      
        
        {/* Handle unmatched routes (optional) */}
        {/* <Route path="*" element={<NotFound />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default MainRouter;
