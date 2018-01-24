import React from 'react'
import ReactDOM from 'react-dom'
import {Provider} from 'react-redux'
import App from './containers/App'
import Menu from './containers/Menu'
import configureStore from './store/configureStore'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { Router, Route, browserHistory, IndexRoute } from 'react-router'
import { syncHistoryWithStore} from 'react-router-redux'
import './styles/app.css';

const store = configureStore();

const history = syncHistoryWithStore(browserHistory, store);

ReactDOM.render(
		<Provider store={store}>
			<MuiThemeProvider>
			<Router history={history}>
				<Route path="/" component={Menu}>
					<IndexRoute component={App}/>
				</Route>
			</Router>
			</MuiThemeProvider>
		</Provider>,
	document.getElementById('root')	
)


