import React, {Component} from 'react';
import { Icon, Input, Button, Checkbox } from 'antd';
import { Field, reduxForm } from 'redux-form'
import {SignIn} from '../../action/SignIn'

const validate = values => {
    const errors = {};
    let { email, password } = values;
    if (!email){
        errors.email = 'This field needs to be filled.';
    }
    if (!password){
        errors.password = 'This field needs to be filled.';
    }
    return errors
};

const renderField = ({
     input,
     label,
     className,
     type,
     meta: { touched, error, warning }
 }) => (
    <div className='wrap-input100'>
        <label className='label-input100'>{label}</label>
        <input {...input} className={touched && error? `is-invalid ${className}` : className} placeholder={label} type={type}/>
        <span className="focus-input100"></span>
        {touched &&
        ((error && <span className='invalid-feedback'>{error}</span>) ||
            (warning && <span>{warning}</span>))}
    </div>

);

export class Form extends Component {
    constructor() {
        super()
        this.state = {
            ifSignUp: false
        }
    }
    changeSign = () => {
        this.setState({ ifSignUp: !this.state.ifSignUp })
    }
    render() {
        const { handleSubmit, submitting } = this.props;
        return (
            <form className='contact100-form' onSubmit={handleSubmit(SignIn)}>
                <div className='tabs flex-row'>
                <span className="tab contact100-form-title active" onClick={this.changeSign}>
                        Sign Up
                </span>
                <span className="tab contact100-form-title" onClick={this.changeSign}>
                    Sign In
                </span>
                </div>
                {this.state.ifSignUp? FormSignUp(this.props): FormSignIn(this.props)}
                <div className="wrap-input100">
                    <button type="submit" disabled={submitting} className="contact100-form-btn">Submit</button>
                </div>
            </form>
        )
    }
};


const FormSignIn = props => {
    return (
        <div>
            <Field type="email" name='email' component={renderField} className="input100" label="Email" />
            <Field type="password" name='password' component={renderField} className='input100' label="Password"/>
        </div>
        )
}

const FormSignUp = props => {
    return (
        <div>
            <Field type="email" name='email' component={renderField} className="input100" label="Email" />
            <Field type="text" name='username' component={renderField} className="input100" label="Username" />
            <Field type="text" name='first-name' component={renderField} className='input100' label="First name"/>
            <Field type="text" name='last-name' component={renderField} className='input100' label="Last name"/>
            <Field type="password" name='password' component={renderField} className='input100' label="Password"/>
            <Field type="password" name='confirm-password' component={renderField} className='input100' label="Confirm password"/>
        </div>
    )
}

export default reduxForm({
    form: 'LoginForm',
    validate
})(Form)