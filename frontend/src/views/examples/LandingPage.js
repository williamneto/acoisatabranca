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
              <Col md="3"></Col>
              <Col md="3">
                <div className="info">
                  <div className="icon icon-info">
                    
                  </div>
                  <div className="description">
                    <h3 className="info-title">Candidaturas</h3>
                    <p className="description">
                      <h6>{data.data.total_cands}</h6>
                    </p>
                  </div>
                </div>            
              </Col>
              <Col md="3">
                <div className="info">
                  <div className="icon icon-info">
                    
                  </div>
                  <div className="description">
                    <h3 className="info-title">Eleitas</h3>
                    <p className="description">
                      <h6>{data.data.all_cands_eleitos}</h6>
                    </p>
                  </div>
                </div>  
              </Col>
              <Col md="3"></Col>
            </Row>
            <Row>
              <Col md="6">
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
              <Col md="6">
                <div className="info">
                  <div className="icon icon-info">
                  </div>
                  <div className="description">
                    <h4 className="info-title">Candidaturas pretas eleitas</h4>
                    
                    <h6>{data.data.cands_prets_eleitos}</h6>
                    <h6>{data.data.percent_eleitos_prets}</h6>
                  </div>
                </div>
              </Col> 
            </Row>
            { data.data.partido_doacoes && data.data.partido_doacoes.map( doacoes => {
              return (
                <>
                  <Row>
                    <Col md="4">
                    </Col>
                    <Col md="4">
                      <div className="info">
                        <div className="description">
                          <h3 className="info-title">Recursos distribuidos à candidaturas pelo partido {doacoes.SG_PARTIDO}</h3>
                          <h6>R$ {doacoes.total}</h6>
                        </div>
                      </div>
                    </Col>
                    <Col md="4">
                    </Col>
                  </Row>
                  <Row>
                    <Col md="6">
                      <div className="info">
                        <div className="description">
                          <h5 className="info-title">Para candidaturas brancas</h5>
                          <h6>R$ {doacoes.brancs}</h6>
                          <h6>{doacoes.brancs_percent}</h6>
                        </div>
                      </div>
                    </Col>
                    <Col md="6">
                      <div className="info">
                        <div className="description">
                          <h5 className="info-title">Para candidaturas pretas</h5>
                          <h6>R$ {doacoes.prets}</h6>
                          <h6>{doacoes.prets_percent}</h6>
                        </div>
                      </div>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="6">
                      <div className="info">
                        <div className="description">
                          <h5 className="info-title">Para candidaturas brancas eleitas</h5>
                          <h6>R$ {doacoes.brancs_eleitos}</h6>
                          <h6>{doacoes.brancs_eleitos_percent}</h6>
                        </div>
                      </div>
                    </Col>
                    <Col md="6">
                      <div className="info">
                        <div className="description">
                          <h5 className="info-title">Para candidaturas pretas eleitas</h5>
                          <h6>R$ {doacoes.prets_eleitos}</h6>
                          <h6>{doacoes.prets_eleitos_percent}</h6>
                        </div>
                      </div>
                    </Col>
                  </Row>
                </>
              )
            })}
          </Container>}
        </div>
      </div>
      <DemoFooter />
    </>
  );
}

export default LandingPage;
