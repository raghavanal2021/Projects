import {configureStore} from '@reduxjs/toolkit';
import holidayCalendarslice from './features/holidayCalendarslice';
import LoadStatusReducer from './features/LoadSlice';
import ScreenerReducer from './features/ScreenerSetupslice';

const store = configureStore({
    reducer:{
        holiday: holidayCalendarslice,
        load: LoadStatusReducer,
        screenersetup: ScreenerReducer
    }
})

export default store;