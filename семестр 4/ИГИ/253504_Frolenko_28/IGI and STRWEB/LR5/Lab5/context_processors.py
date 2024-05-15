from django.utils import timezone
from tzlocal import get_localzone


def current_time(request):
    local_tz = get_localzone()
    local_time = timezone.now().astimezone(local_tz)
    formatted_time = local_time.strftime('%H:%M:%S')
    return {'current_time': formatted_time}
