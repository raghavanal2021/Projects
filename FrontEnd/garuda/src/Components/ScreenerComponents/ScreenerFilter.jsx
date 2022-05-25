import React,{useState} from 'react'
import { Panel } from 'primereact/panel';
import { Ripple } from 'primereact/ripple';
import { Calendar } from 'primereact/calendar';
import { Button } from 'primereact/button';
import { Dropdown } from 'primereact/dropdown';

/**
* @author
* @function ScreenerFilter
**/

export const ScreenerFilter = (props) => {
    const [date1, setDate1] = useState(null);
    const [selectedItem, setSelectedItem] = useState(null);
    const [screenoptions,setScreenOptions] = useState([]);

    const template = (options) => {
        const toggleIcon = options.collapsed ? 'pi pi-chevron-down' : 'pi pi-chevron-up';
        const className = `${options.className} justify-content-start`;
        const titleClassName = `${options.titleClassName} pl-1`;
        
        return (
            <div className={className}>
                <button className={options.togglerClassName} onClick={options.onTogglerClick}>
                    <span className={toggleIcon}></span>
                    <Ripple />
                </button>
                <span className={titleClassName}>
                    Screener Options
                </span>
            </div>
        )
    }

  return(
    <div>
          <Panel headerTemplate={template} toggleable>
    <div>
        <div className='mt-2 flex mb-4'>
          <div className="ml-2 w-1/2">
            <label htmlFor="icon">Enter the Screener Date</label>
            <Calendar className='ml-3 w-full' id="basic" value={date1} onChange={(e) => setDate1(e.value)} />
          </div>
          <div className="ml-2 w-1/2">
            <label htmlFor="icon">Screener</label>
            <Calendar className='ml-3 w-full' id="basic" value={date1} onChange={(e) => setDate1(e.value)} />
          </div>
   
          <div className="ml-2 w-1/2 mt-5">
            <Button label="Run" className="p-button-success"> </Button>
          </div>
        </div>
    </div>
            </Panel>

    </div>
   )
  }
