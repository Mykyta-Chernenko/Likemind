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
            // [1, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ik5pa2l0YSIsImV4cCI6MTUxNzU4OTY5NiwiZW1haWwiOiIifQ.OrU13Bc9HtPhgQTpgf0qjtEqgvvOFiqcotNJj0kzX9Y'],
            // [9, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJEZW5pcyIsImV4cCI6MTUxNzU4OTY4NSwiZW1haWwiOiJuaWtpdGFAY29kZS1vbi5iZSJ9.SHKINswXBspQ956FUd6Lfm0zdSXDITa5kvKDcpsACTQ'],
            [10, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6IkFydGVtIiwiZXhwIjoxNTE3NTg5NjU5LCJlbWFpbCI6Im5pa2l0YUBjb2RlLW9uLmJlIn0.gFOmd4sTlLvu3OIdkU0Yh4ExdoQobvVeGQuDgFFRSkc']];
        // const token = tokens[Math.round(Math.random() * 2)];
        const token = tokens[0]
        localStorage.setItem('token', token[1])
        localStorage.setItem('user_id', token[0])
        const user_socket = new WebSocket('ws://0.0.0.0:8000/user?token=' + token[1]);
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
        axios.get('http://localhost:8000/api/private-chats/', config)
            .then((response) => {
                    console.log('dsds')
                    console.log(response.data)
                    this.setState({'chats': response.data})
                    console.log(response.data)
                    console.log('chats in wrap')
                }
            )
    }

    render() {
        const chats = this.state.chats
        return <div>{chats ? < AllChats chats={this.state.chats}/> : ''}</div>
    }
}

function mapStateToProps(state) {
    return {}
}

function mapDispatchToProps(dispatch) {
    return {}
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ChatWrapper))