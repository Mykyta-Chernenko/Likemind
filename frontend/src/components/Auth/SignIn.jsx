import React from 'react';
import { Icon, Input, Button, Checkbox } from 'antd';
import { Field, reduxForm } from 'redux-form'
import {SignIn} from '../../action/SignIn'

const FormSignUp = props => {
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
            <Field type="email" name='email' component={renderField} className="input100" label="Email" />
            <Field type="text" name='username' component={renderField} className="input100" label="Username" />
            <Field type="text" name='first-name' component={renderField} className='input100' label="First name"/>
            <Field type="text" name='last-name' component={renderField} className='input100' label="Last name"/>
            <Field type="password" name='password' component={renderField} className='input100' label="Password"/>
            <Field type="password" name='confirm-password' component={renderField} className='input100' label="Confirm password"/>
            <div className="wrap-input100">
                <button type="submit" disabled={submitting} className="contact100-form-btn">Submit</button>
            </div>
        </form>
    )
}
