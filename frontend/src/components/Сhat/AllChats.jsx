import React, {Component} from 'react'
import '../../styles/chat.css'
import axios from 'axios'

export class AllChats extends Component {
    constructor(props) {
        super(props);
        console.log('sfrmfsd')
        console.log(this.props.chats)
        const config = {
            headers: {'Authorization': 'JWT ' + localStorage.getItem('token')}
        };
        const self = this;
        this.state = {
            chats: this.props.chats
        };
        let chats = this.state.props
        let promises = []
        for (let i = 0; i < this.props.chats.length; i++) {
            promises.push(axios.get('http://localhost:8000/api/users/' + chats[i].last_message['user_id'] +
                '?fields=id,username', config))
        }
        console.log(chats)
        axios.all(promises)
            .then(axios.spread((...args) => {
                    for (let i = 0; i < args.length; i++) {
                        chats[i].user = args[i].data
                    }
                }
            ))
            .then(this.state = {'chats': chats})

    }

    render() {
        const chats = this.state.chats.map((key, value) => {
            return <li key={key}>
                <div className="avatar">{value.user ? value.user.username : ''}</div>
                <div>{value.last_message.text} {value.last_message.time}</div>
            </li>
        })
        return <ul>
            {chats}
        </ul>
    }
}