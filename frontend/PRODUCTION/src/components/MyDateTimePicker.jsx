import React from 'react';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { TextField, InputAdornment, IconButton } from '@mui/material';
import { CalendarToday } from '@mui/icons-material';
function MyDateTimePicker() {
  const [value, setValue] = React.useState(null);
  return (
    <DateTimePicker
      label="Select Date and Time"
      value={value}
      onChange={(newValue) => setValue(newValue)}
      renderInput={(params) => (
        <TextField
          {...params}
          inputProps={{ ...params.inputProps, readOnly: true }} // Disable typing
          InputAdornmentProps={{
            position: 'end',
            onClick: params.inputProps?.onClick, // Open calendar on click
          }}
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={params.inputProps?.onClick}>
                  <CalendarToday />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      )}
    />
  );
}
export default MyDateTimePicker;