class SimpleMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"BEFORE REQUEST FOR {request.path}")
        response = self.get_response(request)
        print("AFTER GITTING RESPONSE")
        return response