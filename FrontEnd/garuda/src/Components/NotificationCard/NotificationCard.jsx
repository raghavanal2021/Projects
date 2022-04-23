import React, {useState} from 'react';
import { Card } from 'primereact/card';
import { useSelector } from 'react-redux';
/**
* @author
* @function NotificationCard
**/
export const NotificationCard = (props) => {
const [response,setresponse] = useState([]);
const msgstate =  useSelector((state)=> state.load.loadstatus);
useState(() => {
    if (msgstate !== undefined) {
        msgstate.forEach(function(msg){
            setresponse(response => [...response,msg.loadstatus])
        })
        }
},[msgstate]);
useState(() => {
    console.log(msgstate)
    if (msgstate !== undefined) {
    msgstate.forEach(function(msg){
        setresponse(response => [...response,msg])
    })
    }
    },[]);

const returncard = () => {
    var rows = [];
    response.forEach(function(output) {
        if (output !== undefined){
            console.log(output.payload.eventtimestamp);
            rows.push( <Card> { output.payload.eventtimestamp }</Card>)      
    }
    return <tbody>{rows}</tbody>
    /*else {
        return (
            <div>No Load currently running...</div>
        )
    }*/
})
}


  return(
    <div>
        {returncard()}
    </div>
   )
  }
