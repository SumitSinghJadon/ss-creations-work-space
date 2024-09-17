import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import DjangoConfig from '../config/Config';
import MenuMaster from './MenuMaster';

const Sidebar = ({ isOpen }) => {
  const [openDropdownId, setOpenDropdownId] = useState(null);
  const [menuMaster, setMenuMaster] = useState([])

  const toggleDropdown = (dropdownId) => {
    setOpenDropdownId(openDropdownId === dropdownId ? null : dropdownId);
  };
  const [openMenuId, setOpenMenuId] = useState(null);

  const toggleMenu = (menuId) => {
    if (openMenuId === menuId) {
      setOpenMenuId(null); // Close menu if already open
    } else {
      setOpenMenuId(menuId); // Open the selected menu
    }
  };

  // useEffect(() => {
  //   fetchDefectData();
  // }, []);

  // const fetchDefectData = () => {
  //   axios.get(`${DjangoConfig.apiUrl}/rtqm/home/`)
  //     .then(response => {
  //       console.log(response.data)
  //       setMenuMaster(response.data.menu)

  //     })
  //     .catch(error => {
  //       console.error('Error:', error);
  //     });
  // };

  const organizedMenu = menuMaster.reduce((acc, item) => {
    if (item.parent_id === null) {
      acc[item.id] = { ...item, submenus: [] }; 
    } else {
      if (acc[item.parent_id]) {
        acc[item.parent_id].submenus.push(item); 
      }
    }
    return acc;
  }, {});
  return (
    <div className={`${isOpen ? 'w-50' : 'w-10'} transition-all duration-300 text-black h-screen p-4`}>

     {/* <MenuMaster/> */}
{/* 
      {isOpen && (
        <>
          <ul className="space-y-2">

            <li>
              <button
                id="orderDropdownBtn"
                onClick={() => toggleDropdown('orderDropdown')}
                className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
              >
                Order
                <svg
                  className={`h-6 w-6 ml-auto transition-transform ${openDropdownId === 'orderDropdown' ? 'transform rotate-180' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M6 8l4 4 4-4H6z" />
                </svg>
              </button>
              {openDropdownId === 'orderDropdown' && (
                <ul className="pl-8 mt-2 space-y-2">
                  <li>
                    <Link to="rtqm/order-process-plan-mt" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Order Process Plan MT
                    </Link>
                  </li>
                  <li>
                    <Link to="rtqm/order-process-plan-dt" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Order Process Plan DT
                    </Link>
                  </li>

                </ul>
              )}
            </li>

            <li>
              <button
                id="mastersDropdownBtn"
                onClick={() => toggleDropdown('mastersDropdown')}
                className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
              >
                Masters
                <svg
                  className={`h-6 w-6 ml-auto transition-transform ${openDropdownId === 'mastersDropdown' ? 'transform rotate-180' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M6 8l4 4 4-4H6z" />
                </svg>
              </button>
              {openDropdownId === 'mastersDropdown' && (
                <ul className="pl-8 mt-2 space-y-2">
                  <li>
                    <Link to="master/ob-history" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Operation Master
                    </Link>
                  </li>
                  <li>
                    <Link to="master/defect-master" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Defect Master
                    </Link>
                  </li>
                  <li>
                    <Link to="/dashboard/master/style-silhouettes" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Style Silhouettes
                    </Link>
                  </li>
                  <li>
                    <Link to="master/sift-master" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Shift Master
                    </Link>
                  </li>
                  <li>
                    <Link to="master/process-master" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Process Master
                    </Link>
                  </li>
                  <li>
                    <Link to="master/section-master" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Section Master
                    </Link>
                  </li>
                  <li>
                    <Link to="master/o-p-master" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                    Qms Tracking 
                    </Link>
                  </li>
                  <li>
                    <Link to="master/user-master" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                    User Master 
                    </Link>
                  </li>
                </ul>

              )}
            </li>

            <li>
              <button
                id="planingDropdownBtn"
                onClick={() => toggleDropdown('planingDropdown')}
                className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
              >
                Production Planing
                <svg
                  className={`h-6 w-6 ml-auto transition-transform ${openDropdownId === 'mastersDropdown' ? 'transform rotate-180' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M6 8l4 4 4-4H6z" />
                </svg>
              </button>
              {openDropdownId === 'planingDropdown' && (
                <ul className="pl-8 mt-2 space-y-2">
                  <li>
                    <Link to="planing/planing-input" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Sewing Planing
                    </Link>
                  </li>


                </ul>

              )}
            </li>

            <li>
              <button
                id="rtqmId"
                onClick={() => toggleDropdown('rtqmDropdown')}
                className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
              >
                RTQM
                <svg
                  className={`h-6 w-6 ml-auto transition-transform ${openDropdownId === 'mastersDropdown' ? 'transform rotate-180' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M6 8l4 4 4-4H6z" />
                </svg>
              </button>
              {openDropdownId === 'rtqmDropdown' && (
                <ul className="pl-8 mt-2 space-y-2">
                  <li>
                    <Link to="/tab-login" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Input
                    </Link>
                  </li>

                  <li>
                    <Link to="/" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      OutPut
                    </Link>
                  </li>
                </ul>

              )}
            </li>

            
            <li>
              <button
                id="reportId"
                onClick={() => toggleDropdown('Report')}
                className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
              >
                Reports
                <svg
                  className={`h-6 w-6 ml-auto transition-transform ${openDropdownId === 'Report' ? 'transform rotate-180' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M6 8l4 4 4-4H6z" />
                </svg>
              </button>
              {openDropdownId === 'Report' && (
                <ul className="pl-8 mt-2 space-y-2">
                  <li>
                    <Link to="reports/rtqm-report?" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      RTQM Report
                    </Link>
                  </li>

                 
                </ul>

              )}
            </li>

            <li>
              <button
                id="cuttingDropdownBtn"
                onClick={() => toggleDropdown('cuttingDropdown')}
                className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
              >
                Cutting
                <svg
                  className={`h-6 w-6 ml-auto transition-transform ${openDropdownId === 'cuttingDropdown' ? 'transform rotate-180' : ''}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M6 8l4 4 4-4H6z" />
                </svg>
              </button>
              {openDropdownId === 'cuttingDropdown' && (
                <ul className="pl-8 mt-2 space-y-2">
                  <li>
                    <Link to="cutting_route/history/" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Cutting Entry
                    </Link>
                  </li>
                  <li>
                    <Link to="/" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                      Ready To Load
                    </Link>
                  </li>
                  
                </ul>

              )}
            </li>



          





            {/* <li>
              <Link to="/dashboard" className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                <svg
                  className="h-6 w-6 mr-2"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-7 4a1 1 0 0 0-1-1v-1a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1zM17 4a1 1 0 0 1 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-1zM9 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17 18a1 1 0 0 1-1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-1z"
                    clipRule="evenodd"
                  />
                </svg>
                History
              </Link>
            </li> 
          </ul>
        </>
      )} */}
    </div>
  );
};

export default Sidebar;
