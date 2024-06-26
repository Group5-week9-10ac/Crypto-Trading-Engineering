import React, { useState } from "react";

import { Form, Button } from "react-bootstrap";
import "react-datepicker/dist/react-datepicker.css";
import DatePicker from "react-datepicker";
import Select from "react-select";

const Createback = () => {
  const [startDate, setstartDate] = useState(null);
  const [endDate, setendDate] = useState(null);
  const [selectedCoin, setselectedCoin] = useState(null);
  const [initialCash, setinitialCash] = useState("");
  const [fmwValue, setfmwValue] = useState("");
  const [smwValue, setsmwValue] = useState("");
  const [stakeValue, setStakeValue] = useState("");

  const coin = [
    {
      value: 1,
      label: "ETH",
    },
    {
      value: 2,
      label: "BTC",
    },
    {
      value: 3,
      label: "SOL",
    },
    {
      value: 4,
      label: "BNB",
    },
  ];
  const handleChange = (obj) => {
    setselectedCoin(obj);
  };
  const handleChangeCash = (event) => {
    const result = event.target.value.replace(/\D/g, "");

    setinitialCash(result);
  };
  const handleChangeStake = (event) => {
    const result = event.target.value.replace(/\D/g, "");

    setStakeValue(result);
  };
  const handleChangesmwValue = (event) => {
    const result = event.target.value.replace(/\D/g, "");

    setsmwValue(result);
  };
  const handleChangefmwValue = (event) => {
    const result = event.target.value.replace(/\D/g, "");

    setfmwValue(result);
  };
  return (
    <>
      <div className="form">
        <form>
          <div className="date-container">
            <Form.Group>
              <Form.Label>Start Date</Form.Label>
              <DatePicker
                selected={startDate}
                onChange={(date) => setstartDate(date)}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>End Date</Form.Label>
              <DatePicker
                selected={endDate}
                onChange={(date) => setendDate(date)}
              />
            </Form.Group>
          </div>
          <br></br>
          <Form.Group>
            <Form.Label>Coin</Form.Label>
            <Select
              value={selectedCoin}
              options={coin}
              onChange={handleChange}
            />
          </Form.Group>
          <br></br>
          <Form.Group>
            <Form.Label>SMW</Form.Label>
            <Form.Control
              type="text"
              placeholder="smw"
              value={smwValue}
              onChange={handleChangesmwValue}
            ></Form.Control>
          </Form.Group>
          <br></br>
          <Form.Group>
            <Form.Label>FMW</Form.Label>
            <Form.Control
              type="text"
              placeholder="fmw"
              value={fmwValue}
              onChange={handleChangefmwValue}
            ></Form.Control>
          </Form.Group>
          <br></br>
          <Form.Group>
            <Form.Label>No. of Stake</Form.Label>
            <Form.Control
              type="text"
              placeholder="Run location"
              value={stakeValue}
              onChange={handleChangeStake}
            ></Form.Control>
          </Form.Group>
          <br></br>
          <Form.Group>
            <Form.Label>Initial Cash</Form.Label>
            <Form.Control
              type="text"
              placeholder="Initial Cash"
              value={initialCash}
              onChange={handleChangeCash}
            ></Form.Control>
          </Form.Group>
          <br></br>
          <Form.Group>
            <Form.Label>Run Location</Form.Label>
            <Form.Control type="text" placeholder="Run location"></Form.Control>
          </Form.Group>
          <br></br>
          <Form.Group>
            <Button as="sub" variant="primary">
              Create Scene
            </Button>
          </Form.Group>
          <br></br>
        </form>
      </div>
    </>
  );
};

export default Createback;
