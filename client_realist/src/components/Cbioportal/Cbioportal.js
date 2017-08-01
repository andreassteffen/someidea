import React from 'react';
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from  'recharts';

const data = [
      {name: 'LAML', multiple: 10, mutated: 20, del:5, amp: 10},
      {name: 'BRCA', multiple: 20, mutated: 10, del:31, amp: 2},
      {name: 'COADREAD', multiple: 4, mutated: 2, del:7, amp: 1},
      {name: 'DLBC', multiple: 12, mutated: 13, del:2, amp: 5},
      {name: 'OV', multiple: 10, mutated: 20, del:5, amp: 10},
      {name: 'LUAD', multiple: 10, mutated: 20, del:5, amp: 10},
      {name: 'HNSC', multiple: 10, mutated: 20, del:5, amp: 10},
];


export class Cbioportal extends React.Component {
    constructor(props){
        super(props)
        this.state = {data:[]}
    }
    _makeApiCall(symbol){

        fetch(`http://0.0.0.0:5003/${symbol}`, {
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
            <h1 className='dragit'>cbioportal</h1>
            <BarChart width={600} height={300} data={this.state.data}
            margin={{top: 20, right: 30, left: 20, bottom: 5}}>
                <XAxis dataKey="cancer_study_id" tickLine={false} stroke="black"/>
                <YAxis stroke="black"/>
                <Tooltip/>
                <Bar dataKey="multiple" stackId="a" fill="#aaaaaa" />
                <Bar dataKey="mut" stackId="a" fill="green" />
                <Bar dataKey="homdel" stackId="a" fill="blue" />
                <Bar dataKey="amp" stackId="a" fill="red" />
            </BarChart>
      </div>
    );
  }
}