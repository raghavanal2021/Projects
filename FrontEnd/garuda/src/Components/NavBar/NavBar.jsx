import React ,{useRef} from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'primereact/button';
import { Badge } from 'primereact/badge';
import { OverlayPanel } from 'primereact/overlaypanel';
import { ResultGrid } from '../LoadResult/ResultGrid';
import { NotificationCard } from '../NotificationCard/NotificationCard';

/**
* Raghavan AL
* Navigation Bar Component
**/

export const NavBar = (props) => {
  const op = useRef(null);
  return(
    <div>
        <nav className='bg-gray-800'>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <img
                  className="h-8 w-8"
                  src="https://tailwindui.com/img/logos/workflow-mark-indigo-500.svg"
                  alt="Workflow"
                />
              </div>

              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Link to = "loader">Loader</Link>
                </div>
               </div>
               </div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Link to = "screener">Screener</Link>
                </div>
               </div>
            </div>
            <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Link to ="scanner">Scanner</Link>
                </div>
               </div>
            </div>
            <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Link to ="watchlist" >Watchlist</Link>
                </div>
               </div>
            </div>
            <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                Market Profile
                </div>
               </div>
            </div>
            <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Link to ="fundamentals">Fundamentals and Valuations</Link> 
                </div>
               </div>
            </div>
            </div>
            <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Link to ="admin" >Administration</Link>
                </div>
               </div>
            </div>

            <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4"> 
                <div className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium">
                <Button type="button" label="Notifications"  className="p-button-primary" onClick={(e) => op.current.toggle(e)}>
                  <Badge severity="danger" ></Badge></Button>
                </div>
               </div>
            </div>
            <div>
            <OverlayPanel ref={op} showCloseIcon id="overlay_panel" style={{width: '450px'}}>
                    <NotificationCard/>
                </OverlayPanel>
            </div>
            </div>
        </div>
        </nav>
    </div>
   )
  }
