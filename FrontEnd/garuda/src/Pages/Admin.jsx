import React from 'react';
import  HolidayCalendar  from '../Components/HolidayCalendar/HolidayCalendar';

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
    </div>
   )
  }

  export default Administration;