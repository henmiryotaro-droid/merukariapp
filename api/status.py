import json


def handler(request):
    return {
        "status": "ok",
        "message": "Vercel Python runtime is active. The Mercari automation logic must run on a local or dedicated server because browser automation is not supported in Vercel serverless."
    }


def app(environ, start_response):
    response = handler(None)
    body = json.dumps(response).encode('utf-8')
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [body]


application = app
