import os


def handler(request):
    email = os.getenv('MERCARI_EMAIL')
    password = os.getenv('MERCARI_PASSWORD')

    if not email or not password:
        return {
            "status": "warning",
            "message": "MERCARI_EMAIL and MERCARI_PASSWORD are not set in environment variables. Set them in Vercel environment variables if you want to enable configuration feedback."
        }

    return {
        "status": "ok",
        "message": "Vercel deploy is active. Mercari automation itself requires Selenium and Chrome and must run on a local or dedicated server."
    }
