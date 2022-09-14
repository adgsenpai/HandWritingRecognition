import React from 'react';
import logo from './logo.svg';
import CSS from 'csstype';
import './static/css/soft-ui-dashboard.css.map';
import './static/css/soft-ui-dashboard.min.css';

import { HandwritingCanvas } from 'handwriting-canvas';
import { Style } from 'util';

const canvasStyle: CSS.Properties = {
  border: '0.5px solid black',
};

const ClearButton = () => {
  return (
    <button className="btn btn-primary" onClick={
      () => {
        const canvas = document.getElementById('draw-area') as HTMLCanvasElement;
        const ctx = canvas.getContext('2d');
        ctx?.clearRect(0, 0, canvas.width, canvas.height);
      }
    }>Clear</button>
  );
}


const ProcessButton = () => {
  return (
    <button className="btn btn-primary" onClick={
      () => {
        const canvasElement = document.getElementById('draw-area') as HTMLCanvasElement;
        const resultDOM = document.getElementById('result') as HTMLDivElement;
        resultDOM.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
        // send post request to server
        fetch('/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ image: canvasElement.toDataURL('image/png') })
        })
          .then(response => response.json())
          .then(data => {          
            console.log(data);
            resultDOM.innerHTML = `<img src="${'data:image/jpeg;base64,'+data.imagedata}" alt="result" />`;          
          })
          .catch(error => {
            console.error('Error:', error);
            // remove spinner
            resultDOM.innerHTML = 'Error';
          });       
      }
    }>Process</button>
  );
}


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h5>Draw here!</h5>
        <canvas style={canvasStyle} id="draw-area">  </canvas>
        <br></br>
        <ClearButton />
        <ProcessButton />
        <div id="result"></div>
      </header>
    </div>
  );
}

// on page load
window.onload = function () {
  const canvasElement = document.getElementById('draw-area') as HTMLCanvasElement;
  const rootElement = document.getElementById('root') as HTMLElement;
  if (canvasElement) {
    //set canvasElement rootElement size
    canvasElement.width = rootElement.clientWidth;
    canvasElement.height = 500;
    //create handwriting canvas
    const handwritingCanvas = new HandwritingCanvas(canvasElement);

    // on web window resize
    window.onresize = function () {
      canvasElement.width = rootElement.clientWidth;
      canvasElement.height = 500;
      const handwritingCanvas = new HandwritingCanvas(canvasElement);

    }    
  }
}

export default App;
