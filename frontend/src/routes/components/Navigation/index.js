import React, { Component } from 'react';
import { connect } from 'react-redux';

import { logoutUser, loggedIn } from '../../../redux';

import './styles.css';


class Navigation extends Component {

    constructor(props) {
        super(props);

        this.handleLogout = this.handleLogout.bind(this);
    }

    handleLogout(e) {
        e.preventDefault();
        this.props.dispatch(logoutUser());
    }

    render() {
        const user = this.props.user;
        return (
            <div className="nav">
            	<div className="inner pageWidth">
                    <div className="left">
                        <ul>
                            <li><a href="#">Home</a></li>
                        </ul>
                    </div>
                    <div className="right">
                        <ul>
                            {loggedIn(user) && <li><a href="#">{user.username}</a></li>}
                            {loggedIn(user) && <li><a href="#" onClick={this.handleLogout}>logout</a></li>}
                        </ul>
                    </div>
                </div>
            </div>
        );
    }
}

export default connect(state => {
    return {user: state.user}
})(Navigation)
