import React, {Component} from 'react';
import Note from '../components/Note'

export default class NotesContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            notes: []
        };

        const token = window.localStorage.accessToken;

        fetch('/notes', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        }).then(response => {
            return response.json()
        }).then(data => {
            this.setState({notes: data})
        })
    }

    deleteNote(note) {
        const token = window.localStorage.accessToken;

        fetch(`/notes/${note.id}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        }).then(response => {
            if ( response.status === 204) {
                let notes = this.state.notes
                notes.pop(note)
                this.setState({notes: notes})
            }
        })
    }

    render() {
        return (
            <div className="App">
                {this.state.notes.map((x, i) => {
                    return <Note key={i} note={x} delete={this.deleteNote}/>
                })}
            </div>
        );
    }
}
