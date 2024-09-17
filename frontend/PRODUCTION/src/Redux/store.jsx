import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import authReducer from './AuthSlice';
import storage from 'redux-persist/lib/storage'; 
import { FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from 'redux-persist';
import logger from './logger';


const persistConfig = {
    key: 'root',
    storage,
    // whitelist: ['auth'],
};


const persistedAuthReducer = persistReducer(persistConfig, authReducer);



const store = configureStore({
    reducer: {
        auth: persistedAuthReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
          serializableCheck: {
            ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
            serializableCheck: false, 
          },
        }).concat(logger),
   
});

const persistor = persistStore(store);

export { store, persistor };