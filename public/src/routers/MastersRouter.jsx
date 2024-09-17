// import React from 'react';
import { Route, Routes } from 'react-router-dom';
import DefectMaster from '../pages/Masters/DefectMaster';
import OperationMaster from '../pages/Masters/OperationMaster';
import StyleSilhouettes from '../pages/Masters/StyleSilhouettes';
import ObHistory from '../pages/Masters/ObHistory';
import SilhouettesList from '../pages/Masters/SilhouettesList';


const MastersRouter = () => {
  return (
    <Routes>
      <Route path="defect-master" element={<DefectMaster />} />
      <Route path="operation-master" element={<OperationMaster />} />
      <Route path="style-silhouettes" element={<StyleSilhouettes />} />
      <Route path="ob-history" element={<ObHistory />} />
      <Route path="silhouettes-list" element={<SilhouettesList />} />

      

      


    </Routes>
  );
}

export default MastersRouter;
