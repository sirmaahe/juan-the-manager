import React, {Component} from 'react';
import NotesContainer from './containers/NotesContainer'
import LoginContainer from './containers/LoginContainer'

class App extends Component {
    constructor(props) {
        super(props);

        let token = window.localStorage.accessToken;
        this.state = {
            access_token: token
        };
    }

    setToken(token) {
        window.localStorage.accessToken = token;
        this.setState( {access_token: token} );
    }

    render() {
        return (
            <div className="App">
                { this.state.access_token? <NotesContainer/>: <LoginContainer setToken={ () => this.setToken }/>}
            </div>
        );
    }
}

export default App;
