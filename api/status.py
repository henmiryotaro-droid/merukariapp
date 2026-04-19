def handler(request):
    return {
        "status": "ok",
        "message": "Vercel Python runtime is active. The Mercari automation logic must run on a local or dedicated server because browser automation is not supported in Vercel serverless." 
    }
