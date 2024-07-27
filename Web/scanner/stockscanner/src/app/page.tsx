import NavBar from "../Components/NavBar";
import Menu from "../Components/Menu";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Stack from "react-bootstrap/Stack";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <NavBar />
      <div>
        <br />
      </div>
      <Container fluid>
        <Row>
          <Col sm={3} md={3}>
            <Menu />
          </Col>
          <Col md={9}>
            <Row>
              <Col sm={5}>1</Col>
              <Col sm={5}>2</Col>
              <Col sm={5}>3</Col>
              <Col sm={5}>4</Col>
            </Row>
          </Col>
        </Row>
      </Container>
    </main>
  );
}
