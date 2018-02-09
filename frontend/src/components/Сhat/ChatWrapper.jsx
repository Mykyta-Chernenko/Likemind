import React, {Component} from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'
import '../../styles/chat.css'
import {AllChats} from './AllChats'
import axios from 'axios'
import {Chat} from "./Chat";

export class ChatWrapper extends Component {
    constructor() {
        super();
        const tokens = [
            // [1, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ik5pa2l0YSIsImV4cCI6MTUxNzkyNzk1NywiZW1haWwiOiIifQ.LxVKI3UAooNxY5rrqzD4r1q_hmNazMUZZgfegp1FJis'],
            // [10, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJEZW5pcyIsImV4cCI6MTUxODAwOTE4MSwiZW1haWwiOiJuaWtpdGFAY29kZS1vbi5iZSJ9.8yfo6ZQuDVhefVQYfIq6p-XgXJmu3cq9SbHJkThAW38'],
            ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6IkFydGVtIiwiZXhwIjoxNTE4MDA5MTYzLCJlbWFpbCI6Im5pa2l0YUBjb2RlLW9uLmJlIn0.IXUm3xON3rsPWxk51ANHS7l3MlHsAx9I6A39qoWQVTY']];
        // const token = tokens[Math.round(Math.random() * 2)];
        const token = tokens[0];
        localStorage.setItem('token', token);
        const user_socket = new WebSocket('ws://0.0.0.0:8000/user/?token=' + token);
        user_socket.onopen = () => {
            console.log("User chat_socket open");
        };
        user_socket.onmessage = (event) => {
            console.log(JSON.parse(event.data)['data'])
            //    handle action messages from server

        };
        user_socket.onclose = () => {
            console.log('User chat_socket disconnected')
        };
        user_socket.onerror = (e) => {
            console.log(e)
        };
        this.state = {
            chats: []
        }
        const config = {
            headers: {'Authorization': 'JWT ' + localStorage.getItem('token')}
        };
        axios.get('http://localhost:8000/api/self-users/', config)
            .then()
        localStorage.setItem('user_id', token[0])
        axios.get('http://localhost:8000/api/private-chats/', config)
            .then((response) => {
                    this.setState({'chats': response.data})
                }
            )
    }

    render() {
        const chats = this.state.chats
        return <div>{chats.length ? < AllChats chats={this.state.chats}/> : ''}</div>
    }
}

function mapStateToProps(state) {
    return {}
}

function mapDispatchToProps(dispatch) {
    return {}
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ChatWrapper))