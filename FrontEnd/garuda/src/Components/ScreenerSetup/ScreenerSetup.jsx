import React, { useEffect, useRef, useState } from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Checkbox } from 'primereact/checkbox';
import { Dropdown } from 'primereact/dropdown';
import { useDispatch, useSelector } from 'react-redux';
import { Toast } from 'primereact/toast';
import { updatescreener } from '../../WebSockets/actions';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
/**
* @author
* @function ScreenerSetup
**/

export const ScreenerSetup = (props) => {
    const [displayDialog,setdisplayDialog] = useState(false);
    const [enabled, setenabled] = useState(false);
    const [screenername,setscreenername] = useState("");
    const [screenerdesc,setscreenerdesc] = useState("");
    const [resolution, setresolution] = useState("");
    const msgstate = useSelector((state)=> state.screenersetup);
    const [response,setresponse] = useState([]);
    const toast = useRef(null);
    const dispatch = useDispatch()

    const header = (
        <div className="bg-blue-300">
        <h2> <b> Screener Setup </b></h2>
        </div>
    );

    const onDisplayClick = () => {
        setdisplayDialog(true);
    }

    const resolutionOptions = [
        {label: 'Daily', value: 'D'},
        {label: 'Weekly', value: 'W'},
        {label: 'Monthly', value: 'M'}
    ];

    const onHide = () => {
        setdisplayDialog(false);
    }

    const dialogHeader =(
    <h2>Add a new Screener Type</h2>
    )
        
    const footer = (
        <div>
        <div className='mt-10 flex mb-2'>
            <div className='ml-5'>
            <Button icon="pi pi-plus" label= "Setup a new Screener" onClick={()=>onDisplayClick('displaydialog')}/>
            </div>
            </div>
        </div>
            );

    const dialogclickok = () => {
        let jsonobj = {"screenername":screenername, "screenerdesc":screenerdesc,"freq":resolution, "enabled": enabled};
        let inputjson = JSON.stringify(jsonobj);
        alert(inputjson);
        callsetupService(inputjson);
            }

    const dialogfooter = (
        <div>
             <Button icon="pix   pi-plus" label= "Add"  onClick={dialogclickok} />
             <Button label= "Close"  onClick={onHide} />
        </div>
    )

    const showError = () => {
        toast.current.show({severity:'error', summary: 'Duplicate Screener', detail:'Screener Already Exists. Your setup is not saved.', life: 3000});
    }

    const showSuccess = () => {
        toast.current.show({severity:'info', summary: 'Screener Added', detail:'Requested Screener Added Successfully..', life: 3000});
    }

    const clear = () => {
        toast.current.clear();
    }

    useEffect(() => {
        fetch("http://localhost:8400/screeners/",{method:'GET'})
        .then(res => res.json())
        .then(data => {
            let msgobj = JSON.parse(data);
            let payload = JSON.parse(JSON.stringify(msgobj.payload));
            dispatch(updatescreener((eval(JSON.parse(JSON.stringify(payload.return))))));
            //let dataobj = JSON.parse(data.payload.return);
        })
    },[])

    useEffect(()=>{
        setresponse([]);
        setresponse(...msgstate.screeners);
    },[msgstate.screeners])

    const callsetupService = (message) => (
        fetch("http://localhost:8400/screenersetup/",{method:'POST',body:message,headers:{"Content-Type": "application/json; charset=utf-8"}})
        .then(res => res.json())
        .then(data => { 
                       const dataobj = JSON.parse(data);
                       if (dataobj.payload.statuscode === -100) {
                           showError();
                       }
                       else {
                           dispatch(updatescreener(dataobj.payload.return));
                           showSuccess();
                       }
                       console.log(dataobj.payload.statuscode);  
                      })
       
    )


 const [columnDefs] = useState([
    { field: "screenername", headerName: "Screener Name",resizable: true,cellStyle: () => ({
        display: "flex",
        alignItems: "left",
        justifyContent: "left"
      })},
    { field: "screenerdesc", headerName: "Screener Description", resizable:true, cellStyle: () => ({
        display: "flex",
        alignItems: "left",
        justifyContent: "left"
      }) },
    { field: "enabled", resizable:true,cellStyle: () => ({
        display: "flex",
        alignItems: "left",
        justifyContent: "left"
      })},
]);  


    
  return(
    <div className='mt-10 flex'>
    <div className='ml-5'>
        <Card header={header} footer={footer}>
        <div>
        <DataTable value={response} responsiveLayout="scroll">
                    <Column field="screenername" header="Screener Name"></Column>
                    <Column field="screenerdesc" header="Screener Description"></Column>
                    <Column field="freq" header="Frequency"></Column>
                    <Column field="enabled" header="Enabled"></Column>
                </DataTable>
        </div>
        </Card>

    </div>
    <div>

    <Toast ref={toast} />
        <Dialog header = {dialogHeader} footer={dialogfooter} visible={displayDialog} style={{ width: '50vw' }} onHide={onHide} >
            <div className='grid p-fluid'>
            <div className="col-12 md:col-4">
                        <div className="p-inputgroup">
                            <span className="p-inputgroup-addon">
                                <i className="pi pi-tags"></i> 
                            </span>
                            <InputText placeholder="Screener Name" value= {screenername} onChange={(e) => setscreenername(e.target.value)} />
                        </div>
                    </div>
                    <div className="col-12 md:col-4 mt-2">
                        <div className="p-inputgroup">
                            <span className="p-inputgroup-addon">
                            <i className="pi pi-tags"></i> 
                            </span>
                            <InputText placeholder="Description" value = {screenerdesc} onChange={(e) => setscreenerdesc(e.target.value)} />
                        </div>
                    </div>
                    <div className="col-12 md:col-4 mt-2">
                        <div className="p-inputgroup">
                            <span className="p-inputgroup-addon">
                            <i className="pi pi-tags"></i> 
                            </span>
                            <Dropdown placeholder="Set the Resolution" value={resolution} options={resolutionOptions}  onChange= {(e)=> setresolution(e.value)}/>
                        </div>
                    </div>
                    <div className="col-12 mt-2">
                        <div className="p-inputgroup">
                            <span className="p-inputgroup-addon">
                                <Checkbox checked={enabled} onChange={(e) => setenabled(!enabled)} />
                            </span>
                            <span className="p-inputgroup-addon"> Screener Enabled</span>
                        </div>
                    </div>
            </div>
        </Dialog>
    </div>
</div>

   )
  }
