import { SubmissionError } from 'redux-form';
import axios from 'axios'
export const SignIn = (val, dispatch) => {
    dispatch({
        type: 'LOGIN_LOAD'
    });
    return axios.post('oauth/authorize',{
        val
    })
        .then( req => req.json())
        .then(
            json => {
                localStorage.setItem('token', json);
                dispatch({type: 'LOGIN_SUCCESS'})
            },
            err => {
                dispatch({type: 'LOGIN_FAILURE'})
            }
        )

};
