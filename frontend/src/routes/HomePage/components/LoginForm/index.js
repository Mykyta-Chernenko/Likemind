import React, { Component } from 'react';
import PropTypes from 'prop-types';

import './styles.css';


class LoginFormPresentation extends Component {

    nonFieldErrors() {
        return this.props.formErrors.non_field_errors.map((item, index) => {
            return (
                <div key={index} className="formError">
                    <span>{item}</span>
                </div>
            )
        });
    }

    getInputClassName(name) {
        const classes = ['inputControl', 'marginTop-24'];
        if (!!this.props.formErrors[name]) classes.push('error');
        return classes.join(' ')
    }

    fieldError(name) {
        const error = this.props.formErrors[name];
        return error && <div className="formError"><span>{error}</span></div>
    }

    render() {
        const formData = this.props.formData;
        return (
            <form className="loginForm" onSubmit={this.props.onSubmit}>
                {this.props.formErrors.non_field_errors && this.nonFieldErrors()}
                <input type="text" name="username" value={formData.username || ''} className={this.getInputClassName('email')} onChange={this.props.onChange} placeholder="username"/>
                {this.fieldError('username')}
                <input type="password" name="password" value={formData.password || ''} className={this.getInputClassName('email')} onChange={this.props.onChange} placeholder="password"/>
                {this.fieldError('password')}
                <button type="submit" className="btn btnGreen marginTop-24">login</button>
            </form>
        )
    }
}

LoginFormPresentation.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
    formData: PropTypes.object.isRequired,
    formErrors: PropTypes.object.isRequired,
}

class LoginFormContainer extends Component {

    constructor(props) {
        super(props);
        this.state = {
            formData: this.props.formData || {},
            formErrors: this.props.formErrors || {}
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleInputChange(e) {
        const target = e.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            formData: {...this.state.formData, [name]: value}
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        this.props.handleSubmit(this.state.formData);
    }

    render() {
        return (
            <LoginFormPresentation onSubmit={this.handleSubmit} onChange={this.handleInputChange} formData={this.state.formData} formErrors={this.props.formErrors}/>
        )
    }
}

export default LoginFormContainer;
