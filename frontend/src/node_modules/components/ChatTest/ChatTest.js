import React, {Component} from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'
import axios from 'axios'

export class ChatTest extends Component {
    constructor(props) {
        super(props);
        this.sendMessage = this.sendMessage.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.startChat = this.startChat.bind(this);
        this.initializeSocketForChat = this.initializeSocketForChat.bind(this);
        let tokens = [[1, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ik5pa2l0YSIsImV4cCI6MTUxNzkyNzk1NywiZW1haWwiOiIifQ.LxVKI3UAooNxY5rrqzD4r1q_hmNazMUZZgfegp1FJis'],
            [10, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJEZW5pcyIsImV4cCI6MTUxODAwOTE4MSwiZW1haWwiOiJuaWtpdGFAY29kZS1vbi5iZSJ9.8yfo6ZQuDVhefVQYfIq6p-XgXJmu3cq9SbHJkThAW38'],
            [9, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6IkFydGVtIiwiZXhwIjoxNTE4MDA5MTYzLCJlbWFpbCI6Im5pa2l0YUBjb2RlLW9uLmJlIn0.IXUm3xON3rsPWxk51ANHS7l3MlHsAx9I6A39qoWQVTY']];
        let token = tokens[Math.round(Math.random() * 2)];
        let user_socket = new WebSocket('ws://0.0.0.0:8000/user/?token=' + token[1]);
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
        this.state.chat_socket.send(JSON.stringify(this.state.message));
    }

    handleResponse(value) {
        this.setState({messages: [...this.state.messages, value]})
    }

    handleInputChange(e) {
        this.setState({message: e.target.value})
    }

    initializeSocketForChat(id) {
        console.log('init ');
        document.cookie = 'token=' + this.state.token[1]
        if (this.state.chat_socket) {
            this.state.chat_socket.close()
        }
        let socket = new WebSocket('ws://0.0.0.0:8000/private_chat/?token=' +
            this.state.token[1] + '&to_user_id=' + id)
        console.log('end init')
        socket.onopen = () => {
            console.log("Connected to chat chat_socket");
        };
        socket.onmessage = (event) => {
            alert('sfd')
            console.log(event)
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
        return (<div>
                <p> you {this.state.username} are speaking with {this.state.interlocuter}</p>
                <input value={this.state.message} onChange={this.handleInputChange}></input>
                <button onClick={this.sendMessage}>Send message</button>
                <ul style={divStyle}>
                    {this.state.messages.map(
                        (value, key) => {
                            alert(value);
                            return <li key={key}
                                       className={this.username_id === value['username'] ? 'chat-user-left' : 'chat-user-right'}>
                                {this.username_id === value['username'] ? 'you' : 'Username: ' + value['username']} wrote
                                :"{value['text']}"
                            </li>
                        }
                    )
                    }
                </ul>
                <ul>
                    Friends:
                    {this.state.friends.map(
                        (value) =>
                            <li key={value.id} id={value.id} data-username={value.username} onClick={this.startChat}>
                                {value.username}
                            </li>
                    )}
                </ul>
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

function mapStateToProps(state) {
    return {}
}

function mapDispatchToProps(dispatch) {
    return {}
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ChatTest))