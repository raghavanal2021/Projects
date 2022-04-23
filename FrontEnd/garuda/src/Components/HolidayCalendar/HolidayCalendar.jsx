import React, { useEffect, useState } from 'react';
import { Card } from 'primereact/card';
import { Dropdown } from 'primereact/dropdown';
import { AgGridReact } from 'ag-grid-react';


import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';

/**
* @author
* @function HolidayCalendar
**/


const HolidayCalendar = (props) => {

    const [yearArray,setyearArray] = useState([]);
    const [selectedYear,setSelectedYear] = useState("");
    const [response,setresponse] = useState("");

useEffect(()=> {
    returnYears();
    fetch("http://localhost:8400/getHolidays/" + new Date().getFullYear(),{method:'GET'})
    .then(res => res.json())
    .then(data => { 
                     console.log(data);
                     setresponse(JSON.parse(data));
                  });

},[]);

const returnYears = () => {
    let current_year = {name: new Date().getFullYear(), code : new Date().getFullYear()};
    let prev_year = {name: new Date().getFullYear() - 1, code : new Date().getFullYear() - 1};
    let year_2_back = {name: new Date().getFullYear() - 2, code : new Date().getFullYear() - 2};
    let yeararr = [current_year,prev_year,year_2_back];
    setyearArray(yeararr);
}

const header = (
    <div className="bg-blue-300">
    <h2> <b> Holiday Calendar </b></h2>
    </div>
);
    
const footer = (
    <div>
    <div className='mt-10 flex mb-2'>
        <div className='ml-5'>
        </div>
        </div>
    </div>
        );

 const selectYears = (years) => {
     console.log(years.code);
     fetch("http://localhost:8400/getHolidays/" + years.code,{method:'GET'})
            .then(res => res.json())
            .then(data => { 
                             console.log(data);
                             setresponse(JSON.parse(data));
                          });
                          return response;
                        
 }

 const [columnDefs] = useState([
    { field: "Year",resizable: true,cellStyle: () => ({
        display: "flex",
        alignItems: "left",
        justifyContent: "left"
      })},
    { field: "Description", resizable:true, cellStyle: () => ({
        display: "flex",
        alignItems: "left",
        justifyContent: "left"
      }) },
    { field: "Date", resizable:true },
]);  

  return(
    <div className='mt-10 flex'>
        <div className='ml-5'>
            <Card header={header} footer={footer}>  
            <p className="m-0" style={{lineHeight: '1.5'}}></p>
                <Dropdown options={yearArray} optionLabel="name" onChange={(e) => {
                    setSelectedYear(e.value);
                    selectYears(e.value);
                }} value={selectedYear} placeholder = "Select the Year" />
                <div className='mt-5'>
                <div className="ag-theme-alpine" style={{height:700, width: 600}}>
            <AgGridReact
               rowData={response}
               columnDefs={columnDefs}>
           </AgGridReact>
       </div>
            </div>
            </Card>
        </div>
    </div>
   )
  }

  export default HolidayCalendar;