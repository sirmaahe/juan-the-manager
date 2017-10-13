import React, {Component} from 'react';
import Note from '../components/Note'
import Category from '../components/Category'
import _ from 'lodash'

export default class NotesContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            notes: {'NoName': []},
            activeCategory: 'NoName'
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
            let newNotes = {}

            _.forEach(data, (e) => {
                const category = e.category || 'NoName'

                if (!newNotes[category]) {
                    newNotes[category] = []
                }

                newNotes[category].push(e)
            })

            if (_.isEmpty(newNotes)) {
                this.setState({notes: newNotes})
            }
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
                this.setState({ notes: notes })
            }
        })
    }

    updateCategory(note, name) {
        const token = window.localStorage.accessToken;

        fetch(`/notes/${note.id}/category`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            },
            data: { category: name }
        }).then(response => {
            if ( response.status === 201 ) {
                let notes = this.state.notes;
                let newCategory = notes[name] || [];

                notes[note.category].pop(note);
                newCategory.push(note);

                this.setState({ notes: notes })
            }
        })
    }

    changeCategory(name) {
        this.setState({ activeCategory: name })
    }

    render() {
        return (
            <div>
                <div>{ Object.keys(this.state.notes).map((x, i) => {
                    return <Category key={i} name={x} onClick={ () => {this.changeCategory(x)} }/>
                } ) }</div>

                { this.state.notes[this.state.activeCategory].map( (x, i) => {
                    return <Note
                        key={i} note={x} delete={this.deleteNote}
                        category={ this.state.activeCategory }
                        updateCategory={ this.updateCategory }
                    />
                } ) }
            </div>
        );
    }
}
