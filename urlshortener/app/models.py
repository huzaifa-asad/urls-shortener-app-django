from django.db import models
from django.conf import settings
import qrcode
from io import BytesIO
import base64

# Create your models here.

class URL(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
    def get_short_url(self, request=None):
        """Get the full short URL with dynamic domain detection"""
        if request:
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
            return f"{protocol}://{domain}/{self.short_code}/"
        # Fallback for when no request is available
        from django.conf import settings
        if hasattr(settings, 'SITE_URL'):
            return f"{settings.SITE_URL}/{self.short_code}/"
        return f"http://localhost:8000/{self.short_code}/"
    
    def generate_qr_code(self, request=None):
        """Generate QR code for the original URL"""
        # Use the original URL directly instead of the short URL
        target_url = self.original_url
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,  # Controls the size (1 is 21x21)
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(target_url)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for HTML display
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return qr_base64
    
    def get_qr_code_data_url(self, request=None):
        """Get QR code as data URL for HTML img src"""
        qr_base64 = self.generate_qr_code(request)
        return f"data:image/png;base64,{qr_base64}"
