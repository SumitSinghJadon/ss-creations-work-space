import axios from 'axios';
import { store } from '../Redux/store';
import { removeTokens, setTokens } from '../Redux/AuthSlice';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
});

// Request interceptor to add token to headers
api.interceptors.request.use(
    (config) => {
        const state = store.getState();
        const { access } = state.auth;
        if (access) {
            config.headers['Authorization'] = `Bearer ${access}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const { response } = error;
        const { status } = response || {};

        if (status === 401) {
            // Token might be expired, attempt to refresh
            const state = store.getState();
            const { refresh } = state.auth;
            console.log("refresh", refresh);

            if (refresh) {
                try {
                    const refreshResponse = await axios.post('http://127.0.0.1:8000/api/token/refresh/', { refresh });
                    const { access: accessToken, refresh: refreshToken } = refreshResponse.data;

                    store.dispatch(setTokens({ access: accessToken, refresh: refreshToken }));

                    // Retry the original request
                    error.config.headers['Authorization'] = `Bearer ${accessToken}`;
                    return api.request(error.config);
                } catch (refreshError) {
                    // Refresh token failed, handle logout
                    store.dispatch(removeTokens());
                    return Promise.reject(refreshError);
                }
            } else {
                // No refresh token, handle logout
                store.dispatch(removeTokens());
            }
        }

        return Promise.reject(error);
    }
);

export default api;
