import React, {Component} from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'
import '../../styles/chat.css'
import {AllChats} from './AllChats'
import axios from 'axios'
import {Chat} from "./Chat";

const TEXT_MESSAGE = 'text_message';

export class ChatWrapper extends Component {
    constructor() {
        super();
        const auth_credits = [
            {'username': 'denis', 'password': 'q'},
            {'username': 'nikita', 'password': 'q'},
            {'username': 'artem', 'password': 'q'}];
        const auth = auth_credits[Math.round(Math.random() * 2)];
        axios.post('http://localhost:8000/api/obtain-auth-token/',
            {
                'username': auth['username'],
                'password': auth['password']
            })
            .then(response => {
                localStorage.setItem('token', response.data['token']);
                return response.data['token']
            })
            .then((token) => {
                console.log('token' + token)
                const config = {
                    headers: {'Authorization': 'JWT ' + token}
                };
                axios.get('http://localhost:8000/api/self-users/?fields=id', config)
                    .then(response => {
                        localStorage.setItem('user_id', response.data['id'])
                    });
                const user_socket = new WebSocket('ws://0.0.0.0:8000/user/?token=' + token);
                user_socket.onopen = () => {
                    console.log("User chat_socket open");
                };
                user_socket.onmessage = (event) => {
                    console.log('user event')
                    const data = JSON.parse(event.data);
                    if (data.type === TEXT_MESSAGE) {
                        const action = data.action;
                        const chats = this.state.chats
                        for (let i = 0; i < chats.length; i++) {
                            if (chats[i].id === action.chat) {
                                chats[i].last_message = action
                            }
                        }
                        this.setState({'chats': chats})
                    }

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
            chats: [],
            current_chat: null,
        };
    }

    ChooseChat = (chat_id) => {
        console.log(chat_id);
        this.setState({'current_chat': chat_id})
    };

    render() {
        const chats = this.state.chats;
        return <div className="chat-display">
            {chats.length ? < AllChats chats={this.state.chats} ChooseChat={this.ChooseChat}/> : ''}
            {this.state.current_chat ? <Chat key={this.state.current_chat} chat_id={this.state.current_chat}/> : ''}
        </div>
    }
}

function mapStateToProps(state) {
    return {}
}

function mapDispatchToProps(dispatch) {
    return {}
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ChatWrapper))