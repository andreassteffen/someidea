import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import Navbar from './components/Navbar';
import ProteinViewer from './components/ProteinViewer';
import Jamboree from './components/Jamboree';
import Cbioportal from './components/Cbioportal';
import Chembl from './components/Chembl';

var ReactGridLayout = require('react-grid-layout');

var layout = [
  {i: 'chembl', x: 0, y: 0, w: 1, h:1},
  {i: 'jamboree', x: 1, y: 0, w: 1, h: 1},
  {i: 'cbioportal', x: 0, y: 1, w: 1, h:1 },
  {i: 'proteinviewer', x: 1, y: 1, w: 1, h: 1}
];
class App extends Component {
    constructor(props) {
    super(props)
    this.state = {symbol: 'MYC'}
  }
  setSymbol(symbol){
    this.setState({symbol:symbol})
  }
  render() {
    return (
      <div className="App">
        <Navbar setSymbol={(symbol) => this.setSymbol(symbol)}/>
          <h1 className="ui center aligned icon header">{this.state.symbol}</h1>
          <ReactGridLayout draggableHandle=".dragit" className="layout" layout={layout} cols={2} rowHeight={350} width={1200}>
            <div key={'chembl'}><Chembl symbol={this.state.symbol} /></div>
            <div key={'jamboree'}><Jamboree symbol={this.state.symbol} /></div>
            <div key={'cbioportal'}><Cbioportal symbol={this.state.symbol} /></div>
            <div key={'proteinviewer'}><ProteinViewer symbol={this.state.symbol} /></div>
          </ReactGridLayout>
      </div>
    );
  }
}

export default App;
