import React from 'react';
import  HolidayCalendar  from '../Components/HolidayCalendar/HolidayCalendar';
import { ScreenerSetup } from '../Components/ScreenerSetup/ScreenerSetup';

/**
* @author
* @function Administration
**/

const Administration = (props) => {
  return(
    <div className='mt-10 flex mb-4'>
      <div className="ml-2 w-1/2">
    <div><HolidayCalendar/></div>
    </div>
    <div className="ml-2 w-1/2">
    <div><ScreenerSetup/></div>
    </div>
    </div>
   )
  }

  export default Administration;