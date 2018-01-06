import React, { Component } from 'react'
//import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { withRouter} from 'react-router'

class App extends Component {
    render() {
        return <div className='form'>
        </div>
    }
}

function mapStateToProps(state) {
  return {

  }
}

function mapDispatchToProps(dispatch) {
  return {
    
  }
}

export default  withRouter(connect(mapStateToProps, mapDispatchToProps)(App))