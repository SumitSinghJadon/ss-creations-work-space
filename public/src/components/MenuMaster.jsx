import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'; 
import DjangoConfig from '../config/Config';

const MenuMaster = () => {
    const [menuItems, setMenuItems] = useState([]);

    useEffect(() => {
        fetchMenuData();
    }, []);

    const fetchMenuData = () => {
        axios.get(`${DjangoConfig.apiUrl}/rtqm/home/`)
            .then(response => {
                setMenuItems(response.data.menu);
            })
            .catch(error => {
                console.error('Error fetching menu data:', error);
            });
    };

    const [openMenuId, setOpenMenuId] = useState(null);

    // Function to toggle submenu display
    const toggleSubMenu = (menuId) => {
        setOpenMenuId(openMenuId === menuId ? null : menuId);
    };

    return (
        <div>
            <ul className="menu-list">
                {menuItems.filter(item => item.parent_id === null).map(menuTitle => (
                    <li key={menuTitle.id}>
                        <button
                            id={`menu-${menuTitle.id}`}
                            className="text-sm hover:text-black hover:bg-gray-100 px-4 py-2 flex items-center w-full text-left"
                            onClick={() => toggleSubMenu(menuTitle.id)} // Toggle submenu visibility
                        >
                            {menuTitle.name}
                            <svg
                                className={`h-4 w-4 ml-auto transition-transform ${openMenuId === menuTitle.id ? 'transform rotate-90' : ''}`}
                                viewBox="0 0 20 20"
                                fill="currentColor"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path fillRule="evenodd" d="M6 3a1 1 0 01.707.293l6 6a1 1 0 010 1.414l-6 6A1 1 0 016 17V3z" clipRule="evenodd" />
                            </svg>
                        </button>

                        {openMenuId === menuTitle.id && (
                            <ul className="pl-8 mt-2 space-y-2">
                                {menuItems
                                    .filter(item => item.parent_id === menuTitle.id)
                                    .map(submenuItem => (
                                        <li key={submenuItem.id}>
                                            {submenuItem.is_link ? (
                                                <Link to={submenuItem.url} className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                                                    {submenuItem.name}
                                                </Link>
                                            ) : (
                                                <span className="text-sm hover:text-black hover:bg-gray-300 px-4 py-2 flex items-center">
                                                    {submenuItem.name}
                                                </span>
                                            )}
                                        </li>
                                    ))}
                            </ul>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MenuMaster;
