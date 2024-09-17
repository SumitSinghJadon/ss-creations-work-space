import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addOrder, resetProduct, decrementQuantity } from '../../utils/slice/LineMasterSlice';
import axios from 'axios';
import DjangoConfig from '../../config/Config';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const SelectQuantityByLineMaster = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate()
    const userData = useSelector(state => state.User.userData);
    const [sizeQuantityData, setSizeQuantityData] = useState([])
    const [quantity, setQuantity] = useState(null);
    const [counter, setCounter] = useState(1);
    const [selectedSize, setSelectedSize] = useState('');
    const orderItems = useSelector((state) => state.order.items);
    const sewingPlanData = useSelector(state => state.sewingInput.rowData);
    const [sizeData, setSizeData] = useState([])
    const [totalInput,setTotalInput] = useState([])
    // console.log("sewingPlanData", sewingPlanData,"userData",userData)




    useEffect(() => {
        fetchSizeData();
        fetchSizeQuantityData()
    }, [])

    const fetchSizeData = () => {
        const userData = {
            buyer: sewingPlanData.buyer,
            styleno: sewingPlanData.styleno,
            ourref: sewingPlanData.ourref,
            color: sewingPlanData.color
        };
        const queryParams = new URLSearchParams(userData).toString();
        axios.get(`${DjangoConfig.apiUrl}/rtqm/sewing_line_input/?${queryParams}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            setSizeData(response.data)

        })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
    }


    const fetchSizeQuantityData = () => {
        const userData = {
            id: sewingPlanData?.id  || "",
        };
        const queryParams = new URLSearchParams(userData).toString();
        axios.get(`${DjangoConfig.apiUrl}/rtqm/sewing_line_dt_input/?${queryParams}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            console.log("Size wise Quantity",response.data)
            setSizeQuantityData(response.data.size_dt_list)
            setTotalInput(response.data.size_mt_list)
        })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
    }
    let totalQuantityBackEnd = 0;
    
    if (Array.isArray(sizeQuantityData)) {
        sizeQuantityData.forEach(item => {
            totalQuantityBackEnd += item.quantity;

        });
    }
    let totalQuantityInput =0
    if(Array.isArray(totalInput)){
        totalInput.forEach((item)=>{
            totalQuantityInput += item.total_input_qty

        })
    }
    
    // console.log("totalQuantityBackEnd",totalQuantityBackEnd)
    // console.log("sizeData",sizeData)
    // const getQuantityForSize = (size) => {
    //     const item = orderItems.find(item => item.size === size);
    //     return item ? item.quantity : 0;
    // };

  
   
    console.log("Total Quantity Input:", totalQuantityInput);

    const handleQuantityChange = (event) => {
        const value = parseInt(event.target.value);
        setQuantity(value >= 0 ? value : null);
    };

    let totalProduct = sewingPlanData?.quantity || 0

    const incrementCounter = () => {
       let  limitproduct = totalProduct - totalQuantityInput
        if (quantity > limitproduct) {
            toast.error(`Cannot increment . Total product limit  reached. left for add ${limitproduct}`);
            return;
        }
        if (selectedSize) {
            if (!quantity || isNaN(quantity)) {
                setCounter(1);
                saveSizeInput(1);
            } else {
                if (quantity - 1 + quantity >= totalProduct) {
                    toast.error("Cannot increment further. Total product limit reached.");
                    return;
                }
                setCounter(quantity);
                saveSizeInput(quantity);
            }
        }
    };

    const QuantityIncrementCounter = () => {
        if (selectedSize) {
            if (!quantity || isNaN(quantity)) {
                setQuantity(1);
            } else {
                setQuantity(quantity + 1);
            }
        }
    };
    const QuantityDecrementCounter = () => {
        if (selectedSize) {
            if (!quantity || isNaN(quantity)) {
                setQuantity(0);
            } else {
                setQuantity(quantity - 1);
            }
        }
    };

    // const decrementCounter = () => {
    //     if (selectedSize) {
    //         if (!quantity || isNaN(quantity)) {
    //             if (counter > 0) {
    //                 setCounter(1);
    //                 dispatch(decrementQuantity({ size: selectedSize }));
    //             }
    //         } else {
    //             if (counter > 0) {
    //                 setCounter(quantity);
    //                 dispatch(decrementQuantity({ size: selectedSize, quantity }));
    //             }
    //         }
    //     }
    // };

    const handleSizeSelection = (size) => {
        if (selectedSize === size) {
            setSelectedSize('');
        } else {
            setSelectedSize(size);
            document.getElementById('my_modal_5').showModal()
        }
    };

    const saveSizeInput = (quantityToSave) => {
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });

        const currentDate = new Date().toLocaleDateString();
        if (selectedSize && quantityToSave > 0) {
            const mtData = {
                size: selectedSize,
                quantity: quantityToSave,
                id: sewingPlanData.id,
                entry_time :currentTime,
                entry_date :currentDate,

            }
            console.log("sending data",mtData)
            axios.post(`${DjangoConfig.apiUrl}/rtqm/sewing_line_input/`, mtData
            ).then(response => {
                toast.success(`${response.data.message}`);
                dispatch(addOrder({ size: selectedSize, quantity: quantityToSave }));
                fetchSizeQuantityData()
                setQuantity(null)
            })
                .catch(error => {
                    console.error('Error fetching filtered data:', error);
                });

        }
        if (quantityToSave < 0) {
            dispatch(addOrder({ size: selectedSize, quantity: -1 }));
        }
    };

    const handelChangePLan = () => {
        // handleClearStore()
        navigate('/input-master/line-master');
    }


    const renderSizeButtons = () => {
        return sizeData.map((size, index) => {
            let sQuantity = 0
            if (Array.isArray(sizeQuantityData)) {
                const quantityObj = sizeQuantityData.find(item => item.size === size.sizeval);
                sQuantity = quantityObj ? quantityObj.quantity : 0;
                console.log("quantityObj", quantityObj);}

                const matchData = totalInput.find((so) => so.size === size.sizeval);
                const totalQuantity = matchData ? matchData.total_input_qty : 0;

            return (

                <div key={index} className="relative w-full bg-blue-500 p-4 h-20 mt-1 rounded-lg shadow-md">
                    {/* <p className="absolute text-white z-10">
                        {sQuantity}
                    </p> */}
                    <p className="absolute top-0 left-0 p-4 z-10 text-white text-lg">{totalQuantity}</p>
                    <p className="absolute top-0 right-0 p-4 z-10 text-white text-lg">{sQuantity}</p>
                    <button
                        className="absolute inset-0 w-full h-full text-white font-semibold bg-blue-600 hover:bg-blue-700 rounded-lg focus:outline-none"
                        onClick={() => handleSizeSelection(size.sizeval)}
                    >
                        {size.sizeval}
                    </button>
                </div>
            );
        });
    };


    return (
        <div className="flex flex-col w-full h-full border rounded-md p-4 m-2">
            <div className="flex justify-evenly">
                <div className="border-2 w-full items-center pb-2">
                    <p className="text-sm font-medium">Buyer</p>
                    <p className="text-sm">{sewingPlanData.buyer_name}</p>
                </div>
                <div className="border-2 w-full items-center pb-2">
                    <p className="text-sm font-medium">Style</p>
                    <p className="text-sm">{sewingPlanData.styleno}</p>
                </div>
                {/* <div className="border-2 w-full items-center pb-2">
                    <p className="text-sm font-medium"></p>
                    <p className="text-sm">{sewingPlanData.buyer}</p>
                </div> */}
                <div className="border-2 w-full items-center pb-2">
                    <p className="text-sm font-medium">Color</p>
                    <p className="text-sm">{sewingPlanData.color}</p>
                </div>
                <div className="border-2 w-full items-center pb-2">
                    
                    <p className="text-sm font-medium">Total Quantity</p>
                    <p className="text-sm">{sewingPlanData.quantity}</p>
                </div>
            </div>
            <div className="flex justify-normal w-full h-72 black-border-1 mt-2">
                <div className="w-full">
                    <div className='flex flex-wrap mt-1 bg-slate-100 justify-between'>
                    <div className='flex flex-wrap w-auto  justify-around'>
                            <div className='w-44 flex justify-around'>
                                <p >Total Input Pieces : </p>
                                <badge>{totalQuantityInput}</badge>
                            </div>
                            <div className='w-44 flex justify-around'>
                                <p >Total Add Now : </p>
                                <badge>{totalQuantityBackEnd}</badge>
                            </div>
                        </div>
                       
                        <div>
                            {/* <button className='btn  btn-primary w-24 float-end' onClick={handleClearStore}> clear </button> */}
                        </div>
                    </div>
                    <div className="gap-2">
                        <div className="px-4 py-3  rounded">
                            {sizeData.length > 0 ? (
                                <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                                    {renderSizeButtons()}
                                </div>
                            ) : (
                                <p>No size data available</p>
                            )}
                        </div>
                    </div>
                    <div className="w-full mt-10  justify-around">
                        <button className="px-4 py-2 bg-blue-900 w-28 float-end text-white rounded hover:bg-blue-600 mr-2" onClick={handelChangePLan}>
                            Change Plan
                        </button>
                    </div>

                    <dialog id="my_modal_5" className="modal modal-bottom sm:modal-middle">
                        <div className="modal-box p-4">
                            <h3 className="font-bold text-lg">Size: {selectedSize}</h3>

                            <div className="flex items-center mt-4 w-full">
                                <input
                                    type="number"
                                    value={quantity}
                                    onChange={handleQuantityChange}
                                    className="border rounded py-1 px-2 text-center flex-grow mr-2"
                                />
                            </div>
                            <div className="flex items-center mt-4">
                                <button
                                    className="w-full py-2 bg-blue-900 text-white rounded hover:bg-blue-600"
                                    onClick={QuantityIncrementCounter}
                                >
                                    +
                                </button>
                                <button
                                    className="w-full py-2 bg-red-700 text-white rounded hover:bg-blue-600 ml-2"
                                    onClick={QuantityDecrementCounter}
                                >
                                    -
                                </button>
                            </div>

                            <div className="flex justify-end mt-4">
                                <form method="dialog">

                                    <button
                                        className="px-4 py-2 bg-blue-900 text-white rounded hover:bg-blue-600 mr-2"
                                        onClick={incrementCounter}
                                    >
                                        Save
                                    </button>
                                    <button className="btn">Close</button>
                                </form>
                            </div>
                        </div>
                    </dialog>

                </div>
            </div>
        </div>

    );
};

export default SelectQuantityByLineMaster;



