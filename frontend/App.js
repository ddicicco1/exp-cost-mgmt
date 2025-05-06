import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import InvoiceUpload from './InvoiceUpload';

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
      </Switch>
    </Router>
  );
}

export default App;
