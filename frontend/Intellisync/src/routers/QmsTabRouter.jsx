// import React from 'react';
import { Route, Routes } from 'react-router-dom';
import QCSection from '../pages/qmsTab/QCSection';
import DefectSizeMaster from '../pages/qmsTab/DefectSizeMaster';
import PassSizeMaster from '../pages/qmsTab/PassSizeMaster';
import OperationsMasterSelect from '../pages/qmsTab/OperationsMasterSelect';
import DefectMasterSelect from '../pages/qmsTab/DefectMasterSelect';
import ConvertImageInToSketch from '../pages/qmsTab/ConvertImageInToSketch';
import DefectMarkLocation from '../pages/qmsTab/DefectMarkLocation';
import PassSizeInput from '../pages/qmsTab/passRftTab/PassSizeInput';
import DefectEndLineStart from '../pages/qmsTab/DefectEndLineStart';
import RejectSizeMaster from '../pages/qmsTab/RejectTab/RejectSizeMaster';
import RejectOperationMaster from '../pages/qmsTab/RejectTab/RejectOperationMaster';
import RejectDefectMaster from '../pages/qmsTab/RejectTab/RejectDefectSelection';
import RejectMarkLocation from '../pages/qmsTab/RejectTab/RejectMarkLocation';
import RectifiedDefectDtList from '../pages/qmsTab/RectifiedTab/RectifiedDefectDtList';
import RectifiedDefectSelect from '../pages/qmsTab/RectifiedTab/RectifiedDefectSelect';
import RectifiedOperationsMaster from '../pages/qmsTab/RectifiedTab/RectifiedOperationsMt';
import RectifiedMarkLocation from '../pages/qmsTab/RectifiedTab/RectifiedMarkLocation';


const QmsTabRouter = () => {
    return (
        <Routes>
            <Route path="qc-section" element={<QCSection />} />
            <Route path="defect-end-line-start" element={<DefectEndLineStart/>} />

            {/* Defect Routers */}
            <Route path="operation-master-select" element={<OperationsMasterSelect />} />
            <Route path="pass-size-master" element={<PassSizeMaster/>} />
            <Route path="defect-size-master" element={<DefectSizeMaster/>} />
            <Route path="defect-master-select" element={<DefectMasterSelect/>} />
            <Route path="convert-image-in-to-sketch" element={<ConvertImageInToSketch/>} />
            <Route path="defect-mark-location" element={<DefectMarkLocation/>} />

            {/* Pass Routers */}
            <Route path="pass-size-input" element={<PassSizeInput/>} />

            {/* Reject Routers */}
            <Route path="reject-size-master" element={<RejectSizeMaster/>} />
            <Route path="reject-operation-master" element={<RejectOperationMaster/>} />
            <Route path="reject-defect-master" element={<RejectDefectMaster/>} />
            <Route path="reject-mark-location" element={<RejectMarkLocation/>} />


            {/* Rectified Routers */}

            <Route path="rectified-defect-dt-list" element={<RectifiedDefectDtList/>} />
            <Route path="rectified-operation-master" element={<RectifiedOperationsMaster/>} />
            <Route path="rectified-defect-select" element={<RectifiedDefectSelect/>} />
            <Route path="rectified-mark-location" element={<RectifiedMarkLocation/>} />




            






            


        </Routes>
    );
}

export default QmsTabRouter;
