import React, {useState} from 'react';
import axios from 'axios';
import {Form, Field} from 'react-final-form'
import './App.css';
import {TransactionResults} from "./TransactionResults";

function App() {
    const [transactions, setTransactions] = useState([])
    const [invalidTransactions, setInvalidTransactions] = useState([])
    const [error, setError] = useState("")

    const sendToServer = async (data) => {
        // Reset
        setTransactions([])
        setInvalidTransactions([])
        setError("")

        let formData = new FormData();
        const file = document.getElementById('file').files[0];

        if (file === undefined) {
            setError("Please select a file")
            return
        }
        let url = data['backend']

        formData.append('file', file, data['file'])

        try {
            const response = await axios.post(`${url}/transactions/validate/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })

            setError("")
            const data = response.data

            setTransactions(data['raw_transactions'])
            setInvalidTransactions(data['invalid_transactions'])
        } catch (e) {
            console.log(e)

            if (e.response) {
                setError(e.response.data['detail'])
            } else {
                setError(e)
            }
        }
    }

    return (
        <div className="App">
            <header className="App-header">
                <h2>Acme Transaction Checker</h2>
                <Form onSubmit={sendToServer}
                      render={({handleSubmit}) => (
                          <form onSubmit={handleSubmit}>
                              <h4>Upload your file here</h4>
                              <Field name='file' type='file' component='input' id='file'/> <br/>
                              <Field name='backend' type='text' component='input' defaultValue="http://localhost:8000"/>
                              <br/>
                              <button type='submit'>Submit</button>
                          </form>
                      )}
                />

                {error ? <p style={{color: 'red'}}>{error.toString()}</p> : <div/>}

                {transactions.length > 0 ?
                    <TransactionResults transactions={transactions} invalidTransactions={invalidTransactions}/> :
                    <div/>}
            </header>
        </div>
    );
}

export default App;
