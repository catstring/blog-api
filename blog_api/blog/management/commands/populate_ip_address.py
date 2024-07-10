# blog/management/commands/populate_ip_address.py
from django.core.management.base import BaseCommand
from blog.models import PostView

class Command(BaseCommand):
    help = 'Populate ip_address field for existing PostView records'

    def handle(self, *args, **kwargs):
        default_ip = '0.0.0.0'
        post_views = PostView.objects.filter(ip_address__isnull=True)
        for pv in post_views:
            pv.ip_address = default_ip
            pv.save()
        self.stdout.write(self.style.SUCCESS('Successfully populated ip_address field for existing PostView records'))
