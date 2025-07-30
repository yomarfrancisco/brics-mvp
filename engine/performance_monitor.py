import time
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available. Performance monitoring will be limited.")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import logging
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitors system performance and dashboard metrics"""
    
    def __init__(self):
        self.performance_metrics = []
        self.start_time = datetime.now()
        self.monitoring_active = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start performance monitoring in background thread"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                metrics = self._collect_metrics()
                self.performance_metrics.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.performance_metrics) > 1000:
                    self.performance_metrics = self.performance_metrics[-1000:]
                
                time.sleep(5)  # Collect metrics every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)
    
    def _collect_metrics(self) -> Dict:
        """Collect current system metrics"""
        try:
            if not PSUTIL_AVAILABLE:
                # Return basic metrics without psutil
                return {
                    'timestamp': datetime.now(),
                    'cpu_percent': 0,
                    'memory_percent': 0,
                    'memory_available_gb': 0,
                    'disk_percent': 0,
                    'disk_free_gb': 0,
                    'process_memory_mb': 0,
                    'process_cpu_percent': 0,
                    'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
                    'psutil_available': False
                }
            
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            process_cpu = process.cpu_percent()
            
            return {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / 1024 / 1024 / 1024,
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / 1024 / 1024 / 1024,
                'process_memory_mb': process_memory,
                'process_cpu_percent': process_cpu,
                'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
                'psutil_available': True
            }
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {
                'timestamp': datetime.now(),
                'error': str(e)
            }
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.performance_metrics:
            return {'error': 'No metrics available'}
        
        try:
            # Ensure all metrics have consistent structure
            cleaned_metrics = []
            for metric in self.performance_metrics:
                # Create a standardized metric structure
                cleaned_metric = {
                    'timestamp': metric.get('timestamp', datetime.now()),
                    'cpu_percent': metric.get('cpu_percent', 0),
                    'memory_percent': metric.get('memory_percent', 0),
                    'memory_available_gb': metric.get('memory_available_gb', 0),
                    'disk_percent': metric.get('disk_percent', 0),
                    'disk_free_gb': metric.get('disk_free_gb', 0),
                    'process_memory_mb': metric.get('process_memory_mb', 0),
                    'process_cpu_percent': metric.get('process_cpu_percent', 0),
                    'uptime_seconds': metric.get('uptime_seconds', 0),
                    'psutil_available': metric.get('psutil_available', False)
                }
                cleaned_metrics.append(cleaned_metric)
            
            df = pd.DataFrame(cleaned_metrics)
            
            # Calculate summary statistics
            summary = {
                'current_metrics': df.iloc[-1].to_dict() if len(df) > 0 else {},
                'average_metrics': {
                    'cpu_percent': df['cpu_percent'].mean() if 'cpu_percent' in df.columns else 0,
                    'memory_percent': df['memory_percent'].mean() if 'memory_percent' in df.columns else 0,
                    'process_memory_mb': df['process_memory_mb'].mean() if 'process_memory_mb' in df.columns else 0,
                    'process_cpu_percent': df['process_cpu_percent'].mean() if 'process_cpu_percent' in df.columns else 0
                },
                'peak_metrics': {
                    'max_cpu_percent': df['cpu_percent'].max() if 'cpu_percent' in df.columns else 0,
                    'max_memory_percent': df['memory_percent'].max() if 'memory_percent' in df.columns else 0,
                    'max_process_memory_mb': df['process_memory_mb'].max() if 'process_memory_mb' in df.columns else 0
                },
                'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
                'total_metrics_collected': len(self.performance_metrics)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating performance summary: {e}")
            return {
                'error': f'Error creating summary: {str(e)}',
                'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
                'total_metrics_collected': len(self.performance_metrics)
            }
    
    def get_performance_alerts(self) -> List[Dict]:
        """Get performance alerts based on thresholds"""
        alerts = []
        
        if not self.performance_metrics:
            return alerts
        
        current_metrics = self.performance_metrics[-1]
        
        # Skip alerts if psutil is not available
        if not current_metrics.get('psutil_available', True):
            return alerts
        
        # CPU alerts
        if current_metrics.get('cpu_percent', 0) > 80:
            alerts.append({
                'type': 'warning',
                'metric': 'CPU Usage',
                'value': f"{current_metrics['cpu_percent']:.1f}%",
                'threshold': '80%',
                'message': 'High CPU usage detected'
            })
        
        # Memory alerts
        if current_metrics.get('memory_percent', 0) > 85:
            alerts.append({
                'type': 'critical',
                'metric': 'Memory Usage',
                'value': f"{current_metrics['memory_percent']:.1f}%",
                'threshold': '85%',
                'message': 'Critical memory usage detected'
            })
        
        # Disk alerts
        if current_metrics.get('disk_percent', 0) > 90:
            alerts.append({
                'type': 'warning',
                'metric': 'Disk Usage',
                'value': f"{current_metrics['disk_percent']:.1f}%",
                'threshold': '90%',
                'message': 'High disk usage detected'
            })
        
        # Process memory alerts
        if current_metrics.get('process_memory_mb', 0) > 1000:  # 1GB
            alerts.append({
                'type': 'warning',
                'metric': 'Process Memory',
                'value': f"{current_metrics['process_memory_mb']:.1f} MB",
                'threshold': '1000 MB',
                'message': 'High process memory usage'
            })
        
        return alerts

class DataProcessingMonitor:
    """Monitors data processing performance"""
    
    def __init__(self):
        self.processing_times = []
        self.data_sizes = []
        self.error_counts = {}
        
    def log_processing_time(self, operation: str, processing_time: float, data_size: int = 0):
        """Log data processing time"""
        self.processing_times.append({
            'timestamp': datetime.now(),
            'operation': operation,
            'processing_time': processing_time,
            'data_size': data_size
        })
        
        # Keep only last 1000 entries
        if len(self.processing_times) > 1000:
            self.processing_times = self.processing_times[-1000:]
    
    def log_error(self, operation: str, error_type: str):
        """Log processing errors"""
        if operation not in self.error_counts:
            self.error_counts[operation] = {}
        
        if error_type not in self.error_counts[operation]:
            self.error_counts[operation][error_type] = 0
        
        self.error_counts[operation][error_type] += 1
    
    def get_processing_summary(self) -> Dict:
        """Get data processing performance summary"""
        if not self.processing_times:
            return {'error': 'No processing data available'}
        
        df = pd.DataFrame(self.processing_times)
        
        summary = {
            'total_operations': len(df),
            'average_processing_time': df['processing_time'].mean(),
            'max_processing_time': df['processing_time'].max(),
            'min_processing_time': df['processing_time'].min(),
            'operations_by_type': df['operation'].value_counts().to_dict(),
            'recent_performance': df.tail(10)['processing_time'].mean(),
            'error_summary': self.error_counts
        }
        
        return summary
    
    def get_slow_operations(self, threshold_seconds: float = 1.0) -> List[Dict]:
        """Get operations that took longer than threshold"""
        if not self.processing_times:
            return []
        
        df = pd.DataFrame(self.processing_times)
        slow_ops = df[df['processing_time'] > threshold_seconds]
        
        return slow_ops.to_dict('records')

class DashboardPerformanceTracker:
    """Tracks dashboard-specific performance metrics"""
    
    def __init__(self):
        self.page_load_times = []
        self.chart_render_times = []
        self.data_refresh_times = []
        self.user_interactions = []
        
    def log_page_load(self, page_name: str, load_time: float):
        """Log page load time"""
        self.page_load_times.append({
            'timestamp': datetime.now(),
            'page': page_name,
            'load_time': load_time
        })
    
    def log_chart_render(self, chart_name: str, render_time: float):
        """Log chart render time"""
        self.chart_render_times.append({
            'timestamp': datetime.now(),
            'chart': chart_name,
            'render_time': render_time
        })
    
    def log_data_refresh(self, data_type: str, refresh_time: float):
        """Log data refresh time"""
        self.data_refresh_times.append({
            'timestamp': datetime.now(),
            'data_type': data_type,
            'refresh_time': refresh_time
        })
    
    def log_user_interaction(self, interaction_type: str, duration: float = 0):
        """Log user interactions"""
        self.user_interactions.append({
            'timestamp': datetime.now(),
            'interaction': interaction_type,
            'duration': duration
        })
    
    def get_dashboard_summary(self) -> Dict:
        """Get dashboard performance summary"""
        summary = {
            'page_loads': len(self.page_load_times),
            'chart_renders': len(self.chart_render_times),
            'data_refreshes': len(self.data_refresh_times),
            'user_interactions': len(self.user_interactions)
        }
        
        if self.page_load_times:
            df_pages = pd.DataFrame(self.page_load_times)
            summary['avg_page_load_time'] = df_pages['load_time'].mean()
            summary['slowest_page'] = df_pages.loc[df_pages['load_time'].idxmax(), 'page']
        
        if self.chart_render_times:
            df_charts = pd.DataFrame(self.chart_render_times)
            summary['avg_chart_render_time'] = df_charts['render_time'].mean()
            summary['slowest_chart'] = df_charts.loc[df_charts['render_time'].idxmax(), 'chart']
        
        if self.data_refresh_times:
            df_refresh = pd.DataFrame(self.data_refresh_times)
            summary['avg_refresh_time'] = df_refresh['refresh_time'].mean()
        
        return summary

# Initialize global instances
performance_monitor = PerformanceMonitor()
data_processing_monitor = DataProcessingMonitor()
dashboard_tracker = DashboardPerformanceTracker()

# Start monitoring
performance_monitor.start_monitoring() 