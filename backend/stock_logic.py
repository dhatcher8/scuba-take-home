from config import Marketstack_API_KEY
import requests
import numpy as np

class StockLogic():

    def __init__(self, db_connection, stock_symbol, start_date, end_date):
        self.db_connection = db_connection
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date

    def getDataReal(self):
        if self.db_connection.dataExists(self.stock_symbol, self.start_date, self.end_date):
            return True
            data = self.db_connection.getData(self.stock_symbol, self.start_date, self.end_date)
        elif self.db_connection.startDateExists(self.stock_symbol, self.start_date, self.end_date):
            last_date = self.db_connection.getLastExistingDate(self.stock_symbol, self.start_date, self.end_date)
            # next date = last date plus one day
            # the next line should use next_date instead of start_date
            data_to_add = self.getDataFromMarketstackAPI(self.stock_symbol, self.start_date, self.end_date)
            data_to_add = self.formatDataToAdd(data_to_add)
            self.db_connection.addData(data_to_add)
            data = self.db_connection.getData(self.stock_symbol, self.start_date, self.end_date)
        else:
            data_to_add = self.getDataFromMarketstackAPI(self.stock_symbol, self.start_date, self.end_date)
            data_to_add = self.formatDataToAdd(data_to_add)
            self.db_connection.addData(data_to_add)
            data = self.db_connection.getData(self.stock_symbol, self.start_date, self.end_date)
        return data

    def getDataFastTrack(self):
        # This method is terrible, but doing it for time sake
        # Just deleting all data from a stock symbol and putting it all there again
        self.db_connection.deleteData(self.stock_symbol)
        data_to_add = self.getDataFromMarketstackAPI(self.stock_symbol, self.start_date, self.end_date)
        if data_to_add == None or len(data_to_add) == 0:
            return "No Data"
        data_to_add = self.formatDataToAdd(data_to_add)
        print(data_to_add)
        self.db_connection.addData(data_to_add)
        data_to_return = self.db_connection.getData(self.stock_symbol, self.start_date, self.end_date)
        # quartiles = self.db_connection.getQuartiles(self.stock_symbol, self.start_date, self.end_date)
        return data_to_return

    def getDataFromMarketstackAPI(self, stock_symbol, start_date, end_date):
        params = {
            'access_key': Marketstack_API_KEY,
            'symbols': stock_symbol,
            'date_from': start_date,
            'date_to': end_date
        }
        api_result = requests.get('http://api.marketstack.com/v1/eod', params)
        api_response = api_result.json()
        try:
            data = api_response.get('data')
        except:
            return []
        return data

    def formatDataToAdd(self, data_to_add):
        # Create a list of tuples from json
        print(data_to_add)
        formatted_data = []
        for day_data in data_to_add:
            formatted_data.append((day_data.get('symbol'), day_data.get('date')[:10], day_data.get('close')))
        return formatted_data

    def getFrequencyData(self, prices):
        freq = {}
        for price in prices:
            rounded = round(price/10)*10
            if (rounded in freq):
                freq[rounded] += 1
            else:
                freq[rounded] = 1
        frequencies = []
        for key in freq:
            sub_dict = {}
            sub_dict['price'] = key
            sub_dict['frequency'] = freq[key]
            frequencies.append(sub_dict)
        frequencies.reverse()
        return frequencies

    def getResponse(self):
        # here we will return all the response values
        # This is where I would switch it back to the real get data function
        data = self.getDataFastTrack()
        if data == "No Data":
            return "No Data"
        prices = []
        for point in data:
            prices.append(float(point[3]))
        print(prices)
        frequencies = self.getFrequencyData(prices)
        low = round(np.percentile(prices, 0), 2)
        quarter = round(np.percentile(prices, 25), 2)
        median = round(np.percentile(prices, 50), 2)
        three_quarters = round(np.percentile(prices, 75), 2)
        high = round(np.percentile(prices, 100), 2)
        sub_data_new = []
        for point in data:
            sub_dict = {}
            sub_dict['id'] = point[0]
            sub_dict['symbol'] = point[1]
            sub_dict['date'] = point[2]
            sub_dict['price'] = point[3]
            sub_data_new.append(sub_dict)
        new_data = {}
        new_data['data'] = sub_data_new
        new_data['low'] = low
        new_data['quarter'] = quarter
        new_data['median'] = median
        new_data['three_quarters'] = three_quarters
        new_data['high'] = high
        new_data['frequencies'] = frequencies
        print(new_data)
        return new_data