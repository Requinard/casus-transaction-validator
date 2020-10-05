import React, {useState} from 'react';
import axios from 'axios';
import {Form, Field} from 'react-final-form'
import './App.css';
import {TransactionResults} from "./TransactionResults";

function App() {
    const [transactions, setTransactions] = useState([])
    const [invalidTransactions, setInvalidTransactions] = useState([])
    const [error, setError] = useState("")
    const [baseUrl, setUrl] = useState("http://localhost:8000") // #todo find the proper URL. Use it from the base url
    const fileId = 'file'

    const sendToServer = async (data) => {
        // Reset
        setTransactions([])
        setInvalidTransactions([])

        let formData = new FormData();
        const file = document.getElementById(fileId).files[0];

        formData.append('file', file, data['file'])

        try {
            const response = await axios.post(`${baseUrl}/transactions/validate/upload`, formData, {
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
            setError(e)
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
                              <Field name='file' type='file' id='file' component='input' id={fileId}/>
                              <button type='submit'>Submit</button>
                          </form>
                      )}
                />

                {error ? <p>{error.toString()}</p> : <div/>}

                {transactions.length > 0 ?
                    <TransactionResults transactions={transactions} invalidTransactions={invalidTransactions}/> :
                    <div/>}
            </header>
        </div>
    );
}

export default App;
