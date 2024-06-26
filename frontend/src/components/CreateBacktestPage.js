import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import "react-datepicker/dist/react-datepicker.css";
import DatePicker from "react-datepicker";
import Select from "react-select";
import { fetchBacktestResults } from "../services/apiService"; // Import the API function

const CreateBacktestPage = () => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [selectedCoin, setSelectedCoin] = useState(null);
  const [initialCash, setInitialCash] = useState("");
  const [fmwValue, setFmwValue] = useState("");
  const [smwValue, setSmwValue] = useState("");
  const [stakeValue, setStakeValue] = useState("");

  const coinOptions = [
    { value: "ETH", label: "Ethereum" },
    { value: "BTC", label: "Bitcoin" },
    { value: "SOL", label: "Solana" },
    { value: "BNB", label: "Binance Coin" },
  ];

  const handleChange = (selectedOption) => {
    setSelectedCoin(selectedOption);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Prepare data for API call
    const requestData = {
      startDate,
      endDate,
      selectedCoin: selectedCoin ? selectedCoin.value : "",
      initialCash,
      fmwValue,
      smwValue,
      stakeValue,
    };

    try {
      const data = await fetchBacktestResults(
        requestData.startDate,
        requestData.endDate,
        requestData.selectedCoin,
        requestData.initialCash,
        requestData.smwValue,
        requestData.fmwValue,
        requestData.stakeValue
      );
      // Handle API response data
      console.log("API Response:", data);
      // Reset form state if needed
      resetForm();
    } catch (error) {
      console.error("Error fetching backtest results:", error);
      // Handle errors if necessary
    }
  };

  const resetForm = () => {
    setStartDate(null);
    setEndDate(null);
    setSelectedCoin(null);
    setInitialCash("");
    setFmwValue("");
    setSmwValue("");
    setStakeValue("");
  };

  return (
    <div className="form">
      <form onSubmit={handleSubmit}>
        <div className="date-container">
          <Form.Group>
            <Form.Label>Start Date</Form.Label>
            <DatePicker
              selected={startDate}
              onChange={(date) => setStartDate(date)}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>End Date</Form.Label>
            <DatePicker
              selected={endDate}
              onChange={(date) => setEndDate(date)}
            />
          </Form.Group>
        </div>
        <br />
        <Form.Group>
          <Form.Label>Coin</Form.Label>
          <Select
            value={selectedCoin}
            options={coinOptions}
            onChange={handleChange}
          />
        </Form.Group>
        <br />
        <Form.Group>
          <Form.Label>SMW</Form.Label>
          <Form.Control
            type="text"
            placeholder="smw"
            value={smwValue}
            onChange={(e) => setSmwValue(e.target.value)}
          />
        </Form.Group>
        <br />
        <Form.Group>
          <Form.Label>FMW</Form.Label>
          <Form.Control
            type="text"
            placeholder="fmw"
            value={fmwValue}
            onChange={(e) => setFmwValue(e.target.value)}
          />
        </Form.Group>
        <br />
        <Form.Group>
          <Form.Label>No. of Stake</Form.Label>
          <Form.Control
            type="text"
            placeholder="Run location"
            value={stakeValue}
            onChange={(e) => setStakeValue(e.target.value)}
          />
        </Form.Group>
        <br />
        <Form.Group>
          <Form.Label>Initial Cash</Form.Label>
          <Form.Control
            type="text"
            placeholder="Initial Cash"
            value={initialCash}
            onChange={(e) => setInitialCash(e.target.value)}
          />
        </Form.Group>
        <br />
        <Form.Group>
          <Form.Label>Run Location</Form.Label>
          <Form.Control type="text" placeholder="Run location" />
        </Form.Group>
        <br />
        <Form.Group>
          <Button type="submit" variant="primary">
            Create Scene
          </Button>
        </Form.Group>
        <br />
      </form>
    </div>
  );
};

export default CreateBacktestPage;

