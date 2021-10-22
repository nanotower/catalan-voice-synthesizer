from starlette.responses import PlainTextResponse

def check(request):
    return PlainTextResponse("I'm alive")