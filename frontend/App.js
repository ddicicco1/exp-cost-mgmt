import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import InvoiceUpload from './InvoiceUpload';
import InvoiceList from './InvoiceList';

function App() {
  return (
    <Router>
      <Switch>
        <Route path='/' exact>
          <h1>Welcome to ECM Dashboard</h1>
        </Route>
        <Route path='/upload-invoice' exact>
          <InvoiceUpload />
        </Route>
        <Route path='/invoices' exact>
          <InvoiceList />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
