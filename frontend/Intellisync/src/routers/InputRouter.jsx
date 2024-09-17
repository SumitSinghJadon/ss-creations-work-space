import React from 'react';
import { Route, Routes } from 'react-router-dom';

import LineMaster from '../pages/InputMaster/LineMaster';
import SelectQuantityByLineMaster from '../pages/InputMaster/SelectQuantityByLineMaster';
import InputLogin from '../pages/InputMaster/InputLogin';

const InputRouter = () => {
    return (
        <Routes>
            <Route path="input-login" element={<InputLogin />} />
            <Route path="line-master" element={<LineMaster />} />
            <Route path="select-quantity-by-master" element={<SelectQuantityByLineMaster />} />
        </Routes>
    );
}

export default InputRouter;
