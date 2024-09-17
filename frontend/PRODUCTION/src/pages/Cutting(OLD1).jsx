import SingleSelectComponent from "../components/SingleSelectComponent";
import { useState } from "react";


const Cutting=()=> {
    const [selectedValues, setSelectedValues] = useState({});

    const options = [
        { value: 'option1', label: 'Option 1' },
        { value: 'option2', label: 'Option 2' },
        { value: 'option3', label: 'Option 3' },
    ];

    const handleSelectChange = (id, value) => {
        console.log('Handle Select Change:', id, value);
        setSelectedValues(prevValues => ({
            ...prevValues,
            [id]: value
        }));
    };

    return (
        <div className="w-full box-border border-2 border-gray-200  shadow">
            <div className="">
                <div className="w-full bg-blue-800 text-white py-2 text-center">CUTTING</div>

                <div className="p-2">
                    <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 text-xs ">
                        {[
                            { id: 'cuttingNo', label: 'Cutting No' },
                            { id: 'cuttingDate', label: 'Cutting Date' },
                            { id: 'styleNo', label: 'Style No' },
                            { id: 'orderNo', label: 'Order No' },
                            { id: 'buyerCode', label: 'Buyer Code' },
                            { id: 'color', label: 'Color' },
                            { id: 'process', label: 'Process' },
                            { id: 'vendorPoNo', label: 'Vendor Po No' },
                            { id: 'requisitionNo', label: 'Requisition No' },
                            { id: 'component', label: 'Component' },
                            { id: 'shipmentDueDate', label: 'Shipment Due Date' },
                            { id: 'timeZone', label: 'Time Zone' },
                            { id: 'personResponsible', label: 'Person Responsible' },
                            { id: 'remarks', label: 'Remarks' }
                        ].map(({ id, label }) => (
                            <div key={id} className="flex flex-col ">
                                <SingleSelectComponent
                                    options={options}
                                    value={selectedValues[id] || ''}
                                    onChange={(value) => handleSelectChange(id, value)}
                                    name={id}
                                    id={id}
                                    placeholder={label}
                                />
                            </div>
                        ))}
                    </div>

                    <div className="flex flex-row sm:flex-row justify-between mt-4 gap-4">
                        <button className="w-full sm:w-auto max-w-[100px] border border-gray-200 bg-blue-800 text-white py-2 rounded-md px-7">Close</button>
                        <button className="w-full sm:w-auto max-w-[100px] border border-gray-200 bg-blue-800 text-white py-2 rounded-md px-7">Show</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Cutting;