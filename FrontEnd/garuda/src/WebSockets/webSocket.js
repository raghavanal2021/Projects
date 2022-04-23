import React, {createContext} from 'react';
import io from 'socket.io-client';
import { useDispatch } from 'react-redux';
import { updateloadstatus } from './actions';
//import updateload  from '../store/features/LoadSlice';
const WebSocketContext = createContext(null);

export {WebSocketContext}

export default ({children}) => {
    let socket;
    let ws;

    const dispatch = useDispatch();
    const sendmessage = (payload) => {
        socket.emit('requestload',payload)
    }
    if (!socket) {
        socket = io.connect("http://localhost:8000");
        socket.on("loadresponse", (msg) =>{
            const payload = JSON.parse(msg);
            dispatch(updateloadstatus(payload));
        })

        ws = {
            socket: socket,
            sendmessage
        }
    }
    return (
        <WebSocketContext.Provider value={ws}>
            {children}
        </WebSocketContext.Provider>
    )
}