import React from 'react';
import ReactDOM from 'react-dom';
var NGL = require("ngl")

const nglstyle = {
    width:"550px", 
    height:"300px"
}


export class ProteinViewer extends React.Component {
    constructor(props){
        super(props)
    }
    _makeApiCall(symbol){        
        fetch(`http://0.0.0.0:5004/${symbol}`, {
	        method: 'get'
        })
        .then(res=>res.json())
        .then(res => {
            this.stage.loadFile( `rcsb://${res.pdb}`, { defaultRepresentation: true, backgroundColor:'white' } )
            this.stage.autoView(100);
        })
    }
    componentDidMount(){
      const stage = new NGL.Stage( "nglviewport" );
      this.stage = stage;
      this._makeApiCall(this.props.symbol)
    }
    componentWillReceiveProps(nextProps) {
        this.stage.removeAllComponents();
        this._makeApiCall(nextProps.symbol);
        
    }
    render() {
        return (
        <div>
            <h1 className='dragit'>protein structure</h1>
            <div id="nglviewport" style={nglstyle}>
            </div>
        </div>
        );
  }
}