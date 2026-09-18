from app import app
from pprint import pprint

client = app.test_client()

endpoints = [
    ('/api/files/vt/scan', {'hash':'44d88612fea8a8f36de82e1278abb02f'}),
    ('/api/files/abuseipdb/check', {'ip':'8.8.8.8'}),
    ('/api/files/otx/ip', {'ip':'8.8.8.8'}),
    ('/api/files/shodan/host', {'ip':'8.8.8.8'}),
    ('/api/files/urlhaus/check', {'url':'http://example.com'}),
    ('/api/files/ismalicious/check', {'url':'http://example.com'}),
    ('/api/files/analyze', {'ip':'8.8.8.8','url':'http://example.com'})
]

print('=== endpoint tests ===')
for path, payload in endpoints:
    r = client.post(path, json=payload)
    print('\n', path, 'status', r.status_code)
    try:
        pprint(r.get_json())
    except Exception as e:
        print('  <non-json>', e)
