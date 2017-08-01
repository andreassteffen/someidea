import React from 'react';
import ReactDOM from 'react-dom';
import JamboreeComment from './JamboreeComment.js'
import { Comment } from 'semantic-ui-react'

const style = {
  height: '300px',
  overflow: 'hidden'
}
const commentstyle = {
    overflow: 'auto',
    height: '100%'

}
export class Jamboree extends React.Component {
    constructor(props){
        super(props)
        this.state = {comments:[]}
    }
    _makeApiCall(symbol){
        fetch(`http://0.0.0.0:5001/${symbol}`, {
	        method: 'get'
        })
        .then(res=>res.json())
        .then((res) => {
            this.setState({comments:res}) 
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
      <div style={style}>
        <h1 className='dragit' >jamboree</h1>
        <div id="jamboree" style={commentstyle}>
              <Comment.Group>

            {this.state.comments.map((comment)=><JamboreeComment key={comment.user} author={comment.user} text={comment.comment} />
            )}
              </Comment.Group>

        </div>
      </div>
    );
  }
}