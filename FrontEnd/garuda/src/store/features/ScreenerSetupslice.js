import { SCREENER } from "../../WebSockets/actions";
const initialState  = { screeners:[] };


function ScreenerReducer(state = initialState, action){

    switch(action.type) {
        case SCREENER:
            //if (state !== initialState) {
            //loadhistory = loadhistory.concat(sta  te);}
            //loadstatus = loadhistory.concat(action.payload);
          //  return {...state,loadstatus: loadstatus};
            return {screeners:[...state.screeners , action.payload]};
        default:
            return state;
    }

}
export default ScreenerReducer;