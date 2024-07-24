"""
ASGI config for socket_test project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

import django
import socketio
from django.core.asgi import get_asgi_application

from socket_test.soketio import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socket_test.settings")
django.setup()

django_asgi_app = get_asgi_application()
application = socketio.ASGIApp(sio, django_asgi_app, socketio_path="socket.io")
