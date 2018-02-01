import React, { Component } from 'react'
//import { bindActionCreators } from 'redux'
import Form from './Form.jsx'
import { connect } from 'react-redux'

import { withRouter} from 'react-router'
import '../../styles/auth.css'

class Auth extends Component {
    render() {
        return (
            <div className="container-contact100">
                <div className="wrap-contact100">
                    <Form/>
                        <div className="contact100-more flex-col-c-m" style={{background: "linear-gradient(120grad, #643986, #98aed5)"}}>
                    </div>
                </div>
            </div>
        )
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

export default  withRouter(connect(mapStateToProps, mapDispatchToProps)(Auth))