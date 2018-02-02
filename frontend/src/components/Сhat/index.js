import React, { Component } from 'react'
//import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import io from 'socket.io-client';
import { withRouter} from 'react-router'
import '../../styles/chat.css'

class Chat extends Component {
    constructor() {
        super();
        this.socket = io('http://0.0.0.0:8000');
        this.state = {
            messages: [
                {id: 0, name: 'Nikita', text: 'lorem ipsum lalalalalallalalallalalal'},
                {id: 0, name: 'Nikita', text: 'lorem ipsum lalalalalallalalallalalal'},
                {id: 2, name: 'Artem', text: 'lorem ipsum lalalalalallalalallalalal'},
                {id: 3, name: 'Den', text: 'lorem ipsum lalalalalallalalallalalal'},
                {id: 0, name: 'Nikita', text: 'lorem ipsum lalalalalallalalallalalal'},
            ]
        }
    }
    onConnect() {

    }
    onDisconnect(data) {

    }
    onEvent() {

    }
    addMessage(e){
        if(e.charCode != 13) return;
        this.setState({
            ...this.state,
             messages: [
                 ...this.state.messages,
                {id: 0, name: 'Nikita', text: this.textInput.value}
            ]
        })
        this.textInput.value = ''
    }
    messageGenerate(messages) {
        let cur_user, tmp, messageToArr;
        return messages.map((message, i) => {
            cur_user = message.id == 0? 'self': 'other'
            messageToArr = message.text.match(/.{1,20}/g);
            tmp = messageToArr.map((value, j) => {
                return (
                  <p key={'p_'+ j + i}>{value}</p>
                )
              })
            return (
                <li className={cur_user} key={'li_chat_' + i}>
                    <div className="avatar">{message.name}</div>
                    <div className="msg">
                        {tmp}
                    </div>
                </li>
            )
        })
    }
    render() {
        return (
            <div className="container-contact100">
                <div className="menu">
                <div className="back"><i className="fa fa-chevron-left"></i> <img src="https://i.imgur.com/DY6gND0.png" draggable="false"/></div>
                <div className="name">Alex</div>
                <div className="last">18:09</div>
            </div>
            <ol className="chat">
                {this.messageGenerate(this.state.messages)}
            </ol>
            <input className="textarea" ref={(txt) => this.textInput = txt} type="text" onKeyPress={this.addMessage.bind(this)} placeholder="Type here!" required/><div className="emojis"></div>
            
            </div>
        )
    }
}

function mapStateToProps(state) {
  return {

  }
}

function mapDispatchToProps(dispatch) {
  return {
    
  }
}

export default  withRouter(connect(mapStateToProps, mapDispatchToProps)(Chat))