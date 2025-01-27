import React, { useEffect, useRef, useState } from "react";
import * as XLSX from "xlsx";
import axios from "axios";
import DjangoConfig from "../../config/Config";
import Select from 'react-select';
import Skeleton from "react-loading-skeleton";
import { toast } from "react-toastify";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const OperationMaster = () => {
    const [data, setData] = useState([]);
    const [sendData, setSendData] = useState([]);
    const [buyerList, setBuyerList] = useState([]);
    const [styleNoData, setStyleNoData] = useState([]);
    const [selectedBuyer, setSelectedBuyer] = useState(null);
    const [selectedStyle, setSelectedStyle] = useState(null);
    const [colorData, setColorData] = useState([])
    const [selectedColor, setSelectedColor] = useState(null)
    const [isLoading, setIsLoading] = useState(false);
    const [obDate, setObDate] = useState("");
    const [reCutting, setReCutting] = useState(0);
    const [kazButton, setKazButton] = useState(0);
    const [other, setOther] = useState(0)
    const [selectAll, setSelectAll] = useState(false);
    const [isButtonDisabled, setIsButtonDisabled] = useState(false);
    const formRef = useRef(null);

    const header = data[0];
    const resetForm = () => {
        setSendData([]);
        setSelectedBuyer(null);
        setSelectedStyle(null);
        setSelectedColor(null);
        setObDate('');
        setReCutting('');
        setKazButton('');
        setOther('');
        setData([])
    };

    const saveData = (event) => {
        event.preventDefault();
        if (header === undefined) {
            toast.error("Please Upload   OB");
            return;
        }
        if (sendData.length === 0) {
            toast.error("Please  Select OB");
            return;
        }

        const userData = {
            sendData: sendData,
            header: header,
            buyer: selectedBuyer.value,
            buyer_name: selectedBuyer.label,
            style: selectedStyle.value,
            color: selectedColor?.value || "",
            obDate: obDate,
            reCutting: reCutting,
            kazButton: kazButton,
            other: other,
        };

        console.log("sendData", userData);

        // let url = `${DjangoConfig.apiUrl}/rtqm/excel_data_show_view/`;
        let url = `http://localhost:8000/rtqm/excel_data_show_view/`;
        axios.post(url, userData)
            .then((res) => {
                console.log(res.data.ob_no)
                toast.success(`Data Saved ${res.data.ob_no}`);
                resetForm()
                // formRef.current.reset();
            })
            .catch((e) => {
                toast.error(e);
            });
    };


    // const sendRows = (e) => {
    //     if (e.target.checked) {
    //         const value = JSON.parse(e.target.value);
    //         setSendData(values => ([...values, value]));
    //     } else {
    //         let valueData = sendData.filter((key) => key[0] !== e.target.value[0]);
    //         setSendData(valueData);
    //     }
    // };



  
    const sendRows = (e) => {
        const checked = e.target.checked;
        const value = JSON.parse(e.target.value);
    
        if (checked) {
            setSendData(currentData => [...currentData, value]);
        } else {
            setSendData(currentData => currentData.filter(row => JSON.stringify(row) !== JSON.stringify(value)));
    
            const allUnchecked = data.slice(1).every(row => {
                return !sendData.some(item => JSON.stringify(item) === JSON.stringify(row));
            });
            if (allUnchecked) {
                setSelectAll(false);
            }
        }
    };

    const handleSelectAll = (e) => {
        const checked = e.target.checked;
        setSelectAll(checked);
    
        if (checked) {
            setSendData(data.map(row => JSON.parse(JSON.stringify(row))));
        } else {
            setSendData([]);
        }
    };
    
    const handleFile = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.readAsBinaryString(file);

        reader.onload = (e) => {
            const binaryString = e.target.result;
            const workbook = XLSX.read(binaryString, { type: "binary" });
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
            const parseData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
            setData(parseData);


        };
    };

    const fetchInitialData = async () => {
        try {
            const response = await axios.get(`${DjangoConfig.apiUrl}/rtqm/qms_planing/`);
            setBuyerList(response.data.buyer_list.map(item => ({ value: item.buyer_code, label: item.buyer_name })));
        } catch (error) {
            console.error('Error fetching initial data:', error);
        }
    };

    useEffect(() => {
        fetchInitialData();
    }, []);

    const handleBuyerChange = (selectedValue) => {
        setSelectedBuyer(selectedValue);
        fatchByBuyer(selectedValue);
    };

    const fatchByBuyer = (selectedValue) => {
        setStyleNoData([]);
        const userData = {
            buyer_filter: selectedValue.value,
        };
        const queryParams = new URLSearchParams(userData).toString();
        axios.get(`${DjangoConfig.apiUrl}/rtqm/excel_data_show_view/?${queryParams}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            const responseData = response.data.data;
            console.log("style data ", responseData)
            const uniqueStyles = [...new Set(responseData.map(item => item.styleno))];
            const styleOptions = uniqueStyles.map(style => ({ value: style, label: style }));
            setStyleNoData(styleOptions);
            setIsLoading(false);
        })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
    };


    const handleStyleChange = (selectedValue) => {
        setSelectedStyle(selectedValue);
        console.log("style selected", selectedValue)
        fatchByStyle(selectedValue);
    };


    const fatchByStyle = (selectedValue) => {
        const userData = {
            buyer_filter: selectedBuyer.value,
            style_filter: selectedValue.value
        };
        const queryParams = new URLSearchParams(userData).toString();
        axios.get(`${DjangoConfig.apiUrl}/rtqm/excel_data_show_view/?${queryParams}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            const responseData = response.data.data;
            const uniqueColor = [...new Set(responseData.map(item => item.color))];
            const colorOptions = uniqueColor.map(color => ({ value: color, label: color }));
            setColorData(colorOptions);

            // setColorData(response.data.data.map(item => ({ value: item.color, label: item.color })))

            setIsLoading(false);
        })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
    };

    const navigate = useNavigate()
    const obTablePage = () => {
        navigate('/dashboard/master/ob-history')
    }


    return (
        <>
            <div className='w-full h-10 flex items-center justify-end  rounded-lg'>
                <Button
                    onClick={obTablePage}
                    variant="contained"
                    color="primary"
                    className="float-right mr-2"
                >
                    Ob History
                </Button>
            </div>
            <form onSubmit={saveData} ref={formRef} className="mt-2">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4 mb-4">
                    <div>
                        <label htmlFor=".xls"> Upload Excel File</label>
                        <input type="file" accept=".xlsx, .xls" onChange={handleFile} className="w-full h-11 border-2 border-gray-400 rounded-md" />
                    </div>

                    <div>
                        <label htmlFor="buyerList"> Buyer</label>
                        <Select
                            options={buyerList}
                            value={selectedBuyer}
                            onChange={handleBuyerChange}
                            name="buyer"
                            placeholder="Select Buyer"
                            className="w-full border-2 border-gray-400 rounded-md"
                            isSearchable
                            isLoading={!buyerList.length}
                            loadingMessage={() => <Skeleton count={5} />}
                            styles={{
                                control: (provided) => ({
                                    ...provided,
                                    height: '40px',
                                    fontSize: '12px',
                                }),
                            }}
                        />
                    </div>

                    <div>
                        <label htmlFor="styleNoData">Style No</label>
                        <Select
                            options={styleNoData}
                            value={selectedStyle}
                            onChange={handleStyleChange}
                            name="style_no"
                            placeholder="Select Style"
                            className="w-full border-2 border-gray-400 rounded-md"
                            isSearchable
                            isLoading={!styleNoData.length}
                            loadingMessage={() => <Skeleton count={5} />}
                            isClearable
                            styles={{
                                control: (provided) => ({
                                    ...provided,
                                    height: '40px',
                                    fontSize: '12px',
                                }),
                            }}
                        />
                    </div>


                    <div>
                        <label htmlFor="colorData">Color</label>
                        <Select
                            options={colorData}
                            value={selectedColor}
                            onChange={setSelectedColor}
                            placeholder="Select Color"
                            className="w-full border-2 z-20 border-gray-400 rounded-md"
                            isSearchable
                            isLoading={!colorData.length}
                            loadingMessage={() => <Skeleton count={5} />}
                            isClearable
                            styles={{
                                control: (provided) => ({
                                    ...provided,
                                    height: '40px',
                                    fontSize: '12px',
                                }),
                            }}
                        />
                    </div>

                    <div>
                        <label htmlFor="ob_date">OB Date</label>
                        <input type="date" name="ob_date" value={obDate} onChange={(e) => setObDate(e.target.value)} className="w-full border-2 h-11 border-gray-400 rounded-md" required />
                    </div>

                    <div>
                        <label htmlFor="recutting">Re-Cutting</label>
                        <input type="number" name="recutting" value={reCutting} onChange={(e) => setReCutting(e.target.value)} className="w-full border-2 h-11 border-gray-400 rounded-md" />
                    </div>

                    <div>
                        <label htmlFor="kaz_button">Kaz-Button</label>
                        <input type="number" name="kaz_button" value={kazButton} onChange={(e) => setKazButton(e.target.value)} className="w-full border-2 h-11 border-gray-400 rounded-md" />
                    </div>
                    <div>
                        <label htmlFor="other">Others</label>
                        <input type="number" name="other" value={other} onChange={(e) => setOther(e.target.value)} className="w-full border-2 h-11 border-gray-400 rounded-md" />
                    </div>

                    <div>
                        <button type="submit" disabled={isButtonDisabled} className="btn w-full mt-5 btn-primary">Save Data</button>
                    </div>
                </div>
                <div>
                    {/* {data.length > 0 && (
                        <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
                            <thead className="bg-white divide-y divide-gray-200">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border border-gray-300" >Checkbox</th>
                                    {data[0].map((header, index) => (
                                        <th key={index} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border border-gray-300">
                                            {header}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {data.slice(1).map((row, rowIndex) => (
                                    <tr key={rowIndex}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border border-gray-300">
                                            <input type="checkbox" value={JSON.stringify(row)} onChange={(e) => sendRows(e)} />
                                        </td>
                                        {data[0].map((header, cellIndex) => (
                                            <td key={cellIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border border-gray-300">
                                                {row[cellIndex]}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )} */}

                    {data.length > 0 && (
                        <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
                            <thead className="bg-white divide-y divide-gray-200">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border border-gray-300">
                                        <input type="checkbox" onChange={handleSelectAll} checked={selectAll} />
                                    </th>
                                    {data[0].map((header, index) => (
                                        <th key={index} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border border-gray-300">
                                            {header}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {data.slice(1).map((row, rowIndex) => (
                                    <tr key={rowIndex}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border border-gray-300">
                                            {/* <input type="checkbox" value={JSON.stringify(row)} onChange={(e) => sendRows(e)} checked={selectAll} /> */}
                                            <input
                                                type="checkbox"
                                                value={JSON.stringify(row)}
                                                onChange={sendRows}
                                                checked={sendData.some(item => JSON.stringify(item) === JSON.stringify(row))}
                                            />
                                        </td>
                                        {data[0].map((header, cellIndex) => (
                                            <td key={cellIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border border-gray-300">
                                                {row[cellIndex]}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}

                </div>
            </form>
        </>
    );
};

export default OperationMaster;
