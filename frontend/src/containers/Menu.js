import React, {Component} from 'react'
import {Link} from 'react-router'


class Main extends Component {
    constructor(props) {
        super(props);
        this.sendMessage = this.sendMessage.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.state = {message: "", messages: []};
        this.tokens = ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTE2ODk2NTU0LCJlbWFpbCI6IiJ9.VeynSzmgrcyVzqAACOw4T3WF7JPuPSoI8eUpJnOvzf4',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6Im5pa2l0YTciLCJleHAiOjE1MTY4OTY2NzgsImVtYWlsIjoibmlraXRhQGNvZGUtb24uYmUifQ._2bI1WMG-a9JOZg94YtNxWojIG1WCg6kiTDKiVaMkjY',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJuaWtpdGE4IiwiZXhwIjoxNTE2ODk2NzExLCJlbWFpbCI6Im5pa2l0YUBjb2RlLW9uLmJlIn0.nYl7FdZV4zuNHQdmECpSUds5g1jifWDr84Kgql_5GGQ'];
        this.token = this.tokens[Math.round(Math.random() * 3)];
        this.socket = new WebSocket('ws://0.0.0.0:8000/chat1/?token='+this.token);

        this.socket.onopen = () => {
            console.log("Connected to chat socket");
            // this.socket.send(JSON.stringify({
            //     'msg': 'hi'
            // }))
        };
        this.socket.onmessage = (event) => {
            console.log(event.data)
            console.log(this.state.messages)
            this.setState({messages: [...this.state.messages, JSON.parse(event.data)]})

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
            listStyle: 'none',
        };
        return <div>
            <ul>
                <li><Link to="/">root</Link></li>
                <li><Link to="/main">main</Link></li>
            </ul>
            <input value={this.state.message} onChange={this.handleInputChange}></input>
            <button onClick={this.sendMessage}>Send message</button>
            <ul style={divStyle}>
                {this.state.messages.map(
                    (value, key) =>
                        <li key={key}
                            className={this.username_id == value['username'] ? 'chat-user-left' : 'chat-user-right'}>
                            {this.username_id == value['username'] ? 'you' : 'Username: ' + value['username']} wrote
                            :"{value['text']}"
                        </li>
                )
                }
            </ul>
            {this.props.children}
        </div>

    }
}

export default Main;