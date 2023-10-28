from django.contrib import admin
from .models import SmtpModel
# Register your models here.



@admin.register(SmtpModel)
class SmtpModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'smtp_server', 'port', 'app_password')

    # Override queryset to restrict access to records based on the logged-in user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs
