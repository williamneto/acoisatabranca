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
import React, { useEffect } from "react";
import axios from "axios";
import { useState } from "react";
import Select from 'react-select'

// reactstrap components
import { Button, Container, FormGroup, Row, Col } from "reactstrap";

// core components
const API = "http://acoisatabranca.com.br:8000"
//const API = "http://localhost:8000"

const LandingPageHeader = ( props ) => {
  const [ufPesquisa, setUfPesquisa] = useState()
  const [cidadePesquisa, setCidadePesquisa] = useState();
  const [partidoPesquisa, setPartidoPesquisa] = useState();

  const [ufsOptions, setUfsOptions] = useState([])
  const [cidadesOptions, setCidadesOptions] = useState([])
  const [partidosOptions, setPartidosOptions] = useState([])

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
        if (response.data.total_cands > 0){
          props.setSearchFail(false)
          props.setData(
            {
              "cidade": cidadePesquisa,
              "partido": partidoPesquisa,
              "data": response.data
            }
          )
        } else {
          props.setSearchFail(true)
        }

        window.scrollTo(0, document.body.scrollHeight)
      })
    } else {
      alert("Digite uma cidade para pesquisa")
    }
  }

  const getUfsOptions = () => {
    axios.get(`${API}/estados/`).then( response => {
      let ufsOptions = []
      for ( let uf of response.data) {
        ufsOptions.push(
          {
            "value": uf,
            "label": uf
          }
        )
      }

      setUfsOptions(ufsOptions)
    })
  }

  const getCidadesOptions = (uf) => {
    axios.get(`${API}/cidades/?uf=${uf}`).then( response => {
      let cidadesOptions = []
      for ( let cidade of response.data) {
        cidadesOptions.push(
          {
            "value": cidade.NM_UE,
            "label": cidade.NM_UE
          }
        )
      }

      setCidadesOptions(cidadesOptions)
    })
  }

  const getPartidosOptions = () => {
    axios.get(`${API}/partidos/`).then( response => {
      let partidosOptions = []
      for ( let partido of response.data) {
        partidosOptions.push(
          {
            "value": partido.SG_PARTIDO,
            "label": partido.SG_PARTIDO
          }
        )
      }

      setPartidosOptions(partidosOptions)
    })
  }

  const handleUfChange = uf => {
    console.log(uf)
    console.log(ufsOptions)
    if ( ufsOptions.includes(uf) ) {
      setUfPesquisa(uf.value)
      getCidadesOptions(uf.value)
    }
  }

  useEffect( () => {
    getUfsOptions()
  }, [])

  useEffect( () => {
    getPartidosOptions()
  }, [])

  const colourStyles = {
    control: styles => ({ ...styles, backgroundColor: 'white' }),
    option: (styles, { data, isDisabled, isFocused, isSelected }) => {
      const color = "black";
      return {
        ...styles,
        color: color,
        cursor: isDisabled ? 'not-allowed' : 'default',
      };
    },
  };
  return (
    <>
      <div
        style={{
          backgroundImage:
            "url(" + require("assets/img/mnu.png") + ")",
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

            <Row>
              <Col>
                <FormGroup>
                  <Select 
                    options={ufsOptions} 
                    placeholder="UF"
                    onChange={ e => handleUfChange(e)}
                    defaultValue={ufPesquisa}
                    styles={colourStyles}
                  />
                  
                </FormGroup>
              </Col>
              
              <Col>
            <FormGroup>
              <Select 
                options={cidadesOptions} 
                placeholder="Cidade"
                onChange={ e => setCidadePesquisa(e.value)}
                defaultValue={cidadePesquisa}
                styles={colourStyles}
              />
                </FormGroup>
              </Col>
            </Row>

            <Row>
              <Col>
                <FormGroup>
              <Select 
                options={partidosOptions} 
                placeholder="Partido (opcional)"
                onChange={ e => setPartidoPesquisa(e.value)}
                defaultValue={partidoPesquisa}
                styles={colourStyles}
              />
            </FormGroup>
              </Col>
            </Row>

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
