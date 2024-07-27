"use client";
import ListGroup from "react-bootstrap/ListGroup";
import Accordion from "react-bootstrap/Accordion";

function Menu() {
  return (
    <>
      <Accordion defaultActiveKey={["0"]} alwaysOpen>
        <Accordion.Item eventKey="0">
          <Accordion.Header>Strategy List</Accordion.Header>
          <Accordion.Body>
            <ListGroup as="ol">
              <ListGroup.Item
                onClick={() => {
                  Launch_window();
                }}
                as="li"
              >
                Prior Bar Low Alert
              </ListGroup.Item>
              <ListGroup.Item
                onClick={() => {
                  Launch_window();
                }}
                as="li"
              >
                5X Std Dev
              </ListGroup.Item>
              <ListGroup.Item
                onClick={() => {
                  Launch_window();
                }}
                as="li"
              >
                Close To Prior YT low 
              </ListGroup.Item>
            </ListGroup>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </>
  );
}
function Launch_window() {
  console.log("Cras");
}

export default Menu;
