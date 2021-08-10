import React, { Component } from 'react';
import DatePicker from 'react-date-picker';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Bar, BarChart } from 'recharts';

export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            testGetResult: null,
            isDataFetched: false,
            startDate: new Date(),
            endDate: new Date(),
            stockSymbol: "",
            buttonClicked: false,
            isNewDataFetched: false,
            noData: false,
            low: null,
            high: null,
            median: null,
            quarter: null,
            three_quarters: null,
            data_list: null,
            frequencies: null,
            all_data: null,
        };

        this.startDateUpdated = this.startDateUpdated.bind(this)
        this.endDateUpdated = this.endDateUpdated.bind(this)
        this.symbolUpdated = this.symbolUpdated.bind(this)
        this.buttonClicked = this.buttonClicked.bind(this)
        // this.testGetRequest = this.testGetRequest.bind(this)
        // this.testGetRequest();
        
    }

    symbolUpdated(event) {
        this.setState({ stockSymbol: event.target.value})
        // console.log(event.target.value)
    }

    startDateUpdated(event) {
        this.setState({ startDate: event})
        // console.log(event)
    }

    endDateUpdated(event) {
        this.setState({ endDate: event})
        // console.log(event)
    }

    buttonClicked() {
        this.setState({ buttonClicked: true});
        axios.get('http://127.0.0.1:8000/get-stock-data', {
            params: {
                stock_symbol: this.state.stockSymbol,
                start_date: this.state.startDate,
                end_date: this.state.endDate
            }
        })
          .then(function (response) {
            // this.setState({ getResponse: response.data.sym,
            // isNewDataFetched: true })
            if (response.data === "No Data") {
                this.setState({ noData: true });
                return;
            }
            console.log(response.data)
            this.setState({ noData: false, 
                isNewDataFetched: true,
                low: response.data.low,
                high: response.data.high,
                median: response.data.median,
                quarter: response.data.quarter,
                three_quarters: response.data.three_quarters,
                data_list: response.data.data,
                frequencies: response.data.frequencies,
                all_data: response.data
            });
            // console.log(response.data);
          }.bind(this))
          .catch(function (error) {
            console.log(error);
          })
          .then(function () {
            // always executed
          });  
    }

    componentDidMount() {
        axios.get('http://127.0.0.1:8000/')
          .then(function (response) {
            this.setState({ testGetResult: response.data,
                isDataFetched: true })
            // console.log(response.data);
          }.bind(this))
          .catch(function (error) {
            console.log(error);
          })
          .then(function () {
            // always executed
          });  
    }

    renderStockInformation() {
        if (this.state.buttonClicked) {
            console.log("updated stock info");
            if (this.state.noData || this.state.stockSymbol == "") {
                return(
                    <h4>There is no data for this stock at these dates.</h4>
                );
            }
            return(
                <div>
                <h4>Price Change Over Time</h4>
                <LineChart width={600} height={230} data={this.state.data_list} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                    <Line type="monotone" dataKey="price" stroke="#8884d8" />
                    <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                    <XAxis dataKey="date" />
                    <YAxis />
                </LineChart>
                <div height={100}></div>
                <h4>Price Frequencies During Period</h4>
                <BarChart className="bar-chart"width={600} height={230} data={this.state.frequencies}>
                    <Bar dataKey="frequency" fill="#8884d8" />
                    <XAxis dataKey="price" />
                    <YAxis />
                </BarChart>
                <div className="price-breakdown-container">
                    <div><h4>Price Breakdown</h4></div>
                    <text className="price-breakdown">Min Price: ${this.state.low}</text>
                    <text className="price-breakdown">25th Percentile: ${this.state.quarter}</text>
                    <text className="price-breakdown">Median: ${this.state.median}</text>
                    <text className="price-breakdown">75th Percentile: ${this.state.three_quarters}</text>
                    <text className="price-breakdown">Max Price: ${this.state.high}</text>
                </div>
                </div>
            );
        }
    }
    
    render() {
        if(!this.state.isDataFetched) return null;
        return (
            <div>
                <h1>Stock Prices Over Time</h1>
                {/* <p>{ this.state.testGetResult }</p> */}
                <div className="form-field">
                    Stock Symbol:&nbsp;
                    <input type="text" 
                        value={this.state.stockSymbol} 
                        onChange={this.symbolUpdated} />
                </div>
                <div className="form-field">
                    Start Date:&nbsp;
                    <DatePicker
                        onChange={this.startDateUpdated}
                        value={this.state.startDate}
                    />
                </div>
                <div className="form-field">
                    End Date:&nbsp;
                    <DatePicker
                        onChange={this.endDateUpdated}
                        value={this.state.endDate}
                    />
                </div>
                <div className="show-button-container">
                    <button className="show-button" onClick={ this.buttonClicked }> Show Data </button>
                </div>
                
                {this.renderStockInformation()}
            </div>
        )
    }
}
