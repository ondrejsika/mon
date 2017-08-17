#!/usr/bin/env python

import conf

import smtplib
import datetime

import requests


def check(url):
    try:
        r = requests.get(url)
        if r.status_code < 400:
            return url, True, r.status_code
        return url, False, r.status_code
    except requests.RequestException:
        return url, False, None


def _sendmail(email_from, email_to, message, username, password, server, tls):
    server = smtplib.SMTP(server)
    if tls:
        server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, message)
    server.quit()


def sendmail(subject, message):
    message = 'Subject: %s\nFrom: %s\n\n%s' % (subject, conf.EMAIL_FROM, message)
    return _sendmail(conf.EMAIL_FROM,
                     conf.EMAIL_TO,
                     message,
                     conf.SMTP_USERNAME,
                     conf.SMTP_PASSWORD,
                     conf.SMTP_SERVER,
                     conf.SMTP_TLS)


results = []
error = False

results.append('=== URLS CHECKS ===')
for url in conf.URLS:
    url, status, status_code = check(url)
    if not status:
        error = True
        status_code = status_code if status_code else '   '
        results.append('- [%s] %s' % (status_code, url))

if error:
    message = list(results)
    message.append('')
    message.append('server: %s' % conf.HOSTNAME)
    message.append('timestamp: %s' % datetime.datetime.now().isoformat())
    message.append('')
    message.append('--')
    message.append('mon, simple website monitor <https://github.com/ondrejsika/mon>')
    message = '\n'.join(message)

    print(message)
    sendmail('[mon] Errors found', message)



