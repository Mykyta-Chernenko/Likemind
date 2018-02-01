import React, {Component} from 'react'
<<<<<<< HEAD:frontend/src/components/ChatTest/index.js

class Chat extends Component {
=======
import {Link} from 'react-router'
import axios from 'axios'

class Main extends Component {
>>>>>>> d480c5680ff97b1bc35946cae0ab385387cae1a5:frontend/src/containers/Menu.js
    constructor(props) {
        super(props);
        this.sendMessage = this.sendMessage.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.startChat = this.startChat.bind(this);
        this.initializeSocketForChat = this.initializeSocketForChat.bind(this);
        let tokens = [[1, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTE3Mzk1MzQzLCJlbWFpbCI6IiJ9.84dOMKCpO5dJcYF1uQxsNbQiTxPdhe8dOpX5-rlzj1E'],
            [9, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6Im5pa2l0YTciLCJleHAiOjE1MTczOTUzNTgsImVtYWlsIjoibmlraXRhQGNvZGUtb24uYmUifQ.RY0GUN4Pxvt7hzOoTulgQkUUstE-jz8PkbmfSdK5wt0'],
            [10, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJuaWtpdGE4IiwiZXhwIjoxNTE3Mzk1Mzc1LCJlbWFpbCI6Im5pa2l0YUBjb2RlLW9uLmJlIn0.qSuVUEHY5tcoa94imejz7_xcr8U0jSPUyUQ-E6GcRMw']];
        let token = tokens[Math.round(Math.random() * 2)];
        let user_socket = new WebSocket('ws://0.0.0.0:8000/user?token=' + token[1]);
        user_socket.onopen = () => {
            console.log("User chat_socket open");
        };
        user_socket.onmessage = (event) => {
            console.log(JSON.parse(event.data)['text'])
            this.setState({user_events: [...this.state.user_events, JSON.parse(event.data)['text']]})

        };
        user_socket.onclose = () => {
            console.log('User chat_socket disconnected')
        };
        user_socket.onerror = (e) => {
            console.log(e)
        };
        this.state = {
            message: "",
            messages: [],
            friends: [],
            token: token,
            chat_socket: '',
            interlocuter: '',
            username: '',
            user_events: [],
            user_socket: user_socket
        };

        let config = {
            headers: {'Authorization': 'JWT ' + token[1]}
        };
        const self = this;
        axios.get('http://localhost:8000/api/users/' + token[0] + '/', config)
            .then(function (response) {
                self.setState({
                    friends: [...self.state.friends, ...response.data.friends],
                    username: response.data.username

                })
                ;
                console.log(response.data.friends);
                console.log(response.status);
            });
    }

    sendMessage() {
        console.log(this.state.message);
        console.log(this.state.chat_socket);
        this.state.chat_socket.send(this.state.message);
    }

    handleResponse(value) {
        this.setState({messages: [...this.state.messages, value]})
    }

    handleInputChange(e) {
        this.setState({message: e.target.value})
    }

    initializeSocketForChat(id) {
        console.log('init ');
        if (this.state.chat_socket) {
            this.state.chat_socket.close()
        }
        let socket = new WebSocket('ws://0.0.0.0:8000/private_chat?token=' +
            this.state.token[1] + '&to_user_id=' + id)
        console.log('end init')
        socket.onopen = () => {
            console.log("Connected to chat chat_socket");
        };
        socket.onmessage = (event) => {
            this.setState({messages: [...this.state.messages, JSON.parse(event.data)]})

        };
        socket.onclose = () => {
            console.log('disconnected')
        };
        socket.onerror = (e) => {
            console.log(e)
        };
        this.setState({
            "chat_socket": socket
        })
    }

    startChat(e) {
        this.setState({chat_with: e.target.id, interlocuter: e.target.getAttribute("data-username")});
        console.log(e.target.id);

        this.initializeSocketForChat(e.target.id)
    }

    render() {
        const divStyle = {
            color: 'blue',
            backgroundColor: 'grey',
            listStyle: 'none',
        };
<<<<<<< HEAD:frontend/src/components/ChatTest/index.js
        return (<div>
            <input value={this.state.message} onChange={this.handleInputChange}></input>
            <button onClick={this.sendMessage}>Send message</button>
=======
        return <div>
            {/*<ul>*/}
            {/*<li><Link to="/">root</Link></li>*/}
            {/*<li><Link to="/main">main</Link></li>*/}
            {/*</ul>*/}
            <ul>
                Friends:
                {this.state.friends.map(
                    (value) =>
                        <li key={value.id} id={value.id} data-username={value.username} onClick={this.startChat}>
                            {value.username}
                        </li>
                )}
            </ul>
            <p>You {this.state.username} are speaking with {this.state.interlocuter}</p>
>>>>>>> d480c5680ff97b1bc35946cae0ab385387cae1a5:frontend/src/containers/Menu.js
            <ul style={divStyle}>
                {this.state.messages.map(
                    (value, key) =>
                        <li key={key}
                            className={this.username_id === value['username'] ? 'chat-user-left' : 'chat-user-right'}>
                            {this.username_id === value['username'] ? 'you' : 'Username: ' + value['username']} wrote
                            :"{value['text']}"
                        </li>
                )
                }
            </ul>
            <input value={this.state.message} onChange={this.handleInputChange}></input>
            <button onClick={this.sendMessage}>Send message</button>
             <div>
                {this.state.user_events.map(
                    (value, key) =>
                        <p key={key}> {value}</p>
                )}
            </div>
            {this.props.children}
        </div>
        )

    }
}

export default Chat;