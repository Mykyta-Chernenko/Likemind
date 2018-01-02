const SET_FORM_ERRORS = 'SET_FORM_ERRORS';
export function setFormErrors(formErrors) {
    return {
        type: SET_FORM_ERRORS,
        payload: formErrors
    }
}

const CLEAR_FORM_ERRORS = 'CLEAR_FORM_ERRORS';
export function clearFormErrors() { return {type: CLEAR_FORM_ERRORS} }


export function formReducer(state = {}, action) {
    switch (action.type) {
        case CLEAR_FORM_ERRORS:
            return {...state, ...{formErrors: {}}}
        case SET_FORM_ERRORS:
            return {...state, ...{formErrors: action.payload}};
        default:
            return state;
    }
}
