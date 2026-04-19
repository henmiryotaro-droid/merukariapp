import os

def handler(request):
    email = os.getenv('MERCARI_EMAIL')
    password = os.getenv('MERCARI_PASSWORD')

    if not email or not password:
        return {
            "status": "warning",
            "message": "MERCARI_EMAIL and MERCARI_PASSWORD are not defined in Vercel environment variables. Set them if you want to configure the app, but Selenium browser automation still requires a local runtime."
        }

    return {
        "status": "ok",
        "message": "This route is deployed on Vercel. Mercari automation cannot be executed in Vercel because it requires browser automation (Chrome/Selenium). Use a local or dedicated server deployment instead."
    }

app = handler
application = handler
