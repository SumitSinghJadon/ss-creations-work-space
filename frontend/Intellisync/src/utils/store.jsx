import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import userReducer from './slice/UserSlice';
import orderReducer from './slice/LineMasterSlice';
import defectReducer from './slice/DefectMasterSlice';
import sewingInputReducer from './slice/SewingInputSlice';
import rejectReducer from './slice/RejectMasterSlice';
import passReducer from './slice/PassMasterSlice';

const persistConfig = {
  key: 'root',
  storage,
  // timeout: 100000, // uncomment if needed
};

const rootReducer = {
  User: persistReducer(persistConfig, userReducer),
  order: persistReducer(persistConfig, orderReducer),
  defectMaster: persistReducer(persistConfig, defectReducer),
  sewingInput: persistReducer(persistConfig, sewingInputReducer),
  rejectMaster: persistReducer(persistConfig, rejectReducer),
  passMaster: persistReducer(persistConfig, passReducer),
};

const store = configureStore({
  reducer: rootReducer,
});

const persistor = persistStore(store);

export { store, persistor };





// import { createStore, applyMiddleware } from 'redux';
// import { persistStore, persistReducer, FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from 'redux-persist';
// import storage from 'redux-persist/lib/storage';
// import rootReducer from './reducers';
// import { getDefaultMiddleware } from '@reduxjs/toolkit';

// const persistConfig = {
//   key: 'root',
//   storage,
// };

// const persistedReducer = persistReducer(persistConfig, rootReducer);

// const middleware = getDefaultMiddleware({
//   serializableCheck: {
//     ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
//     ignoredPaths: ['register'],
//   },
// });

// const store = createStore(
//   persistedReducer,
//   applyMiddleware(...middleware)
// );

// const persistor = persistStore(store);

// export { store, persistor };
