import './App.css';
import { NavBar } from './Components/NavBar/NavBar';
import { BrowserRouter as Router, Routes , Route} from 'react-router-dom';
import  Screener  from './Pages/Screener';
import Scanner from './Pages/Scanner';
import  Watchlist  from './Pages/Watchlist';
import Fundamentals from './Pages/Fundamentals';
import Administration  from './Pages/Admin';
import LoadPage from './Pages/Loader';
import io from 'socket.io-client';
import WebSocketProvider, { WebSocketContext } from './WebSockets/webSocket';
import history from './Pages/history';

function App() {

  return (
    <div className="App">

     <WebSocketProvider>
      <Router history={history}>
     <NavBar/>
       <Routes>
         <Route path='/loader' element={<LoadPage/>}></Route>
         <Route path='/screener' element={<Screener/>}></Route>
         <Route path='/scanner' element={<Scanner/>}> </Route>
         <Route path='/watchlist' element={<Watchlist/>}></Route>
         <Route path='/fundamentals' element={<Fundamentals/>}> </Route>
         <Route path='/admin' element={<Administration/>}></Route>
       </Routes>
     </Router>
     </WebSocketProvider>
    </div>
  );
}

export default App;
