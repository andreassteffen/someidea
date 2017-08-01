import React from 'react';
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from  'recharts';

const data = [
      {name: 'IC50',counts:10},
      {name: 'Kd', counts:31},
      {name: 'EC50', counts:100},
      {name: 'Ki', counts:25},
      {name: '% Inh',counts: 200},
];


export class Chembl extends React.Component {
    constructor(props){
        super(props)
        this.state = {data:[]}
    }
    _makeApiCall(symbol){
        fetch(`http://0.0.0.0:5002/${symbol}`, {
	        method: 'get'
        })
        .then(res=>res.json())
        .then((res) => {
            this.setState({data:res}) 
        })
    }
    componentDidMount(){
      this._makeApiCall(this.props.symbol)
    }
    componentWillReceiveProps(nextProps) {
        this._makeApiCall(nextProps.symbol);
    }
    render() {
    return (
        <div>
            <h1 className='dragit'>chembl</h1>
            <BarChart width={600} height={300} data={this.state.data}
            margin={{top: 20, right: 30, left: 20, bottom: 5}}>
                <XAxis dataKey="standard_type" tickLine={false} stroke="black"/>
                <YAxis stroke="black"/>
                <Tooltip/>
                <Bar dataKey="counts" fill="#64B5F6" />
            </BarChart>
      </div>
    );
  }
}