import { combineReducers } from 'redux';

import { formReducer } from './form';
import { userReducer, LOGOUT_USER } from './user';


const reducers = combineReducers({
	form: formReducer,
    user: userReducer,
});

const rootReducer = (state, action) => {
    if (action.type === LOGOUT_USER) {
        state = undefined;  // Return state back to initial on logout
    }
    return reducers(state, action)
};


export default rootReducer;
