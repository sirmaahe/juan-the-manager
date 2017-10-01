import React, {Component} from 'react';
import Note from '../components/Note'

export default class NotesContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            nodes: []
        };

        const token = window.localStorage.accessToken;

        fetch('/notes', {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
            return response.json()
        }).then(data => {
            this.setState({nodes: data})
        })
    }

    render() {
        return (
            <div className="App">
                {this.state.nodes.map((x, i) => {
                    return <Note key={i} note={x}/>
                })}
            </div>
        );
    }
}
