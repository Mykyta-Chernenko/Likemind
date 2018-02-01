import React from 'react';
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

const FormSignIn = props => {
    return (
        <form className='contact100-form' onSubmit={handleSubmit(SignIn)}>
            <div className='tabs flex-row'>
                <span className="tab contact100-form-title active">
                    Sign Up
                </span>
                <span className="tab contact100-form-title">
                    Sign In
                </span>
            </div>
            <Field type="email" name='email' component={renderField} className="input100" label="Email" />
            <Field type="password" name='password' component={renderField} className='input100' label="Password"/>
            <div className="wrap-input100">
                <button type="submit" disabled={submitting} className="contact100-form-btn">Submit</button>
            </div>
        </form>
    )
}

export default reduxForm({
    form: 'SignInForm',
    validate
})(FormSignIn)