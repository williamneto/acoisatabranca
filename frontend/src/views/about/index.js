import DemoFooter from "components/Footers/DemoFooter";
import IndexNavbar from "components/Navbars/IndexNavbar";
import React from "react";
import { Container } from "reactstrap";

const AboutPage = (props) => {

    return (
        <>
            <IndexNavbar />
            <div
                style={{
                backgroundImage:
                    "url(" + require("assets/img/mnu.png") + ")",
                }}
                className="page-header"
                data-parallax={true}
            >
                <div className="filter" />
                <Container>
                    <div className="motto text-center">
                        <h1>A Coisa Tá Branca</h1>
                    </div>
                </Container>
            </div>
            <div className="main">
                <div className="section text-center">
                    <div className="container">
                        <h1>Sobre</h1>
                        <p>
                            Você provavelmente já ouviu a expressão “a coisa tá preta” sendo utilizada para se referir a uma situação ruim ou desfavorável. É um dito muito comum cujo seu caráter racista passa desapercebido para a maioria. 

                            Pensando em desconstruir este conceito o A Coisa Tá Branca busca analisar a representativade racial nas instâncias democráticas – legislativos e executivos municipais, estaduais e federais – e fazer uma provocação: se a nossa situação política está ruim, é por que ela está branca!

                            Durante séculos o racismo atinge pessoas negras no Brasil, e mesmo com todas as conquistas do século XX, ainda somos prejudicados pelo próprio estado em pleno século XXI. Não apenas assassinando um jovem negro a cada vinte e três minutos, mas também nos negando acesso aos espaços de decisão social, politica e econômica.
                            Representamos cerca de 66,07% da população brasileira e continuamos sub-representados e isso é resultado dos impactos da desigualdade racial que afeta negativamente as nossas vidas em diferentes aspectos, eliminando direitos básicos de uma existência digna de bem viver.
                        </p>
                        <h3>Objetivo</h3>
                        <p>
                            O Brasil é um dos campeões mundiais no quesito de transparência. Temos uma lei de acesso a informação internacionalmente reconhecida e todos os dados não sigilosos referentes aos processos eleitorais que acontecem a cada dois anos são disponibilizados publicamente pelo Tribunal Superior Eleitoral.

                            Sendo assim, o objetivo principal deste projeto é analisar a desigualdade racial e a falta de representatividade nas instâncias políticas. E não apenas a população negra é sub-representada no processo de tomada de decisões, mas também os povos indígenas, as mulheres e a população LGBTQIA+

                            Buscamos utilizar todos os dados públicos disponíveis para analisar e visibilizar estas desigualdades, com o objetivo de chamar a atenção das autoridades constituídas e órgãos partidários para a urgência de agir para que nossos espaços de tomadas de decisão representem de fato a população brasileira.
                        </p>
                    </div>
                </div>
            </div>
            <DemoFooter />
        </>
    )
}

export default AboutPage