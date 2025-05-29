from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from datetime import datetime, timedelta
from .models import DailyReport
from .serializers import DailyReportSerializer
from device_management.models import Device
from power_metrics.models import PowerQualityMetrics
from notifications.models import PowerQualityEvent

class DailyReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyReport.objects.all()
    serializer_class = DailyReportSerializer
    filterset_fields = ['device', 'date']

class DashboardAPIView(APIView):
    """Main dashboard API endpoint"""
    
    def get(self, request):
        """Get dashboard summary data"""
        
        # Device summary
        device_summary = {
            'total_devices': Device.objects.count(),
            'online_devices': Device.objects.filter(status='online').count(),
            'offline_devices': Device.objects.filter(status='offline').count(),
        }
        
        # Recent events
        recent_events = PowerQualityEvent.objects.filter(
            timestamp__gte=datetime.now() - timedelta(hours=24)
        ).count()
        
        # Power quality summary (last 24 hours)
        pq_summary = PowerQualityMetrics.objects.filter(
            timestamp__gte=datetime.now() - timedelta(hours=24)
        ).aggregate(
            avg_voltage=Avg('voltage_rms'),
            avg_current=Avg('current_rms'),
            avg_power_factor=Avg('power_factor'),
            avg_frequency=Avg('frequency'),
            avg_voltage_thd=Avg('voltage_thd'),
            avg_current_thd=Avg('current_thd'),
        )
        
        # System health score
        health_score = self.calculate_system_health()
        
        # Device type distribution
        device_types = Device.objects.values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Event severity distribution
        event_severity = PowerQualityEvent.objects.filter(
            timestamp__gte=datetime.now() - timedelta(days=7)
        ).values('severity').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'device_summary': device_summary,
            'recent_events': recent_events,
            'power_quality': pq_summary,
            'system_health': health_score,
            'device_types': list(device_types),
            'event_severity': list(event_severity),
            'timestamp': datetime.now().isoformat()
        })
    
    def calculate_system_health(self):
        """Calculate overall system health score"""
        # Base score starts at 100
        score = 100
        
        # Device health impact (40% of total score)
        total_devices = Device.objects.count()
        if total_devices > 0:
            online_ratio = Device.objects.filter(status='online').count() / total_devices
            score -= (1 - online_ratio) * 40
        
        # Recent critical events impact (30% of total score)
        recent_critical_events = PowerQualityEvent.objects.filter(
            timestamp__gte=datetime.now() - timedelta(hours=24),
            severity='critical'
        ).count()
        score -= min(recent_critical_events * 5, 30)  # Max 30% reduction
        
        # Power quality impact (30% of total score)
        recent_metrics = PowerQualityMetrics.objects.filter(
            timestamp__gte=datetime.now() - timedelta(hours=1)
        ).aggregate(
            avg_voltage_thd=Avg('voltage_thd'),
            avg_power_factor=Avg('power_factor')
        )
        
        if recent_metrics['avg_voltage_thd']:
            # THD above 5% starts impacting score
            thd_impact = max(0, (recent_metrics['avg_voltage_thd'] - 0.05) * 200)
            score -= min(thd_impact, 15)  # Max 15% reduction
        
        if recent_metrics['avg_power_factor']:
            # Power factor below 0.95 starts impacting score
            pf_impact = max(0, (0.95 - recent_metrics['avg_power_factor']) * 200)
            score -= min(pf_impact, 15)  # Max 15% reduction
        
        return max(0, min(100, score))  # Ensure score is between 0 and 100 