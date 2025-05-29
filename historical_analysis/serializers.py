from rest_framework import serializers
from .models import DailyReport, TrendAnalysis

class DailyReportSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_type = serializers.CharField(source='device.device_type', read_only=True)
    
    class Meta:
        model = DailyReport
        fields = '__all__'
        read_only_fields = ('created_at',)

class TrendAnalysisSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    
    class Meta:
        model = TrendAnalysis
        fields = '__all__'
        read_only_fields = ('created_at',) 