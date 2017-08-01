import React, { Component } from 'react'
import { Menu, Segment,Input } from 'semantic-ui-react'

export class Navbar extends Component {
    constructor(props){
        super(props)
        this.state = { activeItem: 'realist', symbol:'CDK2' }
    }
    

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })
  handleKeyPress = (e)=>{
      console.log(e,e.key)
      if (e.key === 'Enter') {
          this.props.setSymbol(e.target.value)
      }
  }
  render() {
    const { activeItem } = this.state

    return (
      <div>
        <Menu pointing secondary>
          <Menu.Item name='realist' active={activeItem === 'realist'} onClick={this.handleItemClick} />
          <Menu.Item name='jamboree' active={activeItem === 'jamboree'} onClick={this.handleItemClick} />
          <Menu.Menu position='right'>
            <Menu.Item>
                <Input icon='search' placeholder='Search...' onKeyPress={this.handleKeyPress} />
            </Menu.Item>  
            <Menu.Item name='settings' active={activeItem === 'settings'} onClick={this.handleItemClick} />
            <Menu.Item name='logout' active={activeItem === 'logout'} onClick={this.handleItemClick} />
          </Menu.Menu>
        </Menu>
      </div>
    )
  }
}
