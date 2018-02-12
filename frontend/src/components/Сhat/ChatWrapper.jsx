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
        const auth_credits = [
            // [nikita, 'q'],
            // [artem, 'q'],
            {'username': 'denis', 'password': 'q'}];
        const auth = auth_credits[Math.round(Math.random() * 0)];
        axios.post('http://localhost:8000/api/obtain-auth-token/',
            {
                'username': auth['username'],
                'password': auth['password']
            })
            .then(response => {
                localStorage.setItem('token', response.data['token'])
                return response.data['token']
            })
            .then((token) => {
                const config = {
                    headers: {'Authorization': 'JWT ' + token}
                };
                axios.get('http://localhost:8000/api/self-users/?fields=id', config)
                    .then(response => {
                        localStorage.setItem(['user_id', response.data['id']])
                    });
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
                axios.get('http://localhost:8000/api/private-chats/', config)
                    .then((response) => {
                            this.setState({'chats': response.data})
                        }
                    )
            });

        this.state = {
            chats: []
        };
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