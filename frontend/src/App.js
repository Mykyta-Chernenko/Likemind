import React, { Component } from 'react';

// Redux
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import { rootReducer } from './redux';

// React Router
import { BrowserRouter, Route } from 'react-router-dom';

// Routes
import { HomePage } from './routes';

import './styles/styles.css';

const logger = createLogger({collapsed: true});  // logs redux actions
const store = createStore(rootReducer, applyMiddleware(thunkMiddleware, logger));


class App extends Component {

  render() {
        return (
            <Provider store={store}>
                <BrowserRouter basename="/">
                <div className="appRoutes">
                    <Route path="/" exact component={HomePage}/>
                </div>
                </BrowserRouter>
            </Provider>
        )
    }
}

export default App;
