import { LOAD_STATUS } from "../../WebSockets/actions" ;

const initialState  = { loadstatus:[] };
let loadhistory = [];
let loadstatus = [];

function LoadStatusReducer(state = initialState, action){

    switch(action.type) {
        case LOAD_STATUS:
            //if (state !== initialState) {
            //loadhistory = loadhistory.concat(sta  te);}
            //loadstatus = loadhistory.concat(action.payload);
          //  return {...state,loadstatus: loadstatus};
            return {loadstatus:[...state.loadstatus , action.payload]};
        default:
            return state;
    }

}
export default LoadStatusReducer;