import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px

class ComplianceTracker:
    """Tracks regulatory compliance and audit requirements for $BRICS protocol"""
    
    def __init__(self):
        self.compliance_status = {}
        self.audit_trail = []
        self.regulatory_requirements = {}
        self.documentation_status = {}
        
    def initialize_compliance_requirements(self):
        """Initialize regulatory compliance requirements"""
        self.regulatory_requirements = {
            'basel_iii': {
                'name': 'Basel III Capital Requirements',
                'status': 'compliant',
                'last_review': datetime.now() - timedelta(days=30),
                'next_review': datetime.now() + timedelta(days=30),
                'requirements': [
                    'Capital adequacy ratio > 8%',
                    'Leverage ratio < 3%',
                    'Liquidity coverage ratio > 100%'
                ],
                'metrics': {
                    'capital_adequacy_ratio': 12.5,
                    'leverage_ratio': 2.1,
                    'liquidity_coverage_ratio': 125.0
                }
            },
            'kyc_aml': {
                'name': 'KYC/AML Requirements',
                'status': 'compliant',
                'last_review': datetime.now() - timedelta(days=15),
                'next_review': datetime.now() + timedelta(days=45),
                'requirements': [
                    'Customer identification and verification',
                    'Transaction monitoring',
                    'Suspicious activity reporting'
                ],
                'metrics': {
                    'kyc_completion_rate': 98.5,
                    'aml_alerts_resolved': 100.0,
                    'suspicious_reports_filed': 0
                }
            },
            'data_protection': {
                'name': 'Data Protection (POPIA)',
                'status': 'compliant',
                'last_review': datetime.now() - timedelta(days=7),
                'next_review': datetime.now() + timedelta(days=23),
                'requirements': [
                    'Data encryption at rest and in transit',
                    'Access controls and authentication',
                    'Data retention policies'
                ],
                'metrics': {
                    'data_encryption_rate': 100.0,
                    'access_control_score': 95.0,
                    'retention_policy_compliance': 100.0
                }
            },
            'financial_services': {
                'name': 'Financial Services Provider License',
                'status': 'compliant',
                'last_review': datetime.now() - timedelta(days=60),
                'next_review': datetime.now() + timedelta(days=300),
                'requirements': [
                    'FSP license maintenance',
                    'Regular reporting to FSCA',
                    'Professional indemnity insurance'
                ],
                'metrics': {
                    'fsp_license_valid': True,
                    'fsca_reporting_compliance': 100.0,
                    'insurance_coverage': 5000000
                }
            }
        }
    
    def add_audit_event(self, event_type: str, description: str, user: str, severity: str = 'info'):
        """Add audit trail event"""
        audit_event = {
            'timestamp': datetime.now(),
            'event_type': event_type,
            'description': description,
            'user': user,
            'severity': severity,
            'session_id': f"session_{int(datetime.now().timestamp())}"
        }
        self.audit_trail.append(audit_event)
    
    def get_compliance_status(self) -> Dict:
        """Get overall compliance status"""
        total_requirements = len(self.regulatory_requirements)
        compliant_requirements = sum(1 for req in self.regulatory_requirements.values() 
                                  if req['status'] == 'compliant')
        
        compliance_score = (compliant_requirements / total_requirements) * 100
        
        return {
            'overall_score': compliance_score,
            'total_requirements': total_requirements,
            'compliant_requirements': compliant_requirements,
            'non_compliant_requirements': total_requirements - compliant_requirements,
            'last_updated': datetime.now()
        }
    
    def update_compliance_metric(self, requirement_key: str, metric_key: str, value):
        """Update specific compliance metric"""
        if requirement_key in self.regulatory_requirements:
            if 'metrics' not in self.regulatory_requirements[requirement_key]:
                self.regulatory_requirements[requirement_key]['metrics'] = {}
            
            self.regulatory_requirements[requirement_key]['metrics'][metric_key] = value
            
            # Update status based on metrics
            self._update_requirement_status(requirement_key)
    
    def _update_requirement_status(self, requirement_key: str):
        """Update compliance status based on metrics"""
        req = self.regulatory_requirements[requirement_key]
        
        if requirement_key == 'basel_iii':
            # Check Basel III requirements
            metrics = req['metrics']
            if (metrics.get('capital_adequacy_ratio', 0) > 8 and
                metrics.get('leverage_ratio', 0) < 3 and
                metrics.get('liquidity_coverage_ratio', 0) > 100):
                req['status'] = 'compliant'
            else:
                req['status'] = 'non_compliant'
        
        elif requirement_key == 'kyc_aml':
            # Check KYC/AML requirements
            metrics = req['metrics']
            if (metrics.get('kyc_completion_rate', 0) > 95 and
                metrics.get('aml_alerts_resolved', 0) > 90):
                req['status'] = 'compliant'
            else:
                req['status'] = 'non_compliant'
        
        # Update last review date
        req['last_review'] = datetime.now()
    
    def generate_compliance_report(self) -> Dict:
        """Generate comprehensive compliance report"""
        compliance_status = self.get_compliance_status()
        
        report = {
            'report_date': datetime.now(),
            'compliance_summary': compliance_status,
            'regulatory_requirements': self.regulatory_requirements,
            'audit_trail_summary': {
                'total_events': len(self.audit_trail),
                'events_last_30_days': len([e for e in self.audit_trail 
                                          if (datetime.now() - e['timestamp']).days <= 30]),
                'critical_events': len([e for e in self.audit_trail if e['severity'] == 'critical'])
            },
            'upcoming_reviews': [
                {'requirement': req['name'], 'next_review': req['next_review']}
                for req in self.regulatory_requirements.values()
                if req['next_review'] > datetime.now()
            ]
        }
        
        return report

class DocumentationManager:
    """Manages documentation and reporting requirements"""
    
    def __init__(self):
        self.documents = {}
        self.reporting_schedule = {}
        
    def add_document(self, doc_type: str, title: str, content: str, version: str = "1.0"):
        """Add or update document"""
        doc_id = f"{doc_type}_{int(datetime.now().timestamp())}"
        
        self.documents[doc_id] = {
            'doc_type': doc_type,
            'title': title,
            'content': content,
            'version': version,
            'created_at': datetime.now(),
            'last_updated': datetime.now(),
            'status': 'active'
        }
    
    def get_documents_by_type(self, doc_type: str) -> List[Dict]:
        """Get all documents of a specific type"""
        return [doc for doc in self.documents.values() if doc['doc_type'] == doc_type]
    
    def generate_investor_report(self, company_df: pd.DataFrame, protocol_df: pd.DataFrame) -> Dict:
        """Generate investor due diligence report"""
        report = {
            'report_date': datetime.now(),
            'executive_summary': {
                'total_exposure': company_df['total_exposure'].sum(),
                'number_of_obligors': len(company_df),
                'average_yield': company_df['yield'].mean(),
                'protocol_apy': protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
            },
            'risk_assessment': {
                'portfolio_pd': company_df['avg_pd'].mean(),
                'industry_diversification': company_df['industry'].nunique(),
                'credit_rating_distribution': company_df['credit_rating'].value_counts().to_dict()
            },
            'regulatory_compliance': {
                'fsp_license': 'Active',
                'basel_compliance': 'Compliant',
                'kyc_aml_status': 'Compliant'
            },
            'investment_highlights': [
                'Sovereign guarantee protection',
                'Monthly yield distribution',
                'Real-time risk monitoring',
                'Regulatory compliance'
            ]
        }
        
        return report

class AuditTrailManager:
    """Manages audit trails and logging"""
    
    def __init__(self):
        self.audit_events = []
        self.user_sessions = {}
        
    def log_user_action(self, user_id: str, action: str, details: Dict, ip_address: str = None):
        """Log user action for audit purposes"""
        event = {
            'timestamp': datetime.now(),
            'user_id': user_id,
            'action': action,
            'details': details,
            'ip_address': ip_address,
            'session_id': self.user_sessions.get(user_id, 'unknown')
        }
        self.audit_events.append(event)
    
    def get_audit_summary(self, days: int = 30) -> Dict:
        """Get audit summary for specified period"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_events = [e for e in self.audit_events if e['timestamp'] > cutoff_date]
        
        return {
            'total_events': len(recent_events),
            'unique_users': len(set(e['user_id'] for e in recent_events)),
            'action_breakdown': pd.DataFrame(recent_events)['action'].value_counts().to_dict(),
            'events_by_date': pd.DataFrame(recent_events).groupby(
                pd.Grouper(key='timestamp', freq='D')).size().to_dict()
        }

# Initialize global instances
compliance_tracker = ComplianceTracker()
documentation_manager = DocumentationManager()
audit_trail_manager = AuditTrailManager()

# Initialize compliance requirements
compliance_tracker.initialize_compliance_requirements()

# Add some sample audit events
compliance_tracker.add_audit_event('login', 'User logged into dashboard', 'admin', 'info')
compliance_tracker.add_audit_event('data_access', 'Accessed portfolio data', 'analyst', 'info')
compliance_tracker.add_audit_event('report_generated', 'Generated compliance report', 'compliance_officer', 'info')

# Add sample documents
documentation_manager.add_document(
    'policy',
    'Data Protection Policy',
    'Comprehensive data protection policy compliant with POPIA requirements...',
    '2.1'
)

documentation_manager.add_document(
    'procedure',
    'KYC/AML Procedures',
    'Standard operating procedures for customer identification and anti-money laundering...',
    '1.5'
)

documentation_manager.add_document(
    'report',
    'Monthly Compliance Report',
    'Monthly compliance report covering all regulatory requirements...',
    '1.0'
) 