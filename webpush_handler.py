from pywebpush import webpush, WebPushException
import json
from flask import current_app

def trigger_push_notification(sub, title, body):
    ...
def trigger_push_notifications_for_subscriptions(subscriptions, title, body):
    ...
