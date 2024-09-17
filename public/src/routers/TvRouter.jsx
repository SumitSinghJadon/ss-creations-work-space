import { Route, Routes } from 'react-router-dom';
import TvDashboard1 from '../tv_Dashboard/TvDashboard1';
import TVDashboard2 from '../tv_Dashboard/TvDashboard2';
import TvDashboard from '../tv_Dashboard/TvDashboard';


const TvRouter = () => {
  return (
    <Routes>
      <Route path="dashboard" element={<TvDashboard />} />
      <Route path="dashboard2" element={<TVDashboard2 />} />
      <Route path="dashboard1" element={<TvDashboard1 />} />
      
     


    </Routes>
  );
}

export default TvRouter;
