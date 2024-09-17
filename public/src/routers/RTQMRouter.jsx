import { Route, Routes } from 'react-router-dom';
import OrderProcessPlanMT from '../pages/RTQM/OrderProcessPlanMT';
import OrderProcessPlanDT from '../pages/RTQM/OrderProcessPlanDT';

const RTQMRouter = () => {
  return (
    <Routes>
      <Route path="order-process-plan-mt" element={<OrderProcessPlanMT />} />
      <Route path="order-process-plan-dt" element={<OrderProcessPlanDT />} />
     


    </Routes>
  );
}

export default RTQMRouter;
