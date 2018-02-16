import React, {Component} from 'react'
import '../../styles/chat.css'
import axios from 'axios'

export class ChatTitle extends Component {
    constructor(props) {
        super(props);
        const config = {
            headers: {'Authorization': 'JWT ' + localStorage.getItem('token')}
        };
        console.log('init')
        const chat = this.props.chat;
        if ('owner' in chat.last_message) {
            axios.get('http://localhost:8000/api/users/' + chat.last_message['owner'] +
                '/?fields=id,username', config)
                .then(respone => {
                    const chat = this.state.chat;
                    chat.user = respone.data
                    this.setState({'chat': chat})
                })
        }
        this.state = {
            'chat': chat,
        }
    }

    ChooseChat = () => {
        this.props.ChooseChat(this.state.chat.id)
    };

    render() {

        const chat = this.state.chat
        const last_message = chat.last_message;
        let el_last_message = 'no last message';
        if ('text' in last_message) {
            el_last_message = last_message.text + ':' + last_message.created_at
        }
        return <li onClick={this.ChooseChat} className="chat-title">
            <div className="avatar">{chat.user ? chat.user.username : ''}</div>
            <div>{el_last_message}</div>
        </li>
    }
}