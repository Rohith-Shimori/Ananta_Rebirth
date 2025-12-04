"""
Real-Time System Monitoring and Optimization Engine
Advanced system performance monitoring with intelligent optimization
"""

import psutil
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import logging
import subprocess
import platform

logger = logging.getLogger("ananta.monitor")

class OptimizationLevel(Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    MAXIMUM = "maximum"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class SystemMetric:
    name: str
    value: float
    unit: str
    timestamp: datetime
    threshold: Optional[float] = None
    status: str = "normal"  # normal, warning, critical

@dataclass
class PerformanceAlert:
    metric_name: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    value: float
    threshold: float
    suggestions: List[str]

@dataclass
class OptimizationAction:
    action_type: str
    description: str
    impact: str  # low, medium, high
    risk_level: str  # low, medium, high
    automated: bool
    executed: bool = False
    timestamp: Optional[datetime] = None

class SystemMonitoringEngine:
    """Advanced real-time system monitoring with intelligent optimization"""
    
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.optimization_level = OptimizationLevel.BALANCED
        
        # Metrics storage
        self.current_metrics = {}
        self.historical_metrics = []
        self.performance_alerts = []
        self.optimization_actions = []
        
        # Thresholds and limits
        self.thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'disk_usage': 90.0,
            'gpu_usage': 85.0,
            'network_latency': 100.0,  # ms
            'process_count': 200,
            'temperature': 75.0  # Celsius
        }
        
        # Optimization rules
        self.optimization_rules = self._initialize_optimization_rules()
        
        # System information
        self.system_info = self._gather_system_info()
        
        # Callbacks for alerts
        self.alert_callbacks = []
        
        logger.info("🔧 System Monitoring Engine initialized")
    
    def _initialize_optimization_rules(self) -> Dict[str, List[Callable]]:
        """Initialize optimization rules for different scenarios"""
        return {
            'high_cpu': [
                self._optimize_cpu_usage,
                self._manage_processes,
                self._adjust_ai_model_settings
            ],
            'high_memory': [
                self._optimize_memory_usage,
                self._clear_caches,
                self._manage_services
            ],
            'high_disk': [
                self._cleanup_temp_files,
                self._compress_logs,
                self._archive_old_data
            ],
            'high_temperature': [
                self._reduce_system_load,
                self._adjust_fan_settings,
                self._throttle_processes
            ],
            'network_latency': [
                self._optimize_network_settings,
                self._manage_bandwidth,
                self._check_network_health
            ]
        }
    
    def _gather_system_info(self) -> Dict[str, Any]:
        """Gather comprehensive system information"""
        try:
            info = {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(logical=True),
                'cpu_physical': psutil.cpu_count(logical=False),
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total if platform.system() != 'Windows' else psutil.disk_usage('C:').total,
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            }
            
            # GPU information
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    info['gpu_info'] = {
                        'name': gpus[0].name,
                        'memory_total': gpus[0].memoryTotal * 1024 * 1024,  # Convert to bytes
                        'driver_version': gpus[0].driver
                    }
            except ImportError:
                info['gpu_info'] = None
            
            return info
        except Exception as e:
            logger.error(f"Error gathering system info: {e}")
            return {}
    
    def start_monitoring(self, interval: int = 5):
        """Start real-time system monitoring"""
        if self.is_monitoring:
            logger.warning("Monitoring already started")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info(f"📊 System monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("⏹️ System monitoring stopped")
    
    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect all metrics
                metrics = self._collect_all_metrics()
                
                # Update current metrics
                self.current_metrics = metrics
                
                # Store in historical data
                self._store_historical_metrics(metrics)
                
                # Check for alerts
                self._check_thresholds(metrics)
                
                # Apply optimizations if needed
                if self.optimization_level != OptimizationLevel.CONSERVATIVE:
                    self._apply_optimizations(metrics)
                
                # Sleep until next iteration
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def _collect_all_metrics(self) -> Dict[str, SystemMetric]:
        """Collect all system metrics"""
        metrics = {}
        current_time = datetime.now()
        
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics['cpu_usage'] = SystemMetric(
                'cpu_usage', cpu_percent, '%', current_time, self.thresholds['cpu_usage']
            )
            
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                metrics['cpu_frequency'] = SystemMetric(
                    'cpu_frequency', cpu_freq.current, 'MHz', current_time
                )
            
            # Memory metrics
            memory = psutil.virtual_memory()
            metrics['memory_usage'] = SystemMetric(
                'memory_usage', memory.percent, '%', current_time, self.thresholds['memory_usage']
            )
            metrics['memory_available'] = SystemMetric(
                'memory_available', memory.available, 'bytes', current_time
            )
            metrics['memory_used'] = SystemMetric(
                'memory_used', memory.used, 'bytes', current_time
            )
            
            # Disk metrics
            disk_path = '/' if platform.system() != 'Windows' else 'C:'
            disk = psutil.disk_usage(disk_path)
            disk_percent = (disk.used / disk.total) * 100
            metrics['disk_usage'] = SystemMetric(
                'disk_usage', disk_percent, '%', current_time, self.thresholds['disk_usage']
            )
            metrics['disk_free'] = SystemMetric(
                'disk_free', disk.free, 'bytes', current_time
            )
            
            # Network metrics
            network = psutil.net_io_counters()
            metrics['network_bytes_sent'] = SystemMetric(
                'network_bytes_sent', network.bytes_sent, 'bytes', current_time
            )
            metrics['network_bytes_recv'] = SystemMetric(
                'network_bytes_recv', network.bytes_recv, 'bytes', current_time
            )
            
            # Process metrics
            process_count = len(psutil.pids())
            metrics['process_count'] = SystemMetric(
                'process_count', process_count, 'count', current_time, self.thresholds['process_count']
            )
            
            # GPU metrics (if available)
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    metrics['gpu_usage'] = SystemMetric(
                        'gpu_usage', gpu.load * 100, '%', current_time, self.thresholds['gpu_usage']
                    )
                    metrics['gpu_temperature'] = SystemMetric(
                        'gpu_temperature', gpu.temperature, '°C', current_time, self.thresholds['temperature']
                    )
                    metrics['gpu_memory_used'] = SystemMetric(
                        'gpu_memory_used', gpu.memoryUsed * 1024 * 1024, 'bytes', current_time
                    )
            except ImportError:
                pass
            
            # System load average (Unix-like systems)
            if hasattr(psutil, 'getloadavg'):
                load_avg = psutil.getloadavg()
                metrics['load_average_1m'] = SystemMetric(
                    'load_average_1m', load_avg[0], 'load', current_time
                )
                metrics['load_average_5m'] = SystemMetric(
                    'load_average_5m', load_avg[1], 'load', current_time
                )
                metrics['load_average_15m'] = SystemMetric(
                    'load_average_15m', load_avg[2], 'load', current_time
                )
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = current_time - boot_time
            metrics['system_uptime'] = SystemMetric(
                'system_uptime', uptime.total_seconds(), 'seconds', current_time
            )
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
        
        return metrics
    
    def _store_historical_metrics(self, metrics: Dict[str, SystemMetric]):
        """Store metrics in historical data"""
        self.historical_metrics.append({
            'timestamp': datetime.now().isoformat(),
            'metrics': {name: {
                'value': metric.value,
                'unit': metric.unit,
                'status': metric.status
            } for name, metric in metrics.items()}
        })
        
        # Keep only last 1000 entries
        if len(self.historical_metrics) > 1000:
            self.historical_metrics = self.historical_metrics[-1000:]
    
    def _check_thresholds(self, metrics: Dict[str, SystemMetric]):
        """Check metrics against thresholds and generate alerts"""
        for name, metric in metrics.items():
            if metric.threshold is None:
                continue
            
            # Determine status
            if metric.value >= metric.threshold * 1.2:  # 20% above threshold
                metric.status = "critical"
                severity = AlertSeverity.CRITICAL
            elif metric.value >= metric.threshold:
                metric.status = "warning"
                severity = AlertSeverity.WARNING
            else:
                metric.status = "normal"
                severity = AlertSeverity.INFO
            
            # Generate alert if needed
            if metric.status in ["warning", "critical"]:
                alert = PerformanceAlert(
                    metric_name=name,
                    severity=severity,
                    message=f"{name.replace('_', ' ').title()} is {metric.value:.1f}{metric.unit} (threshold: {metric.threshold}{metric.unit})",
                    timestamp=datetime.now(),
                    value=metric.value,
                    threshold=metric.threshold,
                    suggestions=self._generate_alert_suggestions(name, metric.value, metric.threshold)
                )
                
                self.performance_alerts.append(alert)
                
                # Trigger callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert)
                    except Exception as e:
                        logger.error(f"Error in alert callback: {e}")
        
        # Keep only recent alerts
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.performance_alerts = [
            alert for alert in self.performance_alerts
            if alert.timestamp > cutoff_time
        ]
    
    def _generate_alert_suggestions(self, metric_name: str, value: float, threshold: float) -> List[str]:
        """Generate suggestions for performance alerts"""
        suggestions = []
        
        if metric_name == 'cpu_usage':
            suggestions.extend([
                "Close unnecessary applications",
                "Check for background processes",
                "Consider upgrading CPU if consistently high",
                "Optimize AI model complexity"
            ])
        elif metric_name == 'memory_usage':
            suggestions.extend([
                "Clear system cache and temporary files",
                "Close memory-intensive applications",
                "Consider adding more RAM",
                "Optimize memory usage in applications"
            ])
        elif metric_name == 'disk_usage':
            suggestions.extend([
                "Clean up temporary files and downloads",
                "Archive or delete old files",
                "Run disk cleanup utilities",
                "Consider disk space expansion"
            ])
        elif metric_name == 'gpu_usage':
            suggestions.extend([
                "Reduce graphics quality settings",
                "Close GPU-intensive applications",
                "Update GPU drivers",
                "Consider GPU upgrade"
            ])
        elif metric_name == 'gpu_temperature':
            suggestions.extend([
                "Improve system cooling",
                "Clean dust from fans and heatsinks",
                "Reduce system load",
                "Check for proper ventilation"
            ])
        
        return suggestions
    
    def _apply_optimizations(self, metrics: Dict[str, SystemMetric]):
        """Apply automatic optimizations based on metrics"""
        for name, metric in metrics.items():
            if metric.status in ["warning", "critical"]:
                # Find appropriate optimization rules
                if name == 'cpu_usage' and metric.value > self.thresholds['cpu_usage']:
                    self._execute_optimization_rules('high_cpu', metrics)
                elif name == 'memory_usage' and metric.value > self.thresholds['memory_usage']:
                    self._execute_optimization_rules('high_memory', metrics)
                elif name == 'disk_usage' and metric.value > self.thresholds['disk_usage']:
                    self._execute_optimization_rules('high_disk', metrics)
                elif 'temperature' in name and metric.value > self.thresholds['temperature']:
                    self._execute_optimization_rules('high_temperature', metrics)
    
    def _execute_optimization_rules(self, category: str, metrics: Dict[str, SystemMetric]):
        """Execute optimization rules for a specific category"""
        if category not in self.optimization_rules:
            return
        
        for rule in self.optimization_rules[category]:
            try:
                if self.optimization_level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.MAXIMUM]:
                    # Execute aggressive optimizations
                    rule(metrics, aggressive=True)
                elif self.optimization_level == OptimizationLevel.BALANCED:
                    # Execute balanced optimizations
                    rule(metrics, aggressive=False)
            except Exception as e:
                logger.error(f"Error executing optimization rule {rule.__name__}: {e}")
    
    def _optimize_cpu_usage(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Optimize CPU usage"""
        # Find high CPU processes
        high_cpu_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 50:
                    high_cpu_processes.append(proc.info)
            except:
                continue
        
        if high_cpu_processes:
            action = OptimizationAction(
                action_type='cpu_optimization',
                description=f"Found {len(high_cpu_processes)} high CPU processes",
                impact='medium',
                risk_level='low',
                automated=True,
                timestamp=datetime.now()
            )
            
            if aggressive:
                # In aggressive mode, suggest terminating non-essential processes
                non_essential = [p for p in high_cpu_processes if not self._is_essential_process(p['name'])]
                action.description += f" ({len(non_essential)} potentially non-essential)"
            
            self.optimization_actions.append(action)
    
    def _optimize_memory_usage(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Optimize memory usage"""
        memory = psutil.virtual_memory()
        
        action = OptimizationAction(
            action_type='memory_optimization',
            description=f"Memory usage at {memory.percent:.1f}%",
            impact='medium',
            risk_level='low',
            automated=True,
            timestamp=datetime.now()
        )
        
        if aggressive:
            # Clear Python garbage collector
            import gc
            collected = gc.collect()
            action.description += f" (GC collected {collected} objects)"
        
        self.optimization_actions.append(action)
    
    def _cleanup_temp_files(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Clean up temporary files"""
        import tempfile
        import os
        
        temp_dir = tempfile.gettempdir()
        cleaned_size = 0
        
        try:
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path):
                        file_age = time.time() - os.path.getctime(item_path)
                        # Only delete files older than 1 hour
                        if file_age > 3600:
                            file_size = os.path.getsize(item_path)
                            os.remove(item_path)
                            cleaned_size += file_size
                except:
                    continue
        except Exception as e:
            logger.error(f"Error cleaning temp files: {e}")
        
        action = OptimizationAction(
            action_type='temp_cleanup',
            description=f"Cleaned {self._format_bytes(cleaned_size)} of temporary files",
            impact='low',
            risk_level='low',
            automated=True,
            timestamp=datetime.now()
        )
        
        self.optimization_actions.append(action)
    
    def _manage_processes(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Manage system processes"""
        # This is a placeholder for process management
        # In a real implementation, you might want to:
        # - Identify resource-intensive processes
        # - Suggest or automatically terminate non-essential processes
        # - Adjust process priorities
        pass
    
    def _clear_caches(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Clear system caches"""
        # Placeholder for cache clearing
        # Implementation would depend on the specific cache systems in use
        pass
    
    def _manage_services(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Manage system services"""
        # Placeholder for service management
        pass
    
    def _compress_logs(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Compress old log files"""
        # Placeholder for log compression
        pass
    
    def _archive_old_data(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Archive old data"""
        # Placeholder for data archiving
        pass
    
    def _reduce_system_load(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Reduce overall system load"""
        # Placeholder for system load reduction
        pass
    
    def _adjust_fan_settings(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Adjust fan settings for cooling"""
        # Placeholder for fan control (would need platform-specific implementation)
        pass
    
    def _throttle_processes(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Throttle intensive processes"""
        # Placeholder for process throttling
        pass
    
    def _optimize_network_settings(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Optimize network settings"""
        # Placeholder for network optimization
        pass
    
    def _manage_bandwidth(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Manage network bandwidth"""
        # Placeholder for bandwidth management
        pass
    
    def _check_network_health(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Check network health"""
        # Placeholder for network health checks
        pass
    
    def _adjust_ai_model_settings(self, metrics: Dict[str, SystemMetric], aggressive: bool = False):
        """Adjust AI model settings based on system resources"""
        # This would interface with the AI model to adjust:
        # - Model complexity
        # - Batch sizes
        # - Context window sizes
        # - Frequency of self-improvement
        pass
    
    def _is_essential_process(self, process_name: str) -> bool:
        """Check if a process is essential for system operation"""
        essential_processes = {
            'system', 'kernel', 'winlogon', 'csrss', 'smss',
            'services', 'lsass', 'svchost', 'explorer',
            'dwm', 'audiodg', 'spoolsv', 'taskmgr'
        }
        
        process_lower = process_name.lower()
        return any(essential in process_lower for essential in essential_processes)
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        if not self.current_metrics:
            return {'status': 'No data available'}
        
        # Calculate overall health score
        total_metrics = len(self.current_metrics)
        critical_count = sum(1 for m in self.current_metrics.values() if m.status == 'critical')
        warning_count = sum(1 for m in self.current_metrics.values() if m.status == 'warning')
        
        health_score = 100 - ((critical_count * 25) + (warning_count * 10))
        health_score = max(0, health_score)
        
        # Determine overall status
        if critical_count > 0:
            overall_status = 'critical'
        elif warning_count > 0:
            overall_status = 'warning'
        else:
            overall_status = 'healthy'
        
        return {
            'overall_status': overall_status,
            'health_score': health_score,
            'metrics': {
                name: {
                    'value': metric.value,
                    'unit': metric.unit,
                    'status': metric.status,
                    'threshold': metric.threshold
                } for name, metric in self.current_metrics.items()
            },
            'system_info': self.system_info,
            'recent_alerts': [
                {
                    'metric': alert.metric_name,
                    'severity': alert.severity.value,
                    'message': alert.message,
                    'timestamp': alert.timestamp.isoformat(),
                    'suggestions': alert.suggestions
                } for alert in self.performance_alerts[-10:]  # Last 10 alerts
            ],
            'optimization_actions': len(self.optimization_actions),
            'monitoring_active': self.is_monitoring,
            'optimization_level': self.optimization_level.value
        }
    
    def get_performance_history(self, metric_name: str, hours: int = 24) -> List[Dict]:
        """Get performance history for a specific metric"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        history = []
        for entry in self.historical_metrics:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            if entry_time > cutoff_time and metric_name in entry['metrics']:
                history.append({
                    'timestamp': entry['timestamp'],
                    'value': entry['metrics'][metric_name]['value'],
                    'status': entry['metrics'][metric_name]['status']
                })
        
        return history
    
    def set_optimization_level(self, level: OptimizationLevel):
        """Set optimization level"""
        self.optimization_level = level
        logger.info(f"Optimization level set to: {level.value}")
    
    def add_alert_callback(self, callback: Callable[[PerformanceAlert], None]):
        """Add callback for performance alerts"""
        self.alert_callbacks.append(callback)
    
    def run_optimization(self, category: str = 'all') -> Dict[str, Any]:
        """Manually run optimization for specific category or all"""
        if not self.current_metrics:
            return {'error': 'No metrics available'}
        
        executed_actions = []
        
        if category == 'all':
            categories = self.optimization_rules.keys()
        else:
            categories = [category] if category in self.optimization_rules else []
        
        for cat in categories:
            self._execute_optimization_rules(cat, self.current_metrics)
            executed_actions.append(cat)
        
        return {
            'executed_categories': executed_actions,
            'total_actions': len(self.optimization_actions),
            'optimization_level': self.optimization_level.value
        }
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get optimization recommendations based on current metrics"""
        recommendations = []
        
        if not self.current_metrics:
            return recommendations
        
        for name, metric in self.current_metrics.items():
            if metric.status in ['warning', 'critical']:
                recommendations.append({
                    'metric': name,
                    'current_value': metric.value,
                    'threshold': metric.threshold,
                    'status': metric.status,
                    'recommendations': self._generate_alert_suggestions(name, metric.value, metric.threshold),
                    'priority': 'high' if metric.status == 'critical' else 'medium'
                })
        
        return recommendations
