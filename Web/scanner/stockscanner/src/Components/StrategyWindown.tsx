"use client";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import Navbar from "react-bootstrap/Navbar";

export default function NavBar() {
  return (
    <>
      <Navbar bg="primary" data-bs-theme="dark">
        <Container>
          <Navbar.Brand href="#home">Trading Scan</Navbar.Brand>
          <Row>
            <Nav className="me-auto">
              <NavDropdown title="Logged User " id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Settings</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">Logout</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Row>
        </Container>
      </Navbar>
    </>
  );
}
