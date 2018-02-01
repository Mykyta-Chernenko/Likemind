import React, {Component} from 'react'
import { Menu, Icon } from 'antd';
import { Row, Col } from 'antd';
const SubMenu = Menu.SubMenu;
const MenuItemGroup = Menu.ItemGroup;


class NavigateMenu extends Component {
    state = {
        current: 'mail',
    };
    handleClick = (e) => {
        console.log('click ', e);
        this.setState({
            current: e.key,
        });
    };
    render() {
        return (
            <div className='ant-col-6 ant-col-offset-6'>
                <Row >
                    <Col >
                        <Menu
                            onClick={this.handleClick}
                            selectedKeys={[this.state.current]}
                            mode="horizontal"
                        >
                            <Menu.Item key="mail">
                                <Icon type="mail" />Login
                            </Menu.Item>
                            <Menu.Item key="app">
                                <Icon type="appstore" />SignIn
                            </Menu.Item>
                        </Menu>
                    </Col>
                </Row>
                {this.props.children}
            </div>
        );
    }
}

export default NavigateMenu;