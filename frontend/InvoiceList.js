import React, { useEffect, useState } from 'react';
import axios from 'axios';

function InvoiceList() {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    async function fetchInvoices() {
      try {
        const response = await axios.get('http://localhost:5000/invoices');
        setInvoices(response.data);
      } catch (error) {
        console.error('Error fetching invoices:', error);
      }
    }

    fetchInvoices();
  }, []);

  return (
    <div>
      <h1>Invoice List</h1>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Vendor</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Location</th>
            <th>Status</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {invoices.map((invoice) => (
            <tr key={invoice.id}>
              <td>{invoice.id}</td>
              <td>{invoice.vendor}</td>
              <td>{invoice.date}</td>
              <td>{invoice.amount}</td>
              <td>{invoice.location || 'N/A'}</td>
              <td>{invoice.status}</td>
              <td>{invoice.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default InvoiceList;