// User utility functions
export function loggedIn(user) {
    if (!!user) {
        return !!user.token;
    } else {
        return !!getUser();
    }
}

export function logOut() {
    localStorage.clear()
}

export function saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

export function getUser() {
    try {
        return JSON.parse(localStorage.user)
    }
    catch(e) {
        return null;
    }
}


// Common response handling
import { setFormErrors, clearFormErrors } from './form.js';

function responseError(response) {
    const error = new Error();
    error.response = response;
    return error;
}

export function handleResponse(dispatch, actionType) {
    return (response) => {
        if (response.ok) {
            return response.json().then(json => {
                dispatch({type: actionType, payload: json});
                dispatch(clearFormErrors());
                return json;
            });
        }
        else if (response.status === 400) {
            response.json().then(json => {
                dispatch(setFormErrors(json));
            });
        }
        throw responseError(response);
    }
}

export function handleError(dispatch, actionType) {
    return (error) => {
        const {response} = error;
        dispatch({type: actionType, payload: error, meta: response, error: true});
        throw error;
    }
}
