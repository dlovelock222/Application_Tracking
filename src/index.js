/*!

=========================================================
* Argon Dashboard Chakra - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-chakra
* Copyright 2022 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-chakra/blob/master/LICENSE.md)

* Design and Coded by Simmmple & Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import ReactDOM from "react-dom";
import { HashRouter, Route, Switch, Redirect } from "react-router-dom";

import AuthLayout from "layouts/Auth.js";
import AdminLayout from "layouts/Admin.js";
import { ChakraProvider } from "@chakra-ui/react";
import { GoogleOAuthProvider } from '@react-oauth/google';
// Custom Chakra theme
import theme from "theme/theme.js";

ReactDOM.render(
  //<userAuthInstance>
    <GoogleOAuthProvider clientId="152282102842-p4um6thhs74sr7r2bi6tumldk6obet65.apps.googleusercontent.com">
      <ChakraProvider theme={theme} resetCss={false} position="relative">
        <HashRouter>
          <Switch>
            <Route path={`/auth`} component={AuthLayout} />
            <Route path={`/admin`} component={AdminLayout} />
            <Redirect from={`/`} to="/admin/dashboard" />
          </Switch>
        </HashRouter>
      </ChakraProvider>
    </GoogleOAuthProvider>,
  //</userAuthInstance>,
  document.getElementById("root")
);
