from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


def get_lat_long(address):
    geolocator = Nominatim(user_agent="community_app")
    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude

    return None, None


def calculate_distance(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]:
        return None

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return 6371 * c  # KM



def get_nearest_users(need, max_distance_km=10):
    nearby_users = []

    for user in User.objects.all():
        if not hasattr(user, "contact_info"):
            continue

        ci = user.contact_info
        distance = calculate_distance(
            need.latitude, need.longitude,
            ci.latitude, ci.longitude
        )

        if distance is not None and distance <= max_distance_km:
            nearby_users.append(user)

    return nearby_users



def send_need_email(users, need):
    subject = f"New Need Near You: {need.title}"

    message = f"""
Hello,

A new need has been created near you.

Title: {need.title}
Category: {need.category}
Urgency: {need.urgency}
Location: {need.location}

Please login to help if you can.
"""

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [u.email for u in users if u.email]

    if recipient_list:
        send_mail(subject, message, from_email, recipient_list)