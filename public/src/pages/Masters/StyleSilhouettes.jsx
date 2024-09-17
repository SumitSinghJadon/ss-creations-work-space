import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import DjangoConfig from '../../config/Config';
import Skeleton from 'react-loading-skeleton';
import Select from 'react-select';
import { toast } from 'react-toastify';

const StyleSilhouettes = () => {
    const navigate = useNavigate();
    const [frontImageUrl, setFrontImageUrl] = useState('');
    const [backImageUrl, setBackImageUrl] = useState('');
    const [frontSketchImageUrl, setFrontSketchImageUrl] = useState('');
    const [backSketchImageUrl, setBackSketchImageUrl] = useState('');
    const [buyerList, setBuyerList] = useState([]);
    const [styleNoData, setStyleNoData] = useState([]);
    const [selectedBuyer, setSelectedBuyer] = useState(null);
    const [selectedStyle, setSelectedStyle] = useState(null);
    const [isLoading, setIsLoading] = useState(false);





    const handleFileChange = async (event, setImageUrl, setSketchImageUrl) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('image', file);

            try {
                const response = await axios.post(`${DjangoConfig.apiUrl}/rtqm/qms_defect_process/`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (response.status === 200) {
                    const imageUrl = URL.createObjectURL(file);
                    setImageUrl(imageUrl);

                    // const normalizedSketchImageUrl = response.data.sketch_image_url.replace(/\\/g, '/');
                    const sketchImagePath = response.data.sketch_image_url;
                    const sketchImageUrl = `${DjangoConfig.apiUrl}${sketchImagePath}`;
                    setSketchImageUrl(sketchImagePath);
                    console.log(sketchImageUrl)
                } else {
                    console.error('Failed to process image:', response.statusText);
                }
            } catch (error) {
                console.error('Error processing image:', error);
            }
        }
    };

    const handleFrontFileChange = (event) => {
        handleFileChange(event, setFrontImageUrl, setFrontSketchImageUrl);
    };

    const handleBackFileChange = (event) => {
        handleFileChange(event, setBackImageUrl, setBackSketchImageUrl);
    };

    const handleSave = async () => {
        if (!selectedBuyer || !selectedStyle || !frontSketchImageUrl || !backSketchImageUrl) {
            alert('Please fill all fields');
            return;
        }
        const formData = new FormData();
        // formData.append('front_image', frontSketchImageUrl.replace(/\\/g, '/')); 
        // formData.append('back_image', backSketchImageUrl.replace(/\\/g, '/')); 
        formData.append('front_image', frontSketchImageUrl);
        formData.append('back_image', backSketchImageUrl);
        formData.append('buyer', selectedBuyer.value);
        formData.append('style_no', selectedStyle.value);

        try {
            const response = await axios.post(`${DjangoConfig.apiUrl}/rtqm/style_silhouettes/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.status === 201) {
                toast.success('Data Saved successful!');

            } else {
                console.error('Failed to save data:', response.statusText);
                toast.error('Failed to save data');

            }
        } catch (error) {
            console.error('Error saving data:', error);
            alert('Error saving data');
        }
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
            const uniqueStyles = [...new Set(responseData.map(item => item.styleno))];
            const styleOptions = uniqueStyles.map(style => ({ value: style, label: style }));
            setStyleNoData(styleOptions);
            setIsLoading(false);
        })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
    };

    const getPageSilhouettesList = () => {
        navigate('/dashboard/master/silhouettes-list')
    }


    return (
        <div className="flex flex-col items-center w-full  justify-center h-screen bg-gray-100">
            <div className='flex justify-between w-full'>
            <h1 className="text-3xl font-bold mb-8">Upload  Style Silhouettes</h1>
            <button className='btn btn-outline' onClick={getPageSilhouettesList}>Silhouettes History</button>

            </div>
           
            <div className="bg-white p-6 rounded-lg shadow-md w-full h-full ">
                <div className="mb-2 flex justify-around ">
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
                            onChange={setSelectedStyle}
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
                        <label className="block mb-2 font-bold text-gray-700">Upload Front Side Image:</label>
                        <input type="file" onChange={handleFrontFileChange} />
                    </div>
                    <div>
                        <label className="block mb-2 font-bold text-gray-700">Upload Back Side Image:</label>
                        <input type="file" onChange={handleBackFileChange} />
                    </div>
                </div>
                <button
                    onClick={handleSave}
                    className="px-4 py-2 float-end bg-blue-500 center text-white rounded hover:bg-blue-600 focus:outline-none"
                >
                    Save
                </button>
            </div>
        </div>
    );
};

export default StyleSilhouettes;


