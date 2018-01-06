import React, { Component } from 'react'
import { Link } from 'react-router'


class Main extends Component {
    render() {
        
        return <div>
        <ul>
            <li><Link to="/">root</Link></li>
            <li><Link to="/main">main</Link></li>
        </ul>
        {this.props.children}
        </div>

    }
}

export default Main;