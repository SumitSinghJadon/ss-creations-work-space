import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import MainRouter from './routers/MainRouter'
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './Redux/store';
import NotificationContainer from './Redux/NotificationContainer';


ReactDOM.createRoot(document.getElementById('root')).render(
    <Provider store={store}>
        <PersistGate  persistor={persistor}>
            <NotificationContainer />
            <MainRouter />
        </PersistGate>
    </Provider>
)
