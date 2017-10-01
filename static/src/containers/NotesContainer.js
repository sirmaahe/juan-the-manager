import React, {Component} from 'react';
import Note from '../components/Note'

export default class NoteContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            nodes: ['---------', '----------']
        };

        fetch('/notes').then(response => {
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
