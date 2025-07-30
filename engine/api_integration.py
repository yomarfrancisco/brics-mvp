import requests
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

class BankAPIConnector:
    """Manages connections to bank data streams and processes real-time data"""
    
    def __init__(self):
        self.connections = {}
        self.data_cache = {}
        self.connection_status = {}
        self.last_update = {}
        
    def connect_bank(self, bank_name: str, api_endpoint: str, api_key: str, refresh_rate: int = 30) -> Dict:
        """Establish connection to a bank's API"""
        try:
            # Simulate API connection
            connection_id = f"{bank_name}_{int(time.time())}"
            
            self.connections[connection_id] = {
                'bank_name': bank_name,
                'endpoint': api_endpoint,
                'api_key': api_key,
                'refresh_rate': refresh_rate,
                'connected_at': datetime.now(),
                'status': 'connected'
            }
            
            self.connection_status[connection_id] = {
                'status': 'active',
                'last_heartbeat': datetime.now(),
                'data_freshness': 0,
                'success_rate': 99.7,
                'error_rate': 0.3,
                'total_requests': 0,
                'failed_requests': 0
            }
            
            return {
                'success': True,
                'connection_id': connection_id,
                'message': f'Successfully connected to {bank_name}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to connect to {bank_name}'
            }
    
    def disconnect_bank(self, connection_id: str) -> Dict:
        """Disconnect from a bank's API"""
        if connection_id in self.connections:
            self.connections[connection_id]['status'] = 'disconnected'
            self.connection_status[connection_id]['status'] = 'inactive'
            return {'success': True, 'message': 'Disconnected successfully'}
        return {'success': False, 'message': 'Connection not found'}
    
    def get_connection_status(self) -> Dict:
        """Get status of all bank connections"""
        status_summary = {}
        for conn_id, conn_data in self.connections.items():
            if conn_id in self.connection_status:
                status = self.connection_status[conn_id]
                status_summary[conn_data['bank_name']] = {
                    'status': status['status'],
                    'last_heartbeat': status['last_heartbeat'],
                    'data_freshness': status['data_freshness'],
                    'success_rate': status['success_rate'],
                    'error_rate': status['error_rate']
                }
        return status_summary
    
    def fetch_transaction_data(self, connection_id: str) -> Optional[Dict]:
        """Fetch transaction data from connected bank"""
        if connection_id not in self.connections:
            return None
            
        conn_data = self.connections[connection_id]
        
        # Simulate API call with realistic delays
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulate transaction data
        transactions = []
        num_transactions = random.randint(1, 5)
        
        for i in range(num_transactions):
            transaction = {
                'transaction_id': f"TXN_{conn_data['bank_name']}_{int(time.time())}_{i}",
                'obligor': f"OBL{random.randint(1, 15):03d}",
                'company': random.choice(['Nike', 'Ford', 'Samsung', 'Tata Motors', 'Petrobras']),
                'amount': random.uniform(50000, 300000),
                'currency': 'USD',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'On track',
                'risk_score': random.uniform(0.06, 0.12),
                'industry': random.choice(['Consumer Goods', 'Automotive', 'Technology', 'Energy']),
                'credit_type': 'Trade Receivables',
                'underwriting_bank': conn_data['bank_name'],
                'terms_tenor': random.choice(['90 days', '120 days', '150 days', '180 days']),
                'credit_rating': random.choice(['AAA', 'AA', 'A']),
                'time_listed': f"{random.randint(1, 3)}mo ago",
                'spread_bps': random.randint(30, 50)
            }
            transactions.append(transaction)
        
        # Update connection status
        self.connection_status[connection_id]['last_heartbeat'] = datetime.now()
        self.connection_status[connection_id]['data_freshness'] = random.uniform(0.5, 3.0)
        self.connection_status[connection_id]['total_requests'] += 1
        
        # Simulate occasional failures
        if random.random() < 0.02:  # 2% failure rate
            self.connection_status[connection_id]['failed_requests'] += 1
            self.connection_status[connection_id]['error_rate'] = (
                self.connection_status[connection_id]['failed_requests'] / 
                self.connection_status[connection_id]['total_requests'] * 100
            )
            return None
        
        return {
            'bank_name': conn_data['bank_name'],
            'transactions': transactions,
            'timestamp': datetime.now(),
            'data_quality': 'high'
        }
    
    def validate_data_quality(self, data: Dict) -> Dict:
        """Validate incoming data quality"""
        quality_score = 100
        issues = []
        
        if not data.get('transactions'):
            quality_score -= 20
            issues.append('No transactions found')
        
        for txn in data.get('transactions', []):
            if not txn.get('amount') or txn['amount'] <= 0:
                quality_score -= 10
                issues.append('Invalid transaction amount')
            
            if not txn.get('obligor'):
                quality_score -= 5
                issues.append('Missing obligor information')
        
        return {
            'quality_score': max(0, quality_score),
            'issues': issues,
            'status': 'high' if quality_score >= 90 else 'medium' if quality_score >= 70 else 'low'
        }
    
    def process_real_time_data(self) -> Dict:
        """Process all active connections and return aggregated data"""
        all_transactions = []
        connection_summary = {}
        
        for conn_id, conn_data in self.connections.items():
            if conn_data['status'] == 'connected':
                # Check if it's time to fetch new data
                last_update = self.last_update.get(conn_id, datetime.min)
                refresh_rate = conn_data['refresh_rate']
                
                if (datetime.now() - last_update).seconds >= refresh_rate:
                    data = self.fetch_transaction_data(conn_id)
                    if data:
                        # Validate data quality
                        quality = self.validate_data_quality(data)
                        data['quality'] = quality
                        
                        all_transactions.extend(data['transactions'])
                        connection_summary[conn_data['bank_name']] = {
                            'status': 'active',
                            'last_update': datetime.now(),
                            'transactions_count': len(data['transactions']),
                            'data_quality': quality['status']
                        }
                        
                        self.last_update[conn_id] = datetime.now()
                    else:
                        connection_summary[conn_data['bank_name']] = {
                            'status': 'error',
                            'last_update': self.last_update.get(conn_id, datetime.min),
                            'transactions_count': 0,
                            'data_quality': 'low'
                        }
        
        return {
            'transactions': all_transactions,
            'connection_summary': connection_summary,
            'total_transactions': len(all_transactions),
            'timestamp': datetime.now()
        }
    
    def get_available_banks(self) -> List[Dict]:
        """Get list of available banks for connection"""
        return [
            {'name': 'First National Bank', 'country': 'South Africa'},
            {'name': 'Standard Bank', 'country': 'South Africa'},
            {'name': 'Nedbank', 'country': 'South Africa'},
            {'name': 'ABSA Bank', 'country': 'South Africa'},
            {'name': 'Old Mutual', 'country': 'South Africa'},
            {'name': 'Banco de Moçambique', 'country': 'Mozambique'},
            {'name': 'Banco BCI', 'country': 'Mozambique'}
        ]

class DataQualityMonitor:
    """Monitors data quality and provides alerts"""
    
    def __init__(self):
        self.quality_thresholds = {
            'freshness_max_seconds': 300,  # 5 minutes
            'success_rate_min': 95.0,
            'error_rate_max': 5.0
        }
        self.alerts = []
    
    def check_connection_health(self, connection_status: Dict) -> List[Dict]:
        """Check health of all connections and generate alerts"""
        alerts = []
        
        for bank_name, status in connection_status.items():
            # Check data freshness
            if status.get('data_freshness', 0) > self.quality_thresholds['freshness_max_seconds']:
                alerts.append({
                    'type': 'warning',
                    'bank': bank_name,
                    'message': f'Data freshness is {status["data_freshness"]:.1f}s (threshold: {self.quality_thresholds["freshness_max_seconds"]}s)',
                    'timestamp': datetime.now()
                })
            
            # Check success rate
            if status.get('success_rate', 100) < self.quality_thresholds['success_rate_min']:
                alerts.append({
                    'type': 'error',
                    'bank': bank_name,
                    'message': f'Success rate is {status["success_rate"]:.1f}% (threshold: {self.quality_thresholds["success_rate_min"]}%)',
                    'timestamp': datetime.now()
                })
            
            # Check error rate
            if status.get('error_rate', 0) > self.quality_thresholds['error_rate_max']:
                alerts.append({
                    'type': 'error',
                    'bank': bank_name,
                    'message': f'Error rate is {status["error_rate"]:.1f}% (threshold: {self.quality_thresholds["error_rate_max"]}%)',
                    'timestamp': datetime.now()
                })
        
        return alerts

# Initialize global instances
bank_connector = BankAPIConnector()
quality_monitor = DataQualityMonitor()

# Pre-configure some banks
def initialize_default_connections():
    """Initialize default bank connections for demo"""
    banks = [
        {'name': 'First National Bank', 'endpoint': 'https://api.fnb.co.za/v1/transactions', 'key': 'fnb_demo_key'},
        {'name': 'Standard Bank', 'endpoint': 'https://api.standardbank.co.za/v1/data', 'key': 'sb_demo_key'},
        {'name': 'Nedbank', 'endpoint': 'https://api.nedbank.co.za/v1/streams', 'key': 'ned_demo_key'},
        {'name': 'ABSA Bank', 'endpoint': 'https://api.absa.co.za/v1/trade', 'key': 'absa_demo_key'},
        {'name': 'Old Mutual', 'endpoint': 'https://api.oldmutual.co.za/v1/cds', 'key': 'om_demo_key'}
    ]
    
    for bank in banks:
        bank_connector.connect_bank(
            bank_name=bank['name'],
            api_endpoint=bank['endpoint'],
            api_key=bank['key'],
            refresh_rate=30
        )

# Initialize default connections
initialize_default_connections() 