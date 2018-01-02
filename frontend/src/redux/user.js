import fetch from 'isomorphic-fetch';

import { logOut, saveUser, getUser, handleResponse, handleError } from './lib';


export const LOGOUT_USER = 'LOGOUT_USER';
export function logoutUser() {
    logOut();
    return {type: LOGOUT_USER}
}


const LOGIN_USER_REQUEST = 'LOGIN_USER_REQUEST';
const LOGIN_USER_RESPONSE = 'LOGIN_USER_RESPONSE';
export function loginUser(username, password) {
    return (dispatch, getState) => {

        const payload = {username, password};

        dispatch({type: LOGIN_USER_REQUEST, payload});

        return fetch(`/api/obtain-auth-token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
        .then(handleResponse(dispatch, LOGIN_USER_RESPONSE))
        .then((json) => {
            saveUser(json);
            return json;
        })
        .catch(handleError(dispatch, LOGIN_USER_RESPONSE))
    }
}


export function userReducer(state = getUser, action) {

    if (typeof state === 'function') {
        state = state() || {};
    }

    switch (action.type) {
        case LOGIN_USER_RESPONSE:
            if (action.error === true) return state;
            else return {...state, ...action.payload};
        default:
            return state;
    }
}
