import logo from './logo.svg';
import './App.css';
import TopArtist from './TopArtist';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <TopArtist /> 
      </header>
    </div>
  );
}

export default App;
