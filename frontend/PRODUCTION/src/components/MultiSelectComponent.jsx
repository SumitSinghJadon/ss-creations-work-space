import React from 'react';
import Select from 'react-select';

const MultiSelectComponent = ({ options, value, onChange, label, name, id }) => {

  const formattedOptions = options.map(option => ({
    value: option.value,
    label: option.label,
  }));


  const handleChange = (selectedOptions) => {
    onChange(selectedOptions.map(option => option.value));
  };

  return (
    <>
      {label && <label htmlFor={id}>{label}</label>}
      <Select
        id={id}
        name={name}
        value={formattedOptions.filter(option => value.includes(option.value))}
        onChange={handleChange}
        options={formattedOptions}
        isMulti={true} 
        className="mt-1 w-[200px] py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        placeholder="Select multiple options..."
      />

</>
  
  );
};

export default MultiSelectComponent;
