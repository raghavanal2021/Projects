import { updateload } from "../store/features/LoadSlice";
import store from "../store";
export const sendMessage = (sock,action,msg) => {
    sock.emit(action,msg);
}

export const OnMessage = (sock) => {
    sock.on("loadresponse",msg => {
        console.log(msg);
        store.dispatch(msg);
    })
}