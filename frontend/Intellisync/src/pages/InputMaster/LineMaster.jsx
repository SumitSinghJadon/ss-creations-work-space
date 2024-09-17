import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import axios from 'axios';
import { Box, Button, Menu, MenuItem } from '@mui/material';
import { MaterialReactTable, createMRTColumnHelper, useMaterialReactTable } from 'material-react-table';
import Skeleton from 'react-loading-skeleton';
import { toast } from 'react-toastify';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import DjangoConfig from '../../config/Config';
import { saveRows } from '../../utils/slice/SewingInputSlice';
const LineMaster = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const userData = useSelector(state => state.User.userData);
    const [tableData, setTableData] = useState([])

    console.log("userData", userData)

    useEffect(() => {
        fetchPlaningData();

    }, [])


    const fetchPlaningData = () => {
        const userData2 = {
            line_id: userData.id,
        };
        const queryParams = new URLSearchParams(userData2).toString();
        axios.get(`${DjangoConfig.apiUrl}/rtqm/qms_planing2/?${queryParams}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                const responseData = response.data.planing_data
                setTableData(responseData)
            })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
            });
    };
    console.log("TableData",tableData)

    const handleExportRows = (rows) => {
        try {
            if (rows && rows.length > 0 && rows[0].original) {
                const rowData = rows[0].original;
                // console.log("rowData",rowData)
                dispatch(saveRows(rowData));
                console.log("Planing Data",rowData)
                // toast.success(`${response.data.message}`);
                navigate('/input-master/select-quantity-by-master');
            } else {
                console.error('Invalid rows or missing "original" property');
            }
        } catch (error) {
            console.error('Error saving rows:', error);
        }
    };
    
     




    const columnHelper = createMRTColumnHelper();
    const columns = [
        columnHelper.accessor((row, index) => index + 1, { header: 'S/N', size: 40 }),
        columnHelper.accessor('buyer', { header: 'Buyer', size: 20 }),
        columnHelper.accessor('styleno', { header: 'Style No', size: 20 }),
        columnHelper.accessor('color', { header: 'Color ', size: 20 }),
        columnHelper.accessor('quantity', { header: 'Quantity', size: 20 }),
        columnHelper.accessor('delvdate', { header: 'Delivery Date', size: 20 }),
    ];



    const table = useMaterialReactTable({
        columns,
        data: tableData,
        enableMultiRowSelection: false, //shows radio buttons instead of checkboxes
        enableRowSelection: true,
        columnFilterDisplayMode: 'popover',
        paginationDisplayMode: 'pages',
        positionToolbarAlertBanner: 'bottom',
        renderTopToolbarCustomActions: ({ table }) => (
            <Box
                sx={{
                    display: 'flex',
                    gap: '10px',
                    padding: '4px',
                    flexWrap: 'wrap',
                }}
            >
                <Button
                    disabled={!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()}
                    onClick={() => handleExportRows(table.getSelectedRowModel().rows)}
                    startIcon={<FileDownloadIcon />}
                >
                    Save Data
                </Button>
            </Box>
        ),
    });
    

    return (
        <div>

            <div className='mt-2'>
                <MaterialReactTable table={table} />
            </div>

        </div>
    );
};

export default LineMaster;
