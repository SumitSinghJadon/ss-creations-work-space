


const NumberInputComponent=({ value, onChange })=>{

    const handleInputChange = (event) => {
        let newValue = parseInt(event.target.value, 10); 
      
        if (newValue < 0) {
          newValue = 0;
        }
        else if (newValue > 100) {
          newValue = 100;
        }
    
        onChange(newValue); 
      };
    return(
        <>

        <div>
      <label htmlFor="numberInput">Enter a number:</label>
      <input
        type="number"
        id="numberInput"
        value={value}
        onChange={handleInputChange}
        className="mt-1 w-[200px] py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
        </>
    )
}

export default NumberInputComponent;