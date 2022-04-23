import { createSlice } from "@reduxjs/toolkit";


const initialState = {
    holiday:""
};

export const holidaySlice = createSlice({
    name : 'holidaylist',
    initialState,
    reducers: {
        addHoliday:(state,action) => {
            state.holiday = action.payload;
        }
    }
})  

export const {addHoliday} = holidaySlice.actions
export default holidaySlice.reducer