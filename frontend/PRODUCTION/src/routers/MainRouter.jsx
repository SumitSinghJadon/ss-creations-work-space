import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import FileHandOver from '../pages/FileHandOver';
import ProductionPPM from '../pages/ProductionPPM';
import Login from '../auth/Login';
import LayOut from '../layout/LayOut';


const MainRouter = () => {
    return (
      <BrowserRouter>
        <Routes>
        <Route index element={<Login/>} />
        <Route path='Login' element={<Login/>} />
        <Route path='/' element={<LayOut />} >
          <Route path="FileHandOver" element={<FileHandOver />} />
          <Route path="ProductionPPM" element={<ProductionPPM/>} />
        </Route>
        </Routes>
      </BrowserRouter>
    );
  }
  
  export default MainRouter;