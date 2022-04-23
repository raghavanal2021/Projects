import React, {useContext, useEffect, useState} from 'react';
import {Calendar} from 'primereact/calendar';
import { MultiSelect } from 'primereact/multiselect';
import { Button } from 'primereact/button';
import dateFormat from "dateformat";
import { WebSocketContext } from '../../WebSockets/webSocket';
import { useSelector } from 'react-redux';
import { ResultGrid } from '../LoadResult/ResultGrid';
/**
* @author Raghavan AL
* @function Loader
**/
const Loader = (props) => {
    const ws = useContext(WebSocketContext);
    const [rangeDates, setRangeDates] = useState(null);
    const [loadoptions, setLoadOptions] = useState([]);
    const [selectassetClass, setAssetClass] = useState([]);
    const [msg, setmsg] = useState([]);
    const sock = props.sock;
    //const msgObj = msgstate.map( msg => ({action:msg.action,payload:msg.payload}))
    const optionslist = [
        {name: 'FII', code:'FII'},
        {name: 'Volatility',code:'VOLT'},
        {name: 'Block Deals', code:'BLOCK'},
        {name: 'Bulk Deals', code:'BULK'}
    ];

    const assetClass = [
        {name: 'Equities', code:'EQ'},
        {name: 'Futures & Options', code:'FUT'},
        {name: 'Currency', code:'CURR'}
    ]
    const handleClick = () => {
        var optionslist = [];
        var assetList = [];
        loadoptions.forEach((opt) => {
            optionslist.push(opt.code);
        });
        selectassetClass.forEach((assetopt) => {
            assetList.push(assetopt.code)
        })
        let startDate = dateFormat(rangeDates[0],'yyyymmdd');
        let endDate = dateFormat(rangeDates[1],'yyyymmdd')

       let  outputmessage = JSON.stringify({"action":"requestload",
                                            "startDate": startDate,"endDate":endDate,
                                            "assetClass":assetList,"options":optionslist});
        console.log(outputmessage);
        ws.sendmessage(outputmessage);
    }

  return(
      <div>
    <div className='mt-10 flex mb-4'>
    <div className="ml-2 w-1/2">
    <label htmlFor="icon">Enter the Date Range</label>
    <Calendar className='ml-3 w-full' id="icon" value={rangeDates} onChange={(e) => setRangeDates(e.value)} selectionMode="range" readOnlyInput  />
</div>
<div className="ml-2 w-1/2">
    <label htmlFor="icon">Select the Load Type</label>
    <MultiSelect className='ml-3 w-full' value = {loadoptions} options = {optionslist} onChange= { (e) => setLoadOptions(e.value)} optionLabel="name"   display='chip' ></MultiSelect>
</div>
<div className="ml-2 w-1/2">
    <label htmlFor="icon">Asset Class</label>
    <MultiSelect className='ml-3 w-full' value = {selectassetClass} options = {assetClass} onChange= { (e) => setAssetClass(e.value)} optionLabel="name"   display='chip' ></MultiSelect>
</div>

<div className="ml-2 w-1/2 mt-5">
<Button label="Run" className="p-button-success" onClick={handleClick}> </Button>
</div>
</div>
<div>
    <ResultGrid />
</div>
</div>
  )
}

export default Loader;