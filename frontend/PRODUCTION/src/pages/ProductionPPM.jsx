import React, { useState, useEffect } from 'react';
import { Select, MenuItem, TextField, Button, Typography } from '@mui/material';
import { FaBars } from 'react-icons/fa';
import { useSelector } from 'react-redux';
import api from '../auth/api';
import LogOut from '../auth/logOut';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import { toast } from 'react-toastify';


const today = new Date();

// Format the date (e.g., YYYY-MM-DD)
const formattedDate = today.toISOString().split('T')[0];


function ButtonField(props) {
  const {
    setOpen,
    label,
    id,
    disabled,
    InputProps: { ref } = {},
    inputProps: { 'aria-label': ariaLabel } = {},
  } = props;

  return (
    <Button
      variant="outlined"
      id={id}
      disabled={disabled}
      ref={ref}
      aria-label={ariaLabel}
      onClick={() => setOpen?.((prev) => !prev)}
    >
      {label ? `${label}` : 'Pick a date'}
    </Button>
  );
}

function ButtonDatePicker(props) {
  const [open, setOpen] = React.useState(false);

  return (
    <DatePicker
      slots={{ ...props.slots, field: ButtonField }}
      slotProps={{ ...props.slotProps, field: { setOpen } }}
      {...props}
      open={open}
      onClose={() => setOpen(false)}
      onOpen={() => setOpen(true)}
      minDate={props.minDate}
      maxDate={props.maxDate}
    />
  );
}

const ProductionPPM = () => {
  const [planData, setPlanData] = useState([])
  const [planDataShow, setPlanDataShow] = useState([])

  const [datevalue, setDateValue] = useState(dayjs(formattedDate));

  const [optionsBuyer, setOptionsBuyer] = useState([]);
  const [optionsStyle, setOptionsStyle] = useState([]);
  const [optionsOrder, setOptionsOrder] = useState([]);
  const [optionsProcess, setOptionsProcess] = useState([]);
  const [optionsProduct, setOptionsProduct] = useState([]);
  const [optionsComponent, setOptionsComponent] = useState([]);
  const [optionsSubComp, setOptionsSubComp] = useState([]);
  const [selectedValues, setSelectedValues] = useState({
    selectedBuyer: null,
    selectedStyle: null,
    selectedOrder: null,
    selectedDate: datevalue,
    selectedProcess: null,
    selectedProduct: null,
    selectedComp: null,
    selectedSubComp: null,
    ProcessNo: null,
    ProcessRate: null,
    ProductRate: null,
  });
  const navigate = useNavigate();

  console.log("date", selectedValues.selectedDate)


  const updateSelectedDate = (newDate) => {
    // setSelectedValues(prevValues => ({
    //   ...prevValues,
    //   selectedDate: dayjs(newDate) 
    //    // Convert newDate to dayjs instance
    // }));
    setDateValue(newDate);
  };


  const { access } = useSelector((state) => state.auth);
  const { unitId } = useSelector((state) => state.auth)




  console.log("accessToken", access);
  console.log("unitId", unitId)

  useEffect(() => {
    if (access) {
      const fetchUserData = async () => {
        try {
          // Use the API utility to fetch user details
          const response = await api.get('/user/');
          console.log("sumit", response.data);
          setLocation(response.data.location);
        } catch (err) {
          console.log('Failed to fetch user details.');
        }
      };

      fetchUserData();
    } else {
      navigate('/');
    }
  }, [access]);



  const handleChange = (field, value) => {
    setSelectedValues((prevValues) => ({
      ...prevValues,
      [field]: value,
    }));
  };


  // ====================================data get for mt start=======================================

  useEffect(() => {
    if (selectedValues.selectedStyle != null) {
      console.log('Selected style:', selectedValues.selectedStyle);
      axios.get('http://127.0.0.1:8000/api/ourref/', {
        params: {
          'styleno': selectedValues.selectedStyle
        }
      })
        .then(response => {
          console.log('response.data.filterdata:', response.data.filterdata);
          const transformedOptions = response.data.filterdata.map(item => ({
            value: item.ourref,
            label: item.ourref,
          }));
          setOptionsOrder(transformedOptions || []);

        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }
  }, [selectedValues.selectedStyle])



  useEffect(() => {
    if (selectedValues.selectedBuyer != null) {
      console.log('Selected Buyers:', selectedValues.selectedBuyer);
      axios.get('http://127.0.0.1:8000/api/style/', {
        params: {
          'buyer_code': selectedValues.selectedBuyer
        }
      })
        .then(response => {
          console.log('response.data.filterdata:', response.data.filterdata);
          const transformedOptions = response.data.filterdata.map(item => ({
            value: item.styleno,
            label: item.styleno,
          }));
          setOptionsStyle(transformedOptions || []);

        })
        .catch(error => {
          console.error('Error fetching data:', error);

        });
    }

  }, [selectedValues.selectedBuyer])

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/buyer/')
      .then(response => {
        const transformedOptions = response.data.filterdata.map(item => ({
          value: item.buyer_code,
          label: item.buyer_name,
        }));
        setOptionsBuyer(transformedOptions || []);


      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  console.log('buyer', optionsBuyer);
  // =======================================data get for mt end=========================================

  // =========================================data get for dt start=========================================

  useEffect(() => {
    if (selectedValues.selectedComp != null) {
      console.log('selectedComp:', selectedValues.selectedComp);
      axios.get('http://127.0.0.1:8000/api/subcomp/', {
        params: {
          'component_id': selectedValues.selectedComp
        }
      })
        .then(response => {
          console.log('response.data.filterdata:', response.data.filterdata);
          const transformedOptions = response.data.data.map(item => ({
            value: item.id,
            label: item.name,
          }));
          setOptionsSubComp(transformedOptions || []);

        })
        .catch(error => {
          console.error('Error fetching data:', error);

        });
    }

  }, [selectedValues.selectedComp])

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/process/')
      .then(response => {
        const transformedOptions = response.data.data.map(item => ({
          value: item.id,
          label: item.name,
        }));
        setOptionsProcess(transformedOptions || []);


      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/product/')
      .then(response => {
        const transformedOptions = response.data.data.map(item => ({
          value: item.id,
          label: item.name,
        }));
        setOptionsProduct(transformedOptions || []);


      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);



  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/component/')
      .then(response => {
        const transformedOptions = response.data.data.map(item => ({
          value: item.id,
          label: item.name,
        }));
        setOptionsComponent(transformedOptions || []);


      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);
  // ==========================================data get for dt end=========================================



    
// ===================================================input required check code start=========================================
const validateForm = () => {
  const newErrors = {};
  if (!selectedValues.selectedBuyer) newErrors.selectedBuyer = 'Buyer No. is required';
  if (!selectedValues.selectedStyle) newErrors.selectedStyle = 'Style No. is required';
  if (!selectedValues.selectedOrder) newErrors.selectedOrder = 'Order No is required';
  if (!selectedValues.selectedDate) newErrors.selectedDate = 'Date is required';
  if (!selectedValues.selectedProcess) newErrors.selectedProcess = 'Process is required';
  if (!selectedValues.selectedProduct) newErrors.selectedProduct = 'Product is required';
  if (!selectedValues.selectedComp) newErrors.selectedComp = 'Component is required';
  if (!selectedValues.selectedSubComp) newErrors.selectedSubComp = 'Subcomponent is required';
  if (selectedValues.ProcessNo === '') newErrors.ProcessNo = 'Process No. is required';
  if (selectedValues.ProcessRate === '') newErrors.ProcessRate = 'Process Rate is required';
  if (selectedValues.ProductRate === '') newErrors.ProductRate = 'Product Rate is required';

  return newErrors;
};

const showButtonValidate = () => {
  const newErrors = {};
  if (!selectedValues.selectedBuyer) newErrors.selectedBuyer = 'Buyer No. is required';
  if (!selectedValues.selectedStyle) newErrors.selectedStyle = 'Style No. is required';
  if (!selectedValues.selectedOrder) newErrors.selectedOrder = 'Order No is required';
  if (!selectedValues.selectedDate) newErrors.selectedDate = 'Date is required';
  return newErrors;
}
  
// ===============================================input required check code end=============================



  // ===========================================data insert start=========================================
  const handleSubmit = () => {
    const validationErrors = validateForm();
    if (Object.keys(validationErrors).length > 0) {
      const errorMessages = Object.values(validationErrors).join('\n');
      toast.error(errorMessages);
      return;
    }
    console.log("selected value", selectedValues)
    const data = {
      component_id: selectedValues.selectedComp,
      process_id: selectedValues.selectedProcess,
      product_type_id: selectedValues.selectedProduct,
      sub_component_id: selectedValues.selectedSubComp,
      process_no: selectedValues.ProcessNo,
      process_rate: selectedValues.ProcessRate,
      product_rate: selectedValues.ProductRate,
    }

    const isDuplicate = planData.some(item => item.process_id === data.process_id);

    if (isDuplicate) {
      // Show an error message
      toast.error("Error: A record with this process already exists.")
      return; // Stop further execution
    }
    setPlanData(prevData => [...prevData, data]);
    setPlanDataShow([])

  }
  console.log("planData", planData)
  console.log("planDataShow", planDataShow)
  const getLabelFromOptions = (id, options) => {
    const option = options.find(option => option.value === id);
    return option ? option.label : 'Unknown';
  };

  const handleDeleteRow = (index) => {
    setPlanData(prevData => prevData.filter((_, i) => i !== index));
    console.log("planData sumit", index)
  };

  const handleSave = () => {

    const formattedDate = selectedValues.selectedDate ? dayjs(selectedValues.selectedDate).format('YYYY-MM-DD') : null
    const datess = String(formattedDate)
    const data = {
      'buyer': selectedValues.selectedBuyer,
      'style': selectedValues.selectedStyle,
      'ourref': selectedValues.selectedOrder,
      'date': datess,
      'location': unitId,
      'planData': planData
    };
    console.log("data", data)

    axios.post('http://127.0.0.1:8000/api/ppm/', data)
      .then(response => {
          // Successful response
          alert("Data Saved Successfully");
          setPlanData([]);   
      })
      .catch(error => {
        console.error("There was an error saving the data!", error);
        if (error.response && error.response.data && error.response.data.error) {
          toast.error(error.response.data.error); // Display error from backend
        } else {
          alert("An unexpected error occurred. Please try again."); // Fallback error message
        }
      });    
  }
  // =============================================data insert end=========================================





  // =============================================data show code start=========================================
  const handleShow = () => {
    const validationErrors = showButtonValidate();
    if (Object.keys(validationErrors).length > 0) {
      const errorMessages = Object.values(validationErrors).join('\n');
      toast.error(errorMessages);
      return;
    }

    console.log("selected value", selectedValues)
    const formattedDate = selectedValues.selectedDate ? dayjs(selectedValues.selectedDate).format('YYYY-MM-DD') : null
    const datess = String(formattedDate)

    axios.get('http://127.0.0.1:8000/api/ppmShow/', {
      params: {
        'buyer': selectedValues.selectedBuyer,
        'style': selectedValues.selectedStyle,
        'ourref': selectedValues.selectedOrder,
        'date': datess
      }
    }).then(response => {
      console.log(response.data)
      const { prod_proc_plan_dt } = response.data;
      // Update the state with the fetched data
      setPlanDataShow(prod_proc_plan_dt);
    })
    setPlanData([])

  }
  // =============================================data show code end=========================================

  // =============================================process delete code start=========================================

  const  handleDeletedata = (index) => {
    axios.post('http://127.0.0.1:8000/api/ppmDelete/', index)
    .then(response => {
        // Successful response
        alert(response.data.message);
        handleShow()
    })
    .catch(error => {
      console.error("error!", error);
    });   

  };

// ==================================================process delete code end=========================================





  return (
    <div className="bg-gray-100 w-full min-h-screen">
      {/* Header Row */}
      {/* Form Section */}
      <div className="w-full bg-white shadow-md p-4">
        <p className="text-gray-600 mb-2">Ship Style/Orders</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 xl:grid-cols-7 gap-3 mb-6">
          <TextField
            select
            label="Buyer No."
            value={selectedValues.selectedBuyer}
            onChange={(e) => handleChange("selectedBuyer", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"
            required

          >
            {optionsBuyer.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Style No."
            value={selectedValues.selectedStyle}
            onChange={(e) => handleChange("selectedStyle", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"
            required
            disabled={selectedValues.selectedBuyer === null}

          >
            {optionsStyle.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Order No"
            value={selectedValues.selectedOrder}
            onChange={(e) => handleChange("selectedOrder", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"
            required
            disabled={selectedValues.selectedStyle === null}

          >
            {optionsOrder.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <ButtonDatePicker
              label={datevalue == null ? null : datevalue.format('MM/DD/YYYY')}
              value={selectedValues.selectedDate}
              onChange={updateSelectedDate}
              required
            // minDate={dayjs(row.original.orderdate)}
            // maxDate={dayjs(row.original.delvdate)}

            />
          </LocalizationProvider>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleShow}
          >
            Show
          </Button>
          <Button
            variant="contained"
            color="success"
            fullWidth
            onClick={handleSubmit}
          >
            Insert
          </Button>
          <Button
            variant="contained"
            color="error"
            fullWidth
          >
            Remove
          </Button>
        </div>

        {/* Additional Form Section */}
        <div className="lg:grid grid-cols-1 text-sm text-gray-700 font-bold rounded shadow md:grid-cols-2 lg:grid-cols-7 hidden gap-10 mb-2 py-1 px-2 bg-green-100">
          <p>Process</p>
          <p>Product</p>
          <p>Component</p>
          <p>Subcomponent</p>
          <p>Process No.</p>
          <p>Process Rate</p>
          <p>Product Rate</p>

        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 xl:grid-cols-7 gap-3 mb-6">
          <TextField
            select
            label="Process"
            value={selectedValues.selectedProcess}
            onChange={(e) => handleChange("selectedProcess", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"
          >
            {optionsProcess.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="product"
            value={selectedValues.selectedProduct}
            onChange={(e) => handleChange("selectedProduct", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"

          >
            {optionsProduct.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Component"
            value={selectedValues.selectedComp}
            onChange={(e) => handleChange("selectedComp", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"

          >
            {optionsComponent.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Subcomponent"
            value={selectedValues.selectedSubComp}
            onChange={(e) => handleChange("selectedSubComp", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"
            disabled={selectedValues.selectedComp === null}

          >
            {optionsSubComp.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            type="number"
            label="Process No."
            value={selectedValues.ProcessNo}
            onChange={(e) => handleChange("ProcessNo", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"

          />
          <TextField
            type="number"
            label="Process Rate"
            value={selectedValues.ProcessRate}
            onChange={(e) => handleChange("ProcessRate", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"

          />
          <TextField
            type="number"
            label="Product Rate"
            value={selectedValues.ProductRate}
            onChange={(e) => handleChange("ProductRate", e.target.value)}
            fullWidth
            variant="outlined"
            className="custom-height"
          />
        </div>
      </div>
      {/* Additional Form Section */}
      <div className="p-4">
        {/* Responsive wrapper */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-900">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Process</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Component</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sub Component</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Process No</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Process Rate</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product Rate</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500 tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {planData.map((item, index) => (
                <tr key={item.id || index}> {/* Use item.id or index if id is missing */}
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {getLabelFromOptions(item.process_id, optionsProcess)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {getLabelFromOptions(item.product_type_id, optionsProduct)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {getLabelFromOptions(item.component_id, optionsComponent)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {getLabelFromOptions(item.sub_component_id, optionsSubComp)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.process_no}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.process_rate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.product_rate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button
                      onClick={() => handleDeleteRow(index)} // Use index if id is not available
                      className="text-red-600 hover:text-red-800 font-medium"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {planDataShow.map((item) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.process}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.product_type}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.component}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.sub_component}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.process_no}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.process_rate}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.product_rate}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button
                      onClick={() => handleDeletedata(item.id)} // Use index if id is not available
                      className="text-red-600 hover:text-red-800 font-medium"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Save Button */}
        <div className="mt-4">
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600"
          >
            Save
          </button>
        </div>
      </div>



    </div>
  );
};

export default ProductionPPM;