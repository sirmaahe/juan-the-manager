import React, {Component} from 'react';

export default class LoginContainer extends Component {
    doAuth(e) {
        e.preventDefault();

        const form = e.target;
        let payload = {};

        form.childNodes.forEach( elem => {
            if ( elem.name ) {
                payload[elem.name] = elem.value
            }
        });

        fetch( '/auth', {
            method: "POST",
            body: JSON.stringify(payload)
        }).then( data => {
            return data.json()
        }).then( json => {
            this.props.setToken( json.access_token );
        })
    }
    render() {
        return (
            <div>
                <form onSubmit={ e => this.doAuth( e ) }>
                    <input name="username" type="text"/>
                    <input name="password" type="password"/>
                    <input type="submit"/>
                </form>
            </div>
        );
    }
}
