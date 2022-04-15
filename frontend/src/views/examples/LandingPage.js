/*!

=========================================================
* Paper Kit React - v1.3.0
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-kit-react

* Copyright 2021 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/paper-kit-react/blob/main/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";

// reactstrap components
import {
  Container,
  Row,
  Col,
} from "reactstrap";

// core components
import LandingPageHeader from "components/Headers/LandingPageHeader.js";
import DemoFooter from "components/Footers/DemoFooter.js";
import { useState } from "react";

const LandingPage = ( props ) => {
  const [data, setData] = useState()
  const mainContent = React.useRef();

  document.documentElement.classList.remove("nav-open");
  React.useEffect(() => {
    document.body.classList.add("profile-page");
    return function cleanup() {
      document.body.classList.remove("profile-page");
    };
  });
  
  React.useEffect(() => {
    if(mainContent.current && data) mainContent.current.focus(); 
   }, [mainContent]);

  return (
    <>
      
      <LandingPageHeader setData={setData} mainContent={mainContent}/>
      <div className="main" ref={mainContent}>
        <div className="section text-center">
          { data && <Container>
            <Row>
              <Col className="ml-auto mr-auto" md="8">
                <h2 className="title">{data.cidade}</h2>
                <h5 className="description">
                  {data.partido}
                </h5>
                <br />
                
              </Col>
            </Row>
            <br />
            <br />
            <Row>
              <Col md="4">
                <div className="info">
                  <div className="icon icon-info">
                    
                  </div>
                  <div className="description">
                    <h4 className="info-title">Candidaturas</h4>
                    <p className="description">
                      <h6>{data.data.total_cands}</h6>
                    </p>
                  </div>
                </div>
              </Col>
              <Col md="4">
                <div className="info">
                  <div className="icon icon-info">
                  </div>
                  <div className="description">
                    <h4 className="info-title">Candidaturas pretas</h4>
                    <p>
                    <h6>{data.data.cands_prets}</h6>
                    </p>
                    <p>
                      <h6>{data.data.percent_cands_prets}</h6>
                    </p>
                  </div>
                </div>
              </Col>
              <Col md="4">
                <div className="info">
                  <div className="icon icon-info">
                  </div>
                  <div className="description">
                    <h4 className="info-title">Candidaturas pretas eleitas</h4>
                    <p>
                      <h6>{data.data.cands_prets_eleitos}</h6>
                    </p>
                    <p>
                      <h6>{data.data.percent_eleitos_prets}</h6>
                    </p>
                  </div>
                </div>
              </Col>
              
            </Row>
          </Container>}
        </div>
      </div>
      <DemoFooter />
    </>
  );
}

export default LandingPage;
