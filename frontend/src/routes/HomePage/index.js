import React, { Component } from 'react';
import { connect } from 'react-redux';

import { Navigation } from '../components';
import { LoginForm } from './components';

import { loginUser, loggedIn } from '../../redux';
// import 'styles.css';


class HomePage extends Component {

	constructor(props) {
		super(props);
		this.handleLoginSubmit = this.handleLoginSubmit.bind(this);
	}

	handleLoginSubmit(formData) {
		const {username, password} = formData;
		this.props.dispatch(loginUser(username, password))
		.then((data) => {
			// console.log('Login Successful :)');
		})
		.catch((error) => {
			// console.log(error);
		});
	}

    render() {
        return (
            <div>
            	<Navigation />
            	{!loggedIn(this.props.user) && <div className="pageWidth padTop-128">
            		<div className="col-4 marginCenter">
                		<LoginForm handleSubmit={this.handleLoginSubmit} formErrors={this.props.form.formErrors || {}}/>
                	</div>
                </div>}
            </div>
        );
    }
}

export default connect(state => {
    return {user: state.user, form: state.form}
})(HomePage)
