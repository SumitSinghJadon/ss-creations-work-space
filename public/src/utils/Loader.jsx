// import React from 'react';
// import styled, { keyframes } from 'styled-components';

// // Define colors for each line
// const colors = ['red', 'yellow', 'green', 'blue'];

// // Keyframe animation for rotating lines
// const rotate = keyframes`
//     0% {
//         transform: rotate(0deg);
//     }
//     100% {
//         transform: rotate(360deg);
//     }
// `;

// // Styled component for the loader container
// const LoaderContainer = styled.div`
//     position: absolute;
//     top: 50%;
//     left: 50%;
//     transform: translate(-50%, -50%);
//     width: 10px;
//     height: 10px;
//     display: flex;
//     justify-content: center;
//     align-items: center;
// `;


// // Styled component for each line
// const Line = styled.div`
//     position: absolute;
//     width: 6px;
//     height: 10px;
//     background-color: ${props => props.color};
//     top: 28px;
//     left: 37px;
//     transform-origin: 4px 55px;
//     animation: ${rotate} 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;

//     &:nth-child(1) {
//         transform: rotate(0deg);
//         animation-delay: -0.45s;
//     }
   
//     &:nth-child(2) {
//         transform: rotate(90deg);
//         animation-delay: -0.3s;
//     }

//     &:nth-child(3) {
//         transform: rotate(180deg);
//         animation-delay: -0.15s;
//     }

//     &:nth-child(4) {
//         transform: rotate(270deg);
//         animation-delay: 0s;
//     }
// `;

// const AudioLoader = () => {
//     return (
//         <LoaderContainer>
//             {colors.map((color, index) => (
//                 <Line key={index} color={color} />
//             ))}
//         </LoaderContainer>
//     );
// };

// export default AudioLoader;



import React from 'react';
import styled, { keyframes } from 'styled-components';

const colors = ['#e44b43', '#f8be14', '#40a85d', '#4b89ee'];

// Keyframe animation for bar scaling
const scale = keyframes`
    0% {
        transform: scaleY(0.5);
    }
    100% {
        transform: scaleY(1);
    }
`;

// Styled component for the loader container
const LoaderContainer = styled.div`
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 40px; 
    height: 80px; 
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    backdrop-filter: blur(800px);
`;

// Calculate the height based on the index
const calculateHeight = index => {
    switch (index) {
        case 0:
            return '10px'; // Red line
        case 1:
            return '30px'; // Yellow line
        case 2:
            return '50px'; // Green line
        case 3:
            return '70px'; // Blue line
        default:
            return '10px';
    }
};


const AudioBar = styled.div`
    width: 6px; /* Width of each bar */
    height: ${props => calculateHeight(props.index)};
    background-color: ${props => props.color};
    transform-origin: bottom; /* Ensure scaling happens from the bottom */
    animation: ${scale} 1s ease-in-out infinite; /* Adjusted animation duration */

    &:nth-child(1) {
        animation-delay: -0.375s; /* Adjusted delay */
    }

    &:nth-child(2) {
        animation-delay: -0.25s; /* Adjusted delay */
    }

    &:nth-child(3) {
        animation-delay: -0.125s; /* Adjusted delay */
    }

    &:nth-child(4) {
        animation-delay: 0s; /* No delay for the last bar */
    }
`;


const AudioLoader = () => {
    return (
        <LoaderContainer>
            {colors.map((color, index) => (
                <AudioBar key={index} color={color} index={index} />
            ))}
        </LoaderContainer>
    );
};

export default AudioLoader;
