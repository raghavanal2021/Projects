import React, {useState, useEffect} from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { useSelector } from 'react-redux';
import { Badge } from 'primereact/badge';   
import '../Styles/Datatable.css';
/**
* @author
* @function 
**/

export const ResultGrid = (props) => {

const [response,setresponse] = useState([]);
const msgstate =  useSelector((state)=> state.load);

useEffect(()=>{
     setresponse([])
     if (msgstate.loadstatus.payload !== 'undefined') {
     var pyobj = [...msgstate.loadstatus];
     console.log(pyobj);
     pyobj.forEach((py) => {
         console.log(py.payload.date)
         setresponse(response =>[...response,py.payload])
         console.log(response)
     })
      } 
    },[msgstate.loadstatus]);

    const statusBodyTemplate = (rowData) => {
        if (rowData !== undefined) {
        if (rowData.statuscode === 200){    
            return <Badge value="SUCCESS" severity="success" className="mr-2"></Badge>
        }
        else {
            return <Badge value="FAIL" severity="danger" className="mr-2"></Badge>
        }
    }
    }

    

    const datable = () => {
            return (
                <div className='datatable-styles'>                          
                <DataTable value={response} size="small"     responsiveLayout="scroll" sortField='eventtimestamp' sortOrder={-1} stripedRows>
                <Column field="asset" header="Asset"></Column>
                <Column field="eventtimestamp" header="Event Timestamp"></Column>
                <Column field="date" header="Load Date"></Column>
                <Column field="reporttype" header="Report Type"></Column>
                <Column body={statusBodyTemplate} header="Status"></Column>
                <Column field="statusdesc" header="Status Description"></Column>
            </DataTable>
            </div>
         
            )
        }
    
  return(
    <div className= "ml-5 mr-5">
        {datable()}
    </div>
   )
  }
