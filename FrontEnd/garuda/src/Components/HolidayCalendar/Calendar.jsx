import React, { useRef, useState } from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { Calendar } from 'primereact/calendar';
import { InputText } from 'primereact/inputtext';
import dateFormat from "dateformat";
import { Chip } from 'primereact/chip';
import { Messages } from 'primereact/messages'; 
import { Message } from 'primereact/message';
import { useDispatch } from 'react-redux';
import { addHoliday } from '../../store/features/holidayCalendarslice';
import axios from 'axios';
/**
* @author
* @function HolidayCalendar
**/

const HolidayCalendar = (props) => {
    const header = (
        <h2> <b> Holiday Calendar </b></h2>
    );
        
    const footer = (
<div>
<div className='mt-10 flex mb-4'>
    <div className='ml-5 w-1/2'>
        <Button label='Add a Holiday' onClick={()=> onClick('addNewHoliday')}></Button> </div>
        <div className='ml-5 w-1/2'>
        <Button label='Remove a Holiday'></Button>
    </div>
    </div>
</div>
    );

    const renderFooter = (name) => {
        return (
            <div>
                <Button label="No" icon="pi pi-times" onClick={() => onHide(name)} className="p-button-text" />
                <Button label="Yes" icon="pi pi-check" onClick={() => onSubmit(name)} autoFocus />
            </div>
        );
    };
    const [addNewHoliday,setAddnew] =   useState(false);
    const [position,setposition] = useState('center');
    const [holiday,setHoliday] = useState([]);
    const [Hdate,setHDate] = useState("");
    const [Hdesc,setHdesc] = useState("");
    const [value, setvalue] = useState("");
    const [holobj,setholdobj] = useState(Object);
    const [outjson, setoutjson] = useState([]);
    const [responsedata,setresponsedata] = useState(null);
    const dialogfuncmap = {
        'addNewHoliday':setAddnew
    }
    const onClick = (name,position) => {
        dialogfuncmap[`${name}`](true);
        if (position) {
            setposition(position);
        }
    }



    const onHide = (name) => {
        dialogfuncmap[`${name}`](false);
    };

    const headers = {
        'Content-Type': 'application/json'}

    const dispatch = useDispatch();

    const onSubmit = (name) => {
        fetch("http://127.0.0.1:8400/postHolidaysList",{method:'POST',headers:{ 'Content-Type': 'application/json' },body:JSON.stringify({hollist:outjson})})
        .then(response => response.json())
        .then(data =>  {
            console.log(data);
            setresponsedata(data);});
        dialogfuncmap[`${name}`](false);
    };


    const addHolidaytoList = () => {
        let holdobj = {holiday:dateFormat(Hdate,'yyyymmdd'),desc:value}
        console.log(holobj);
        //setoutjson(...outjson,JSON.stringify(holobj));
        setoutjson([...outjson, JSON.stringify(holdobj)]);
    }

  return(
    <div className='mt-10 flex mb-4'>
    <div className='ml-5'>
 <Card header={header} footer={footer}>  
 <p className="m-0" style={{lineHeight: '1.5'}}>
     </p>

 </Card>
    </div>  
    <Dialog header="Add a Holiday" visible={addNewHoliday} style={{ width: '50vw' }} footer={renderFooter('addNewHoliday')}  
            onHide={() => onHide('addNewHoliday')}>
                <div className="grid p-fluid">
                 <div className="field col-4 md:col-4">
                        <label htmlFor="basic">Enter the Holiday Date: </label>
                        <Calendar id="basic" value={Hdate} onChange={(e) => setHDate(e.value)} />
                    </div>
                    <div className="field col-4 md:col-4">
                        <label htmlFor="basic">Enter the Holiday Description: </label>
                      <InputText  value = {value} onChange={(e)=> setvalue(e.target.value)}></InputText>
                    </div>
                    <div className="mt-3">
                        <Button label="Add" onClick={addHolidaytoList} disabled={!value} ></Button>
                    </div>
                    <div className="flex align-items-center flex-wrap">
                        {outjson.map((hol,index) => {
                            console.log(hol);
                            return <Chip key = {index}
                             label = {JSON.parse(hol).holiday + " : " + JSON.parse(hol).desc}/>
                        })}
                    </div>
                    </div>
                </Dialog>
    </div>
   )
  };

export default HolidayCalendar;
