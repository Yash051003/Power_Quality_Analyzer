from django.db import models
from django.contrib.auth.models import User
from device_management.models import Device

class PowerQualityEvent(models.Model):
    EVENT_TYPES = [
        ('voltage_sag', 'Voltage Sag'),
        ('voltage_swell', 'Voltage Swell'),
        ('interruption', 'Interruption'),
        ('frequency_deviation', 'Frequency Deviation'),
        ('high_thd', 'High THD'),
        ('power_factor_low', 'Low Power Factor'),
        ('unbalance', 'Voltage/Current Unbalance'),
        ('transient', 'Transient'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    timestamp = models.DateTimeField(db_index=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    
    # Event details
    description = models.TextField()
    measured_value = models.FloatField()
    threshold_value = models.FloatField()
    duration = models.DurationField(null=True, blank=True)
    
    # Event resolution
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'power_quality_events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'device']),
            models.Index(fields=['event_type', 'severity']),
        ]


class AlertRule(models.Model):
    PARAMETER_CHOICES = [
        ('voltage_rms', 'RMS Voltage'),
        ('current_rms', 'RMS Current'),
        ('power_factor', 'Power Factor'),
        ('frequency', 'Frequency'),
        ('voltage_thd', 'Voltage THD'),
        ('current_thd', 'Current THD'),
        ('active_power', 'Active Power'),
    ]
    
    CONDITION_CHOICES = [
        ('gt', 'Greater Than'),
        ('lt', 'Less Than'),
        ('eq', 'Equal To'),
        ('between', 'Between'),
    ]

    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)  # Null for global rules
    parameter = models.CharField(max_length=20, choices=PARAMETER_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    threshold_min = models.FloatField()
    threshold_max = models.FloatField(null=True, blank=True)
    severity = models.CharField(max_length=10, choices=PowerQualityEvent.SEVERITY_LEVELS)
    
    # Notification settings
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alert_rules'


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('webhook', 'Webhook'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]

    event = models.ForeignKey(PowerQualityEvent, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    recipient = models.CharField(max_length=200)  # Email, phone number, or device token
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'