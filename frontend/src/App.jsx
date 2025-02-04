import { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button, Modal } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [events, setEvents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [email, setEmail] = useState("");

  useEffect(() => {
    fetch("https://sydney-event-scraper.onrender.com/api/events")
      .then((res) => res.json())
      .then((data) => setEvents(data));
  }, []);

  const handleGetTickets = (event) => {
    setSelectedEvent(event);
    setShowModal(true);
  };

  const handleSubmit = () => {
    fetch("https://sydney-event-scraper.onrender.com/api/submit-email", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
    }).then(() => {
      window.location.href = selectedEvent.booking_link;
    });
  };

  return (
    <div className="main-container">
      <Container>
        <h1 className="text-center my-4">Sydney Events</h1>
        <Row>
          {events
            .filter((event) => event.title && event.date && event.booking_link)
            .map((event, index) => (
              <Col key={index} xs={12} sm={6} md={4} lg={3} className="mb-4">
                <Card className="h-100 shadow">
                  <Card.Body>
                    <Card.Title className="text-center">
                      {event.title}
                    </Card.Title>
                    <Card.Text className="text-center">
                      <strong>Date:</strong> {event.date}
                    </Card.Text>
                  </Card.Body>
                  <Card.Footer className="text-center">
                    <Button
                      variant="primary"
                      onClick={() => handleGetTickets(event)}
                      className="w-100"
                    >
                      Get Tickets
                    </Button>
                  </Card.Footer>
                </Card>
              </Col>
            ))}
        </Row>

        <Modal show={showModal} onHide={() => setShowModal(false)} centered>
          <Modal.Header closeButton>
            <Modal.Title>Get Tickets</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">
                Enter your email to continue
              </label>
              <input
                type="email"
                className="form-control"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Close
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              Continue
            </Button>
          </Modal.Footer>
        </Modal>
      </Container>
    </div>
  );
}

export default App;
