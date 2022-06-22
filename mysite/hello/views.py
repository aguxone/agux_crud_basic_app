from django.shortcuts import render

# Create your views here.

# NOTAR, este archivo RECIBE TODAS LAS REQUESTS.
# request va de parámetro en TODO.
# TODA request a ser procesado por las funciones que lleven
# request como parámetro ojo!
# En este caso crearemos una cookie chota nomás.
# Y bueno estas funciones contarán como "view"
# También podríamos hacer clases si no pero bueno más corto una
# función si no tenemos que heredar ningún generic view ni nada.

from django.http import HttpResponse

def myview(request):
    print (request.COOKIES)

    sess = request.session #Vamos a usar la sesion porque el autograder tira error
    # O sea el chaval quiere que creemos todo lo que hizo en el video
    # de contar las visitas y que se resetee si son más de 4.

    # Pedimos el número de visitas en esta sesión y le sumamos 1
    num_visits = sess.get("num_visits",0)+1

    # A la SESION COMO TAL le atribuimos ese número de visitas + 1
    sess["num_visits"] = num_visits

    # Por última si las visitas exceden 4, borramos esa columna de la session
    if num_visits >4:
        del(sess["num_visits"])

    # FINALMENTE creamos la respuesta con el códgio y algo de texto
    # Hacemos un método set_cookie para crear la cookie que quiere
    # OJO CON EL RETURN, devolvemos el objeto HttpResponse, no el objeto con le método
    # el método lo guarda directo en el objeto ya.
    resp=HttpResponse('Welcome to my view? CODE: 6c9084f3 ; Cookie created, session started \n' + "view count=" + str(num_visits))

    resp.set_cookie('dj4e_cookie', '6c9084f3', max_age=1000)

    return resp