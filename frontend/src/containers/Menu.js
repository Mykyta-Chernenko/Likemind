import React, {Component} from 'react'
import {Link} from 'react-router'


class Main extends Component {
    constructor(props) {
        super(props);
        this.sendMessage = this.sendMessage.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.state = {message: "", messages: ['1', '2']}

        this.socket = new WebSocket('ws://0.0.0.0:8000/chat/');

        this.socket.onopen = () => {
            console.log("Connected to chat socket");
            this.socket.send(JSON.stringify({
                'msg': 'hi'
            }))
        };
        this.socket.onmessage = (event) => {
            this.setState({messages: [...this.state.messages, event.data]})

        };
        this.socket.onclose = () => {
            console.log('disconnected')
        };
        this.socket.onerror = (e) => {
            console.log(e)
        }
    }

    sendMessage() {
        console.log(this.state.message);
        this.socket.send(this.state.message);
    }

    handleResponse(value) {
        this.setState({messages: [...this.state.messages, value]})
    }

    handleInputChange(e) {
        this.setState({message: e.target.value})
    }

    render() {
        const divStyle = {
            color: 'blue',
            backgroundColor: 'grey',
        };
        return <div>
            <ul>
                <li><Link to="/">root</Link></li>
                <li><Link to="/main">main</Link></li>
            </ul>
            <input value={this.state.message} onChange={this.handleInputChange}></input>
            <button onClick={this.sendMessage}>Send message</button>
            <ul style={divStyle}>
                {this.state.messages.map((number, key) => <li key={key}>{number}</li>)}
            </ul>
            {this.props.children}
        </div>

    }
}

export default Main;