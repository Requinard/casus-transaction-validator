import React from 'react'

export const TransactionResults = (props) => {
    return (
        <div>
            <h4>Results</h4>

            <p>We found {props.transactions.length} transactions to process</p>

            <p>Out of these, {props.invalidTransactions.length} were invalid</p>

            <table>
                <thead>
                <tr>
                    <th>Transaction</th>
                    <th>Error</th>
                </tr>
                </thead>
                <tbody>
                {props.invalidTransactions.map((transaction, key) => (
                    <tr>
                        <td>{transaction[0]['reference'] || transaction[0]['Reference']}</td>
                        <td>{transaction[1]}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
}
