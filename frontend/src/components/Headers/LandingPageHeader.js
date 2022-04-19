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
import axios from "axios";
import { useState } from "react";

// reactstrap components
import { Button, Container, Input, FormGroup } from "reactstrap";

// core components
const API = process.env.API
//const API = "http://localhost:8000"

const LandingPageHeader = ( props ) => {
  const [cidadePesquisa, setCidadePesquisa] = useState();
  const [partidoPesquisa, setPartidoPesquisa] = useState();

  let pageHeader = React.createRef();

  React.useEffect(() => {
    if (window.innerWidth < 991) {
      const updateScroll = () => {
        let windowScrollTop = window.pageYOffset / 3;
        pageHeader.current.style.transform =
          "translate3d(0," + windowScrollTop + "px,0)";
      };
      window.addEventListener("scroll", updateScroll);
      return function cleanup() {
        window.removeEventListener("scroll", updateScroll);
      };
    }
  });

  const pesquisa = () => {
    
    if (cidadePesquisa) {
      let url
      if (partidoPesquisa) {
        url = `${API}/cidade/?cidade=${cidadePesquisa}&partido=${partidoPesquisa}`
      } else {
        url = `${API}/cidade/?cidade=${cidadePesquisa}`
      }
      axios.get(url).then( response => {
        props.setData(
          {
            "cidade": cidadePesquisa,
            "partido": partidoPesquisa,
            "data": response.data
          }
        )

        window.scrollTo(0, document.body.scrollHeight)
      })
    } else {
      alert("Digite uma cidade para pesquisa")
    }
  }
  return (
    <>
      <div
        style={{
          backgroundImage:
            "url(" + require("assets/img/mnu.png").default + ")",
        }}
        className="page-header"
        data-parallax={true}
        ref={pageHeader}
      >
        <div className="filter" />
        <Container>
          <div className="motto text-center">
            <h1>A Coisa Tá Branca</h1>
            <h3>Monitor da representatividade negra na política</h3>
            <br />

            <FormGroup>
              <Input 
                type="text" 
                name="cidade" 
                id="cidadePesquisa" 
                placeholder="Cidade"
                value={cidadePesquisa}
                onChange={ e => setCidadePesquisa(e.target.value)}
              />
              <Input 
                type="text" 
                name="partido" 
                id="partidoPesquisa" 
                placeholder="Partido (opcional)"
                value={partidoPesquisa}
                onChange={ e => setPartidoPesquisa(e.target.value)}
              />
            </FormGroup>
            <Button 
              className="btn-round" 
              color="neutral" 
              type="button" 
              onClick={ () => pesquisa()}
              outline
            >
              Pesquisar
            </Button>
          </div>
        </Container>
      </div>
    </>
  );
}

export default LandingPageHeader;
