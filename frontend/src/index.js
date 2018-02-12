<<<<<<< HEAD
import './bootstrap.js'
import './node_modules/index.jsx'
=======
import React from 'react'
import ReactDOM from 'react-dom'
import {Provider} from 'react-redux'


import configureStore from './store/configureStore'
import './styles/app.css';
import 'antd/dist/antd.css'

import Routes from './routers'

const store = configureStore();

ReactDOM.render(
	<Provider store={store}>
		<Routes/>
	</Provider>,
	document.getElementById('root')	
);

>>>>>>> 7eb01113cd9d52818151f89b18e15404b0337167
