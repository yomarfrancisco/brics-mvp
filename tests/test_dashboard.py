import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))
from api_integration import BankAPIConnector, DataQualityMonitor
from advanced_analytics import AdvancedRiskAnalytics, PortfolioOptimizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docs'))
from compliance_tracker import ComplianceTracker, DocumentationManager, AuditTrailManager

class TestDataLoading(unittest.TestCase):
    """Test data loading and validation"""
    
    def setUp(self):
        """Set up test data"""
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
    def test_company_summary_loading(self):
        """Test company summary data loading"""
        try:
            company_df = pd.read_csv(os.path.join(self.data_path, 'mock_company_summary.csv'))
            
            # Check required columns
            required_columns = ['company', 'total_exposure', 'avg_pd', 'yield', 'status']
            for col in required_columns:
                self.assertIn(col, company_df.columns, f"Missing required column: {col}")
            
            # Check data types
            self.assertTrue(company_df['total_exposure'].dtype in ['int64', 'float64'])
            self.assertTrue(company_df['avg_pd'].dtype in ['int64', 'float64'])
            self.assertTrue(company_df['yield'].dtype in ['int64', 'float64'])
            
            # Check for reasonable values
            self.assertTrue(company_df['total_exposure'].min() > 0)
            self.assertTrue(company_df['avg_pd'].min() >= 0)
            self.assertTrue(company_df['avg_pd'].max() <= 1)
            self.assertTrue(company_df['yield'].min() >= 0)
            
            print("✅ Company summary data loading test passed")
            
        except Exception as e:
            self.fail(f"Company summary loading failed: {str(e)}")
    
    def test_protocol_metrics_loading(self):
        """Test protocol metrics data loading"""
        try:
            protocol_df = pd.read_csv(os.path.join(self.data_path, 'mock_protocol_metrics.csv'))
            
            # Check required columns
            required_columns = ['metric', 'value', 'component']
            for col in required_columns:
                self.assertIn(col, protocol_df.columns, f"Missing required column: {col}")
            
            # Check for key metrics
            key_metrics = ['brics_price', 'apy_per_brics', 'capital_efficiency']
            for metric in key_metrics:
                self.assertTrue(metric in protocol_df['metric'].values, f"Missing key metric: {metric}")
            
            print("✅ Protocol metrics data loading test passed")
            
        except Exception as e:
            self.fail(f"Protocol metrics loading failed: {str(e)}")
    
    def test_brics_price_loading(self):
        """Test $BRICS price data loading"""
        try:
            price_df = pd.read_csv(os.path.join(self.data_path, 'mock_brics_price.csv'))
            
            # Check required columns
            required_columns = ['timestamp', 'open', 'high', 'low', 'close']
            for col in required_columns:
                self.assertIn(col, price_df.columns, f"Missing required column: {col}")
            
            # Check data types
            price_df['timestamp'] = pd.to_datetime(price_df['timestamp'])
            self.assertTrue(price_df['timestamp'].dtype == 'datetime64[ns]')
            
            # Check for reasonable price values
            self.assertTrue(price_df['close'].min() > 0.9)
            self.assertTrue(price_df['close'].max() < 1.2)
            
            print("✅ $BRICS price data loading test passed")
            
        except Exception as e:
            self.fail(f"$BRICS price loading failed: {str(e)}")

class TestAPIIntegration(unittest.TestCase):
    """Test API integration functionality"""
    
    def setUp(self):
        """Set up API integration test"""
        self.bank_connector = BankAPIConnector()
        self.quality_monitor = DataQualityMonitor()
        
    def test_bank_connection(self):
        """Test bank connection functionality"""
        try:
            # Test connection
            connection_status = self.bank_connector.get_connection_status()
            self.assertIsInstance(connection_status, dict)
            self.assertIn('connected_banks', connection_status)
            
            # Test data fetching
            transaction_data = self.bank_connector.fetch_transaction_data()
            self.assertIsInstance(transaction_data, pd.DataFrame)
            
            print("✅ Bank connection test passed")
            
        except Exception as e:
            self.fail(f"Bank connection test failed: {str(e)}")
    
    def test_data_quality_monitoring(self):
        """Test data quality monitoring"""
        try:
            # Test health check
            health_status = self.quality_monitor.check_connection_health()
            self.assertIsInstance(health_status, dict)
            self.assertIn('overall_health', health_status)
            
            print("✅ Data quality monitoring test passed")
            
        except Exception as e:
            self.fail(f"Data quality monitoring test failed: {str(e)}")

class TestAdvancedAnalytics(unittest.TestCase):
    """Test advanced analytics functionality"""
    
    def setUp(self):
        """Set up analytics test"""
        self.risk_analytics = AdvancedRiskAnalytics()
        self.portfolio_optimizer = PortfolioOptimizer()
        
        # Create test data
        self.test_company_df = pd.DataFrame({
            'company': ['Test1', 'Test2', 'Test3'],
            'total_exposure': [1000000, 2000000, 1500000],
            'avg_pd': [0.05, 0.08, 0.06],
            'yield': [25.0, 30.0, 28.0],
            'industry': ['Tech', 'Manufacturing', 'Retail'],
            'credit_rating': ['AA', 'A', 'AA']
        })
    
    def test_correlation_calculation(self):
        """Test correlation calculation"""
        try:
            correlations = self.risk_analytics.calculate_correlations(self.test_company_df)
            self.assertIsInstance(correlations, pd.DataFrame)
            self.assertGreater(len(correlations), 0)
            
            print("✅ Correlation calculation test passed")
            
        except Exception as e:
            self.fail(f"Correlation calculation test failed: {str(e)}")
    
    def test_var_calculation(self):
        """Test VaR calculation"""
        try:
            var_result = self.risk_analytics.calculate_var(self.test_company_df)
            self.assertIsInstance(var_result, dict)
            self.assertIn('var_95', var_result)
            self.assertIn('var_99', var_result)
            
            print("✅ VaR calculation test passed")
            
        except Exception as e:
            self.fail(f"VaR calculation test failed: {str(e)}")
    
    def test_stress_testing(self):
        """Test stress testing scenarios"""
        try:
            stress_results = self.risk_analytics.stress_test_scenarios(self.test_company_df)
            self.assertIsInstance(stress_results, dict)
            self.assertIn('scenarios', stress_results)
            
            print("✅ Stress testing test passed")
            
        except Exception as e:
            self.fail(f"Stress testing test failed: {str(e)}")

class TestComplianceTracking(unittest.TestCase):
    """Test compliance tracking functionality"""
    
    def setUp(self):
        """Set up compliance test"""
        self.compliance_tracker = ComplianceTracker()
        self.documentation_manager = DocumentationManager()
        self.audit_trail_manager = AuditTrailManager()
        
    def test_compliance_status(self):
        """Test compliance status calculation"""
        try:
            # Initialize requirements
            self.compliance_tracker.initialize_compliance_requirements()
            
            # Get compliance status
            status = self.compliance_tracker.get_compliance_status()
            self.assertIsInstance(status, dict)
            self.assertIn('overall_score', status)
            self.assertIn('total_requirements', status)
            
            # Check score is reasonable
            self.assertGreaterEqual(status['overall_score'], 0)
            self.assertLessEqual(status['overall_score'], 100)
            
            print("✅ Compliance status test passed")
            
        except Exception as e:
            self.fail(f"Compliance status test failed: {str(e)}")
    
    def test_audit_trail(self):
        """Test audit trail functionality"""
        try:
            # Add audit event
            self.compliance_tracker.add_audit_event('test', 'Test event', 'test_user')
            
            # Check event was added
            self.assertGreater(len(self.compliance_tracker.audit_trail), 0)
            
            # Check event properties
            event = self.compliance_tracker.audit_trail[-1]
            self.assertEqual(event['event_type'], 'test')
            self.assertEqual(event['user'], 'test_user')
            
            print("✅ Audit trail test passed")
            
        except Exception as e:
            self.fail(f"Audit trail test failed: {str(e)}")
    
    def test_documentation_management(self):
        """Test documentation management"""
        try:
            # Add document
            self.documentation_manager.add_document('test', 'Test Document', 'Test content')
            
            # Get documents
            docs = self.documentation_manager.get_documents_by_type('test')
            self.assertGreater(len(docs), 0)
            
            # Check document properties
            doc = docs[0]
            self.assertEqual(doc['title'], 'Test Document')
            self.assertEqual(doc['content'], 'Test content')
            
            print("✅ Documentation management test passed")
            
        except Exception as e:
            self.fail(f"Documentation management test failed: {str(e)}")

class TestRealTimeSimulation(unittest.TestCase):
    """Test real-time data simulation"""
    
    def test_ultra_fast_simulation(self):
        """Test ultra-fast data simulation"""
        try:
            # Create test data
            test_df = pd.DataFrame({
                'metric': ['brics_price', 'apy_per_brics'],
                'value': [1.023, 34.4]
            })
            
            # Simulate ultra-fast update
            original_price = test_df[test_df['metric'] == 'brics_price']['value'].iloc[0]
            
            # Apply small random variation
            variation = np.random.uniform(-0.001, 0.001)
            test_df.loc[test_df['metric'] == 'brics_price', 'value'] += variation
            
            new_price = test_df[test_df['metric'] == 'brics_price']['value'].iloc[0]
            
            # Check variation is reasonable
            self.assertLess(abs(new_price - original_price), 0.01)
            
            print("✅ Ultra-fast simulation test passed")
            
        except Exception as e:
            self.fail(f"Ultra-fast simulation test failed: {str(e)}")

def run_all_tests():
    """Run all test suites"""
    print("🧪 Starting comprehensive test suite...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataLoading,
        TestAPIIntegration,
        TestAdvancedAnalytics,
        TestComplianceTracking,
        TestRealTimeSimulation
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("=" * 50)
    print(f"📊 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        for failure in result.failures:
            print(f"   - {failure[0]}: {failure[1]}")
        for error in result.errors:
            print(f"   - {error[0]}: {error[1]}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_all_tests() 