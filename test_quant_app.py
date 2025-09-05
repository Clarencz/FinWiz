import unittest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
import json # Added this line

# Import modules to be tested
from data_manager import DataManager
from api_manager import APIManager
from db_manager import DBManager
from market_data import MarketData
from crypto_data import CryptoData
from forex_data import ForexData
from macro_data import MacroData
from charting import Charting
from analytics import Analytics
from portfolio_manager import PortfolioManager
from trading_simulator import TradingSimulator
from reporting import Reporting
from config_manager import ConfigManager
from security import SecurityManager

class TestQuantApp(unittest.TestCase):

    def setUp(self):
        # Initialize managers for testing
        self.data_manager = DataManager()
        self.api_manager = APIManager()
        self.db_manager = DBManager()
        self.market_data = MarketData()
        self.crypto_data = CryptoData()
        self.forex_data = ForexData()
        self.macro_data = MacroData()
        self.charting = Charting()
        self.analytics = Analytics()
        self.portfolio_manager = PortfolioManager()
        self.trading_simulator = TradingSimulator()
        self.reporting = Reporting()
        self.config_manager = ConfigManager()
        self.security_manager = SecurityManager()

        # Create dummy data for testing
        self.dummy_df = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [105, 106, 107, 108, 109],
            'Low': [99, 100, 101, 102, 103],
            'Close': [104, 105, 106, 107, 108],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']))
        self.dummy_df.index.name = 'Date'

        # Clean up any existing test files/databases
        if os.path.exists('test.db'):
            os.remove('test.db')
        if os.path.exists('test.csv'):
            os.remove('test.csv')
        if os.path.exists('test.xlsx'):
            os.remove('test.xlsx')
        if os.path.exists('test.json'):
            os.remove('test.json')
        if os.path.exists('test_report.pdf'):
            os.remove('test_report.pdf')
        if os.path.exists('encryption.key'):
            os.remove('encryption.key')

    def tearDown(self):
        # Clean up after tests
        if os.path.exists('test.db'):
            os.remove('test.db')
        if os.path.exists('test.csv'):
            os.remove('test.csv')
        if os.path.exists('test.xlsx'):
            os.remove('test.xlsx')
        if os.path.exists('test.json'):
            os.remove('test.json')
        if os.path.exists('test_report.pdf'):
            os.remove('test_report.pdf')
        if os.path.exists('encryption.key'):
            os.remove('encryption.key')

    # Test DataManager
    def test_load_csv(self):
        self.dummy_df.to_csv('test.csv', index=False)
        df = self.data_manager.load_csv('test.csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_load_excel(self):
        self.dummy_df.to_excel('test.xlsx', index=False)
        df = self.data_manager.load_excel('test.xlsx')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_load_json(self):
        with open('test.json', 'w') as f:
            json.dump({'data': 'test'}, f)
        data = self.data_manager.load_json('test.json')
        self.assertIsInstance(data, dict)
        self.assertEqual(data['data'], 'test')

    # Test APIManager (mock external calls)
    @patch('yfinance.download')
    def test_get_yfinance_historical_data(self, mock_yfinance_download):
        mock_yfinance_download.return_value = self.dummy_df
        df = self.api_manager.get_yfinance_historical_data('AAPL')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    # Test DBManager
    def test_save_and_load_dataframe(self):
        self.db_manager.db_name = 'test.db'
        self.db_manager.save_dataframe(self.dummy_df, 'test_table')
        loaded_df = self.db_manager.load_dataframe('test_table')
        self.assertIsInstance(loaded_df, pd.DataFrame)
        self.assertFalse(loaded_df.empty)
        pd.testing.assert_frame_equal(self.dummy_df.reset_index(drop=True), loaded_df.reset_index(drop=True))

    def test_list_tables(self):
        self.db_manager.db_name = 'test.db'
        self.db_manager.save_dataframe(self.dummy_df, 'another_table')
        tables = self.db_manager.list_tables()
        self.assertIn('another_table', tables)

    # Test MarketData (mock external calls)
    @patch('yfinance.Ticker')
    def test_get_quote_snapshot(self, mock_ticker):
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        mock_ticker_instance.info = {'regularMarketPrice': 150.0, 'regularMarketOpen': 149.0}
        self.market_data.get_quote_snapshot('AAPL')
        mock_ticker.assert_called_with('AAPL')

    # Test CryptoData (mock external calls)
    @patch('requests.get')
    def test_get_price_chart(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {'prices': [[1672531200000, 100], [1672617600000, 101]]}
        df = self.crypto_data.get_price_chart('bitcoin')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    # Test ForexData (mock external calls)
    @patch('requests.get')
    def test_get_live_rates(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {'rates': {'USD': 1.0, 'EUR': 0.9}}
        self.forex_data.get_live_rates('USD')
        mock_requests_get.assert_called_once()

    # Test MacroData (mock external calls)
    @patch('requests.get')
    def test_get_fred_series(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {'observations': [{'date': '2023-01-01', 'value': '100.0'}]}
        self.macro_data.get_fred_series('GDP', 'test_key')
        mock_requests_get.assert_called_once()

    # Test Charting (visual output, so check no errors and mock plotext)
    @patch('plotext.plot')
    @patch('plotext.show')
    def test_plot_line_chart(self, mock_plotext_show, mock_plotext_plot):
        self.charting.plot_line_chart(self.dummy_df['Close'])
        mock_plotext_plot.assert_called_once()
        mock_plotext_show.assert_called_once()

    # Test Analytics
    def test_calculate_technical_indicators(self):
        df_ta = self.analytics.calculate_technical_indicators(self.dummy_df.copy())
        self.assertIn('SMA_20', df_ta.columns)
        self.assertIn('RSI', df_ta.columns)

    # Test PortfolioManager
    def test_add_and_view_position(self):
        self.portfolio_manager.add_position('AAPL', 10, 150.0)
        self.assertIn('AAPL', self.portfolio_manager.portfolio['Symbol'].values)

    # Test TradingSimulator
    def test_buy_and_sell(self):
        self.trading_simulator.buy('MSFT', 5, 200.0)
        self.assertEqual(self.trading_simulator.balance, 100000 - (5 * 200.0))
        self.trading_simulator.sell('MSFT', 2, 210.0)
        self.assertEqual(self.trading_simulator.balance, 100000 - (5 * 200.0) + (2 * 210.0))

    # Test Reporting
    def test_export_csv(self):
        self.reporting.export_dataframe_to_csv(self.dummy_df, 'test_export.csv')
        self.assertTrue(os.path.exists('test_export.csv'))

    def test_generate_pdf_report(self):
        content = {"Test Section": "This is a test.", "DataFrame": self.dummy_df}
        self.reporting.generate_pdf_report("Test Report", content, "test_report.pdf")
        self.assertTrue(os.path.exists('test_report.pdf'))

    # Test ConfigManager
    def test_config_set_get_delete(self):
        self.config_manager.set('test_key', 'test_value')
        self.assertEqual(self.config_manager.get('test_key'), 'test_value')
        self.config_manager.delete('test_key')
        self.assertIsNone(self.config_manager.get('test_key'))

    def test_alias_set_get_delete(self):
        self.config_manager.set_alias('mycmd', 'stocks load AAPL')
        self.assertEqual(self.config_manager.get_alias('mycmd'), 'stocks load AAPL')
        self.config_manager.delete_alias('mycmd')
        self.assertIsNone(self.config_manager.get_alias('mycmd'))

    # Test SecurityManager
    def test_encrypt_decrypt_data(self):
        original_data = "sensitive_info_123"
        encrypted = self.security_manager.encrypt_data(original_data)
        decrypted = self.security_manager.decrypt_data(encrypted)
        self.assertEqual(original_data, decrypted)

    def test_encrypt_decrypt_file(self):
        with open('original.txt', 'w') as f:
            f.write("This is a secret message.")
        self.security_manager.encrypt_file('original.txt', 'encrypted.txt')
        self.assertTrue(os.path.exists('encrypted.txt'))
        self.security_manager.decrypt_file('encrypted.txt', 'decrypted.txt')
        self.assertTrue(os.path.exists('decrypted.txt'))
        with open('decrypted.txt', 'r') as f:
            content = f.read()
        self.assertEqual(content, "This is a secret message.")
        os.remove('original.txt')
        os.remove('encrypted.txt')
        os.remove('decrypted.txt')

if __name__ == '__main__':
    unittest.main()


