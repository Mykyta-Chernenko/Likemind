import React, { Component } from 'react'
import { connect } from 'react-redux'

import { ConnectedRouter } from 'react-router-redux'

import { history } from '../store/history'

import { Switch, Route, Redirect } from 'react-router'
// import { PrivateRoute } from './PrivateRoute'
import { Auth, Menu, Chat, TestChat } from '../components'

class Routes extends Component {
    render() {
        return (
            <ConnectedRouter history={history}>
                <Switch>
                    <Route exact path='/' component={Auth}/>
                    <Route path='/chat' component={TestChat}/>
                    <Redirect to='/'/>
                </Switch>
            </ConnectedRouter>
        )
    }
}

function mapStateToProps(state, ownProps) {

    return Object.assign({},...state, ...ownProps)
}

function mapDispatchToProps(dispatch) {
    return {
        ...dispatch
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Routes)