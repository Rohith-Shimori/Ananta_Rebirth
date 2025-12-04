"""
Advanced Security and Privacy Engine
Enterprise-grade security with intelligent threat detection
"""

import hashlib
import secrets
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger("ananta.security")

class SecurityLevel(Enum):
    MINIMAL = "minimal"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"

class ThreatType(Enum):
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_BREACH = "data_breach"
    MALICIOUS_INPUT = "malicious_input"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    BRUTE_FORCE = "brute_force"
    INJECTION = "injection"

@dataclass
class SecurityEvent:
    event_type: ThreatType
    severity: str  # low, medium, high, critical
    description: str
    timestamp: datetime
    source_ip: Optional[str]
    user_agent: Optional[str]
    blocked: bool

@dataclass
class SecurityPolicy:
    level: SecurityLevel
    encryption_enabled: bool
    session_timeout: int  # minutes
    max_login_attempts: int
    require_biometric: bool
    audit_logging: bool
    data_retention_days: int

class AdvancedSecurityEngine:
    """Enterprise-grade security with intelligent threat detection"""
    
    def __init__(self):
        self.current_policy = SecurityPolicy(
            level=SecurityLevel.HIGH,
            encryption_enabled=True,
            session_timeout=30,
            max_login_attempts=5,
            require_biometric=False,
            audit_logging=True,
            data_retention_days=90
        )
        
        self.security_events = []
        self.active_sessions = {}
        self.blocked_ips = set()
        self.suspicious_patterns = {}
        self.encryption_keys = {}
        self.threat_intelligence = {}
        
        # Initialize security components
        self._initialize_encryption()
        self._load_threat_patterns()
        self._initialize_audit_log()
    
    def _initialize_encryption(self):
        """Initialize encryption keys and algorithms"""
        try:
            # Generate master key
            self.master_key = secrets.token_bytes(32)
            
            # Generate session keys
            self.session_keys = {}
            
            logger.info("✅ Encryption system initialized")
        except Exception as e:
            logger.error(f"Encryption initialization failed: {e}")
            self.master_key = None
    
    def _load_threat_patterns(self):
        """Load known threat patterns and signatures"""
        self.threat_patterns = {
            'sql_injection': [
                'union select', 'drop table', 'insert into', 'delete from',
                'exec(', 'script>', 'javascript:', 'vbscript:'
            ],
            'xss': [
                '<script', 'onload=', 'onerror=', 'onclick=', 'javascript:',
                'alert(', 'document.cookie', 'window.location'
            ],
            'command_injection': [
                ';cat ', ';ls ', ';dir ', '|whoami', '&&', '||',
                '`', '$(', 'nc -l', 'python -c'
            ],
            'path_traversal': [
                '../', '..\\', '%2e%2e%2f', '%2e%2e\\', 'etc/passwd',
                'windows/system32'
            ],
            'suspicious_requests': [
                '/admin', '/wp-admin', '/phpmyadmin', '/.env',
                '/config', '/backup', '/dump'
            ]
        }
        
        logger.info("✅ Threat patterns loaded")
    
    def _initialize_audit_log(self):
        """Initialize security audit logging"""
        self.audit_log = []
        logger.info("✅ Audit logging initialized")
    
    def analyze_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze incoming request for security threats
        """
        threats_detected = []
        risk_score = 0.0
        
        # Extract request components
        ip_address = request_data.get('ip_address', 'unknown')
        user_agent = request_data.get('user_agent', 'unknown')
        method = request_data.get('method', 'GET')
        path = request_data.get('path', '/')
        headers = request_data.get('headers', {})
        body = request_data.get('body', '')
        
        # Check IP against blocklist
        if ip_address in self.blocked_ips:
            threats_detected.append({
                'type': ThreatType.UNAUTHORIZED_ACCESS,
                'severity': 'high',
                'description': f'Blocked IP attempted access: {ip_address}'
            })
            risk_score += 0.8
        
        # Analyze for injection attacks
        injection_threats = self._check_injection_attacks(body, path, headers)
        threats_detected.extend(injection_threats)
        risk_score += len(injection_threats) * 0.3
        
        # Check for suspicious patterns
        suspicious_threats = self._check_suspicious_patterns(method, path, body)
        threats_detected.extend(suspicious_threats)
        risk_score += len(suspicious_threats) * 0.2
        
        # Rate limiting check
        if self._is_rate_limited(ip_address):
            threats_detected.append({
                'type': ThreatType.BRUTE_FORCE,
                'severity': 'medium',
                'description': f'Rate limit exceeded for IP: {ip_address}'
            })
            risk_score += 0.4
        
        # Analyze user agent
        ua_threats = self._analyze_user_agent(user_agent)
        threats_detected.extend(ua_threats)
        risk_score += len(ua_threats) * 0.1
        
        # Determine action
        action = 'allow'
        if risk_score >= 0.8:
            action = 'block'
            self._block_ip(ip_address)
        elif risk_score >= 0.5:
            action = 'monitor'
        
        # Log security event
        if threats_detected:
            self._log_security_event(threats_detected, ip_address, user_agent)
        
        return {
            'action': action,
            'risk_score': min(risk_score, 1.0),
            'threats_detected': threats_detected,
            'recommendations': self._generate_security_recommendations(risk_score, threats_detected)
        }
    
    def _check_injection_attacks(self, body: str, path: str, headers: Dict) -> List[Dict]:
        """Check for various injection attacks"""
        threats = []
        content_to_check = f"{body} {path} {json.dumps(headers)}".lower()
        
        for attack_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if pattern in content_to_check:
                    threats.append({
                        'type': ThreatType.INJECTION,
                        'severity': 'high',
                        'description': f'{attack_type.replace("_", " ").title()} detected: {pattern}'
                    })
        
        return threats
    
    def _check_suspicious_patterns(self, method: str, path: str, body: str) -> List[Dict]:
        """Check for suspicious request patterns"""
        threats = []
        
        # Check for admin paths
        for pattern in self.threat_patterns['suspicious_requests']:
            if pattern in path.lower():
                threats.append({
                    'type': ThreatType.SUSPICIOUS_ACTIVITY,
                    'severity': 'medium',
                    'description': f'Suspicious path access: {path}'
                })
        
        # Check for unusual request sizes
        if len(body) > 100000:  # 100KB
            threats.append({
                'type': ThreatType.SUSPICIOUS_ACTIVITY,
                'severity': 'low',
                'description': 'Unusually large request body'
            })
        
        return threats
    
    def _analyze_user_agent(self, user_agent: str) -> List[Dict]:
        """Analyze user agent for suspicious patterns"""
        threats = []
        
        # Check for known malicious bots
        malicious_bots = ['sqlmap', 'nikto', 'nmap', 'masscan', 'zap']
        user_agent_lower = user_agent.lower()
        
        for bot in malicious_bots:
            if bot in user_agent_lower:
                threats.append({
                    'type': ThreatType.SUSPICIOUS_ACTIVITY,
                    'severity': 'high',
                    'description': f'Malicious bot detected: {bot}'
                })
        
        # Check for missing/empty user agent
        if not user_agent or user_agent.strip() == '':
            threats.append({
                'type': ThreatType.SUSPICIOUS_ACTIVITY,
                'severity': 'low',
                'description': 'Empty or missing user agent'
            })
        
        return threats
    
    def _is_rate_limited(self, ip_address: str) -> bool:
        """Check if IP has exceeded rate limits"""
        current_time = time.time()
        
        if ip_address not in self.suspicious_patterns:
            self.suspicious_patterns[ip_address] = []
        
        # Clean old requests (older than 1 minute)
        self.suspicious_patterns[ip_address] = [
            req_time for req_time in self.suspicious_patterns[ip_address]
            if current_time - req_time < 60
        ]
        
        # Check rate limit (max 60 requests per minute)
        return len(self.suspicious_patterns[ip_address]) > 60
    
    def _block_ip(self, ip_address: str):
        """Block IP address"""
        self.blocked_ips.add(ip_address)
        logger.warning(f"🚫 IP blocked: {ip_address}")
    
    def _log_security_event(self, threats: List[Dict], ip_address: str, user_agent: str):
        """Log security event"""
        for threat in threats:
            event = SecurityEvent(
                event_type=threat['type'],
                severity=threat['severity'],
                description=threat['description'],
                timestamp=datetime.now(),
                source_ip=ip_address,
                user_agent=user_agent,
                blocked=threat['severity'] in ['high', 'critical']
            )
            
            self.security_events.append(event)
            
            # Log to audit trail
            self._audit_log(event)
    
    def _audit_log(self, event: SecurityEvent):
        """Add event to audit log"""
        audit_entry = {
            'timestamp': event.timestamp.isoformat(),
            'event_type': event.event_type.value,
            'severity': event.severity,
            'description': event.description,
            'source_ip': event.source_ip,
            'blocked': event.blocked
        }
        
        self.audit_log.append(audit_entry)
        
        # Keep audit log manageable
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-5000:]
    
    def _generate_security_recommendations(self, risk_score: float, threats: List[Dict]) -> List[str]:
        """Generate security recommendations based on analysis"""
        recommendations = []
        
        if risk_score >= 0.8:
            recommendations.append("Immediate action required: High-risk threat detected")
            recommendations.append("Consider blocking the source IP address")
        
        if any(t['type'] == ThreatType.INJECTION for t in threats):
            recommendations.append("Implement input validation and sanitization")
            recommendations.append("Use parameterized queries for database operations")
        
        if any(t['type'] == ThreatType.BRUTE_FORCE for t in threats):
            recommendations.append("Implement stronger rate limiting")
            recommendations.append("Consider CAPTCHA for suspicious requests")
        
        if risk_score >= 0.5:
            recommendations.append("Enable additional monitoring for this session")
            recommendations.append("Review security logs for related activities")
        
        return recommendations
    
    def encrypt_data(self, data: str) -> Tuple[str, str]:
        """Encrypt sensitive data"""
        if not self.current_policy.encryption_enabled or not self.master_key:
            return data, "none"
        
        try:
            import os
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            
            # Generate random IV
            iv = os.urandom(16)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.master_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            
            # Pad data
            padded_data = self._pad_data(data.encode())
            
            # Encrypt
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            # Return hex-encoded encrypted data and IV
            return encrypted_data.hex(), iv.hex()
            
        except ImportError:
            logger.warning("Cryptography library not available, using simple encoding")
            # Fallback to simple encoding
            encoded = data.encode().hex()
            return encoded, "simple"
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data, "failed"
    
    def decrypt_data(self, encrypted_data: str, iv: str) -> str:
        """Decrypt sensitive data"""
        if iv == "none":
            return encrypted_data
        elif iv == "simple":
            return bytes.fromhex(encrypted_data).decode()
        elif iv == "failed":
            return encrypted_data
        
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            
            # Convert from hex
            encrypted_bytes = bytes.fromhex(encrypted_data)
            iv_bytes = bytes.fromhex(iv)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.master_key),
                modes.CBC(iv_bytes),
                backend=default_backend()
            )
            
            # Decrypt
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
            
            # Remove padding
            data = self._unpad_data(padded_data)
            
            return data.decode()
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_data
    
    def _pad_data(self, data: bytes) -> bytes:
        """PKCS7 padding"""
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_data(self, padded_data: bytes) -> bytes:
        """Remove PKCS7 padding"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def create_session(self, user_id: str, context: Dict = None) -> str:
        """Create secure session"""
        session_id = secrets.token_urlsafe(32)
        session_key = secrets.token_bytes(32)
        
        session_data = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=self.current_policy.session_timeout)).isoformat(),
            'context': context or {},
            'ip_address': context.get('ip_address') if context else None,
            'user_agent': context.get('user_agent') if context else None
        }
        
        # Encrypt session data
        encrypted_data, iv = self.encrypt_data(json.dumps(session_data))
        
        self.active_sessions[session_id] = {
            'encrypted_data': encrypted_data,
            'iv': iv,
            'session_key': session_key.hex()
        }
        
        logger.info(f"✅ Session created for user: {user_id}")
        return session_id
    
    def validate_session(self, session_id: str, ip_address: str = None) -> Dict[str, Any]:
        """Validate and decrypt session"""
        if session_id not in self.active_sessions:
            return {'valid': False, 'reason': 'Session not found'}
        
        session = self.active_sessions[session_id]
        
        # Decrypt session data
        try:
            session_data = json.loads(self.decrypt_data(session['encrypted_data'], session['iv']))
        except Exception as e:
            logger.error(f"Session decryption failed: {e}")
            return {'valid': False, 'reason': 'Invalid session format'}
        
        # Check expiration
        expires_at = datetime.fromisoformat(session_data['expires_at'])
        if datetime.now() > expires_at:
            del self.active_sessions[session_id]
            return {'valid': False, 'reason': 'Session expired'}
        
        # Check IP address if provided
        if ip_address and session_data.get('ip_address'):
            if ip_address != session_data['ip_address']:
                logger.warning(f"Session IP mismatch: {ip_address} vs {session_data['ip_address']}")
                # Don't invalidate session, but log for security monitoring
        
        return {
            'valid': True,
            'user_id': session_data['user_id'],
            'context': session_data.get('context', {}),
            'expires_at': session_data['expires_at']
        }
    
    def revoke_session(self, session_id: str):
        """Revoke session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"🔒 Session revoked: {session_id}")
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status"""
        current_time = datetime.now()
        
        # Recent events (last 24 hours)
        recent_events = [
            event for event in self.security_events
            if current_time - event.timestamp < timedelta(hours=24)
        ]
        
        # Event counts by severity
        severity_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        for event in recent_events:
            severity_counts[event.severity] += 1
        
        # Active sessions count
        active_sessions_count = len(self.active_sessions)
        
        # Blocked IPs count
        blocked_ips_count = len(self.blocked_ips)
        
        # Risk assessment
        total_events = len(recent_events)
        high_risk_events = severity_counts['high'] + severity_counts['critical']
        risk_level = 'low'
        if total_events > 100:
            risk_level = 'medium'
        if high_risk_events > 10:
            risk_level = 'high'
        if high_risk_events > 50:
            risk_level = 'critical'
        
        return {
            'risk_level': risk_level,
            'total_events_24h': total_events,
            'severity_breakdown': severity_counts,
            'active_sessions': active_sessions_count,
            'blocked_ips': blocked_ips_count,
            'policy_level': self.current_policy.level.value,
            'encryption_enabled': self.current_policy.encryption_enabled,
            'audit_logging': self.current_policy.audit_logging,
            'last_updated': current_time.isoformat()
        }
    
    def update_security_policy(self, new_policy: Dict[str, Any]):
        """Update security policy"""
        for key, value in new_policy.items():
            if hasattr(self.current_policy, key):
                setattr(self.current_policy, key, value)
        
        logger.info(f"🔐 Security policy updated: {new_policy}")
    
    def cleanup_expired_data(self):
        """Clean up expired sessions and old data"""
        current_time = datetime.now()
        
        # Clean expired sessions
        expired_sessions = []
        for session_id, session in self.active_sessions.items():
            try:
                session_data = json.loads(self.decrypt_data(session['encrypted_data'], session['iv']))
                expires_at = datetime.fromisoformat(session_data['expires_at'])
                if current_time > expires_at:
                    expired_sessions.append(session_id)
            except:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
        
        # Clean old security events (older than retention period)
        retention_date = current_time - timedelta(days=self.current_policy.data_retention_days)
        self.security_events = [
            event for event in self.security_events
            if event.timestamp > retention_date
        ]
        
        # Clean old audit log entries
        self.audit_log = [
            entry for entry in self.audit_log
            if datetime.fromisoformat(entry['timestamp']) > retention_date
        ]
        
        logger.info(f"🧹 Cleaned {len(expired_sessions)} expired sessions and old data")
