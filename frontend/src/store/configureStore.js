import { createStore, applyMiddleware } from 'redux'
import rootReducer from '../reducers'
//import createLogger from 'redux-logger'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension';
import { routerMiddleware} from 'react-router-redux'

import { history } from './history'

const middleware = routerMiddleware(history);

/* eslint-disable no-underscore-dangle */
export default function configureStore(initialState) {
    const store = createStore(
        rootReducer,
        initialState,
        composeWithDevTools(applyMiddleware(thunk, middleware))
    );
    /* eslint-disable no-underscore-dangle */
    if (module.hot) {
        module.hot.accept('../reducers', () => {
            const nextRootReducer = require('../reducers');
            store.replaceReducer(nextRootReducer)
        })
    }

    return store
};