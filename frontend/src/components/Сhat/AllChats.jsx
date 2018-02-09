import React, {Component} from 'react'
import '../../styles/chat.css'
import axios from 'axios'
import {ChatTitle} from './ChatTitle'

export class AllChats extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chats: this.props.chats
        };
        console.log(this.props.chats)

    }
    render() {

        const chats = this.state.chats.map((value, key) => {
            return <ChatTitle key={key} chat={value}/>
        });
        return <ul className="chat">
            {chats}
        </ul>
    }
}