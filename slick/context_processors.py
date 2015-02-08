

def slick(request):
    #print request.COOKIES.get('SIDEBAR_SM', None)
    return {'SIDEBAR_SM': request.COOKIES.get('SIDEBAR_SM', None) }