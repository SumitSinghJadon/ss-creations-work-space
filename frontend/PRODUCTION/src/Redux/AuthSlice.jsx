import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    access: null,
    refresh: null,
    unitId: null,
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setTokens: (state, action) => {
            state.access = action.payload.access;
            state.refresh = action.payload.refresh;
            state.unitId = action.payload.unit_id;
        },
        removeTokens: (state) => {
            state.access = null;
            state.refresh = null;
            state.unitId = null;
        }
    }
});

export const { setTokens, removeTokens } = authSlice.actions;

export default authSlice.reducer;
