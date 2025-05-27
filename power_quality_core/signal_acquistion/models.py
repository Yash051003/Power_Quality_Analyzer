from django.db import models
from django.contrib.postgres.fields import ArrayField
from device_management.models import Device

class RawMeasurement(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    
    # RMS Values
    voltage_rms = models.FloatField()
    current_rms = models.FloatField()
    frequency = models.FloatField()
    
    # Raw samples (for harmonic analysis)
    voltage_samples = ArrayField(models.FloatField(), size=512, null=True, blank=True)
    current_samples = ArrayField(models.FloatField(), size=512, null=True, blank=True)
    
    # Additional measurements
    temperature = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'raw_measurements'
        indexes = [
            models.Index(fields=['timestamp', 'device']),
            models.Index(fields=['device', 'timestamp']),
        ]
        
    def __str__(self):
        return f"{self.device.device_id} - {self.timestamp}"
