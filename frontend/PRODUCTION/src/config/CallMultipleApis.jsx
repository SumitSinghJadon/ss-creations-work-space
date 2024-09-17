// import axios from "axios";
// import DjangoConfig from "./Config";

// const CallMultipleApis = async (endpoint, method = 'GET', data = null) => {
//     try {
//         const requests = DjangoConfig.apiUrl.map(async (baseUrl) => {
//             const url = `${baseUrl}${endpoint}`;
//             let response;

//             switch (method.toUpperCase()) {
//                 case 'GET':
//                     response = await axios.get(url);
//                     break;
//                 case 'POST':
//                     response = await axios.post(url, data);
//                     break;
//                 case 'PUT':
//                     response = await axios.put(url, data);
//                     break;
//                 case 'DELETE':
//                     response = await axios.delete(url);
//                     break;
//                 case 'PATCH':
//                     response = await axios.patch(url, data);
//                     break;
//                 default:
//                     throw new Error(`Unsupported HTTP method: ${method}`);
//             }

//             return response.data;
//         });

//         const results = await Promise.all(requests);
//         return results;
//     } catch (error) {
//         console.error('Error calling multiple APIs:', error);
//         throw error;
//     }
// };

// export default CallMultipleApis;

import axios from "axios";
import DjangoConfig from "./Config";

const CallMultipleApis = async (endpoint, method = 'GET', data = null) => {
    try {
        let response = null;
        
        for (const baseUrl of DjangoConfig.apiUrl) {
            const url = `${baseUrl}${endpoint}`;

            try {
                switch (method.toUpperCase()) {
                    case 'GET':
                        response = await axios.get(url);
                        break;
                    case 'POST':
                        response = await axios.post(url, data);
                        break;
                    case 'PUT':
                        response = await axios.put(url, data);
                        break;
                    case 'DELETE':
                        response = await axios.delete(url);
                        break;
                    case 'PATCH':
                        response = await axios.patch(url, data);
                        break;
                    default:
                        throw new Error(`Unsupported HTTP method: ${method}`);
                }

                if (response.status >= 200 && response.status < 300) {
                    break;
                }
            } catch (error) {
                console.error(`Error calling ${url}:`, error);
            }
        }

        if (response === null) {
            throw new Error('All servers failed to respond.');
        }

        return response.data;
    } catch (error) {
        console.error('Error calling multiple APIs:', error);
        throw error;
    }
};

export default CallMultipleApis
