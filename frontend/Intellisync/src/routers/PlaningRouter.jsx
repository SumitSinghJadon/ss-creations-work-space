import { Route, Routes } from 'react-router-dom';
import Planing from '../pages/plan/Planing';
import SelectPlaningSQ from '../pages/plan/SelectPlaningSQ';




const PlaningRouter = () => {
    return (
        <Routes>
           <Route path="planing-input" element={<Planing/>}/>
           <Route path="planing-size-quantity" element={<SelectPlaningSQ/>}/>

           

        </Routes>
    );
}

export default PlaningRouter;
