import { Box, Button, Menu, MenuItem } from '@mui/material';
import { useEffect, useState} from 'react';
import { useLocation } from 'react-router-dom';
import { MaterialReactTable, createMRTColumnHelper, useMaterialReactTable } from 'material-react-table';

import axios from 'axios';


const ViewSavedExeclData = () => {
    const [isLoading, setIsLoading] = useState(false)
    const [obShowData, setObShowData] = useState([])
    const location = useLocation();
    const { id } = location.state || {};

    const columnHelper = createMRTColumnHelper();
    const columns = [
        columnHelper.accessor((row, index) => index + 1, { header: 'S/N', size: 40 }),
        columnHelper.accessor('ob_no', { header: 'OB/NO', size: 20 }),
        columnHelper.accessor('parts', { header: 'SECTION', size: 20 }),
        columnHelper.accessor('operation', { header: 'OPERATION NAME', size: 20 }),
        columnHelper.accessor('sam', { header: 'SAM', size: 20 }),
        columnHelper.accessor('type_of_machine', { header: 'TYPE OF M/Cs', size: 20 }),
        columnHelper.accessor('attachments', { header: 'ATTACHMENT', size: 20 }),
        columnHelper.accessor('theoretical_manpower', { header: 'THEO. OPTRS ', size: 20 }),
        columnHelper.accessor('planned_work_station', { header: 'THEO. BAL. OPTRS', size: 20 }),
        columnHelper.accessor('target_100_pcs', { header: 'TGT @100%', size: 20 }),
        columnHelper.accessor('target_60_pcs', { header: 'TGT @60%', size: 20 }),
        columnHelper.accessor('seam_length', { header: 'Seam Length', size: 20 }),
        columnHelper.accessor('remark', { header: 'Remarks', size: 20 }),
    ];

    const table = useMaterialReactTable({
        columns,
        data: obShowData,

        // enableRowSelection: true,
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
            />
        ),
    });


    useEffect(() => {
        console.log("sumitID=",id)
        if (id) {
            fetchObDetails(id);
        }
    }, [id]);
    const fetchObDetails = async (id) => {
        try {
            const response = await axios.get(`http://localhost:8000/rtqm/ob_details_show/?id=${id}`);
            console.log(response.data.ob_show_data);
            setObShowData(response.data.ob_show_data);
            setIsLoading(true)
        } catch (error) {
            console.error('There was an error!', error);
        }
    };
    
    return(
        <>
         <div className='mt-2'>
                <MaterialReactTable table={table} />
            </div>
        
        </>
    );

}


export default ViewSavedExeclData;