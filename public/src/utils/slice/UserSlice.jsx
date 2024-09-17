import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  userAuth: false,
  userData: null,
  userId: "",
  userName: "",
};

const userSlice = createSlice({
  name: 'User',
  initialState,
  reducers: {
    userLogin: (state, action) => {
      state.userAuth = true;
      state.userData = action.payload;
      state.userId = action.payload.id;
      state.userName = action.payload.userName;
    },
    userLogout: (state) => {
      state.userAuth = false;
      state.userData = null;
      state.userId = "";
      state.userName ="";
    },
  },
});

export const { userLogin, userLogout } = userSlice.actions;

export const userSelectAuth = (state) => state.User.userAuth;
export const userSelectUser = (state) => state.User.userData;
export const userSelectId = (state) => state.User.userId;
export const userSelectUserName = (state) => state.User.userName;

export default userSlice.reducer;
