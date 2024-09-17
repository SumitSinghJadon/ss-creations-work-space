import { Box, Button, Menu, MenuItem } from '@mui/material';
import axios from 'axios';
import { download, generateCsv, mkConfig } from 'export-to-csv';
import { MaterialReactTable, createMRTColumnHelper, useMaterialReactTable } from 'material-react-table';
import React, { useEffect, useState } from 'react'
import Skeleton from 'react-loading-skeleton';
import { toast } from 'react-toastify';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import DjangoConfig from '../../config/Config';
import { useNavigate } from 'react-router-dom';

const ObHistory = () => {
    const [isLoading, setIsLoading] = useState(false)
    const [obData, setObData] = useState([])
    const navigate = useNavigate()


    const usStates = [
        { value: '37.33999999999999', label: 'mil gaya' },
        { value: 'AK', label: 'Alaska' },
        { value: 'AZ', label: 'Arizona' },
        { value: 'AR', label: 'Arkansas' },
        { value: 'CA', label: 'California' },
    ];
    const validationErrors = {
        state: 'Please select a state', 
    };

    const columnHelper = createMRTColumnHelper();
    const columns = [
        columnHelper.accessor((row, index) => index + 1, { header: 'S/N', size: 40 }),
        columnHelper.accessor('ob_no', { header: 'OB NO', size: 20 }),

        columnHelper.accessor('buyer_name', { header: 'Buyer', size: 20 }),
        columnHelper.accessor('style', { header: 'Style ', size: 20 }),
        columnHelper.accessor('color', { header: 'Color', size: 20 }),
        columnHelper.accessor('line_sum', { header: 'Total Ob', size: 20 }),
        columnHelper.accessor('line_sam', { header: 'Line Sam', size: 20 }),
        columnHelper.accessor('total_sam', {
            accessorKey: 'total_sam', 
            header: 'Total Line Sam', 
            size: 20,
            editVariant: 'select', 
            editSelectOptions: usStates, 
            muiEditTextFieldProps: { 
                select: true,
                error: !!validationErrors?.state,
                helperText: validationErrors?.state,
            },
        }),
        columnHelper.accessor('ob_date', {
            header: 'Ob Date',
            size: 20,
            cellRenderer: (row) => {
                const datetimeString = row.value; // Assuming row.value is '2024-07-15T07:39:05.690Z'
                const dateOnly = datetimeString.substring(0, 10); // Extract YYYY-MM-DD
                return dateOnly; // This will display '2024-07-15'
            },
        }),

    ];

    const csvConfig = mkConfig({
        fieldSeparator: ',',
        decimalSeparator: '.',
        useKeysAsHeaders: true,
    });


    const handleExportRows = (rows) => {
        const rowData = rows.map((row) => row.original);
        const csv = generateCsv(csvConfig)(rowData);
        download(csvConfig)(csv);
    };

    const handleExportData = () => {
        const csv = generateCsv(csvConfig)(obData);
        download(csvConfig)(csv);
    };









    // -----for DropDown-------------------->
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };
    //----------end DropDown---------------->

    const table = useMaterialReactTable({
        columns,
        data: obData,
        // state: {
        //   isLoading:  isLoading ? <Skeleton count={5} /> : null,

        // },
        enableRowSelection: true,
        editDisplayMode: 'modal',
        getRowId: (row) => row.id,
                muiToolbarAlertBannerProps: isLoading
                ? {
                    color: 'error',
                    children: 'Error loading data',
                    }
                : undefined,
                muiTableContainerProps: {
                sx: {
                    minHeight: '100px',
                },
                },
        columnFilterDisplayMode: 'popover',
        paginationDisplayMode: 'pages',
        positionToolbarAlertBanner: 'bottom',
        // editDisplayMode: 'row', // ('modal', 'cell', 'table', and 'custom' are also available)
        enableEditing: true,
        muiTableBodyCellProps: {
            sx: {
              border: '1px solid rgba(81, 81, 81, .5)',
            },
          },
        renderTopToolbarCustomActions: ({ table }) => (
            <Box
                sx={{
                    display: 'flex',
                    gap: '10px',
                    padding: '4px',
                    flexWrap: 'wrap',
                    style: { fontSize: '5px' },
                }}
            >

                <Button
                    aria-controls="export-menu"
                    aria-haspopup="true"
                    onClick={handleClick}
                    startIcon={<FileDownloadIcon />}
                >
                    Export
                </Button>
                <Menu
                    id="export-menu"
                    anchorEl={anchorEl}
                    keepMounted
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                >
                    <MenuItem onClick={handleExportData}>Export All Data</MenuItem>
                    <MenuItem
                        disabled={table.getPrePaginationRowModel().rows.length === 0}
                        onClick={() => handleExportRows(table.getPrePaginationRowModel().rows)}
                    >
                        Export All Rows
                    </MenuItem>
                    <MenuItem
                        disabled={table.getRowModel().rows.length === 0}
                        onClick={() => handleExportRows(table.getRowModel().rows)}
                    >
                        Export Page Rows
                    </MenuItem>
                </Menu>

            </Box>
        ),
    });
    // ------------Columns data end--------------------->

    useEffect(() => {
        fetchDefectData();
    }, []);

    const fetchDefectData = () => {
        axios.get(`${DjangoConfig.apiUrl}/rtqm/ob_mt_data/`)
            .then(response => {
                console.log(response.data);
                setObData(response.data.ob_mt_data);
                setIsLoading(true)
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };
    const UploadObPage = () => {
        navigate('/dashboard/master/operation-master')
    }


    return (
        <div>
            <div className='w-full h-10 flex items-center justify-end  rounded-lg'>
                <Button
                    onClick={UploadObPage}
                    variant="contained"
                    color="primary"
                    className="float-right mr-2"
                >
                    Upload Ob
                </Button>
            </div>

            <div className='mt-2'>
                <MaterialReactTable table={table} />
            </div>


        </div>
    )
}

export default ObHistory

