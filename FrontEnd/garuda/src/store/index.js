import {configureStore} from '@reduxjs/toolkit';
import holidayCalendarslice from './features/holidayCalendarslice';
import LoadStatusReducer from './features/LoadSlice';

const store = configureStore({
    reducer:{
        holiday: holidayCalendarslice,
        load: LoadStatusReducer
    }
})

export default store;