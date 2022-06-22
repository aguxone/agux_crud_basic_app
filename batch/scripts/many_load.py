import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from unesco.models import Category, State, Iso, Region, Site


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    # Hasta acá anda todo como debe!

    # We delete everything first, because we might have run a previous
    # # database before.
    Category.objects.all().delete()
    State.objects.all().delete()
    Iso.objects.all().delete()
    Region.objects.all().delete()
    Site.objects.all().delete() # Through table included

    # # Format
    # # email,role,course
    # # jane@tsugi.org,I,Python
    # # ed@tsugi.org,L,Python


    for row in reader:

        # Usamos el método get_or_create que llenará las tablas con datos posta
        # el row[numero] el número es básicamente la columna que queremos
        # que la vemos en el csv o xls


        #Second the ones that do need relationships
        # These ones are have their own table apart from the though table one
        c, created = Category.objects.get_or_create(name=row[7]) #El parámetro no es un nombre cualquiera
        # es el nombre que está en el model, o sea la columna, y le pusimos name a todas como cosa genérica.
        # en el ejemplo de many que tenía él decía email y otras cosas.
        s, created = State.objects.get_or_create(name=row[8])
        r, created = Region.objects.get_or_create(name=row[9])
        i, created = Iso.objects.get_or_create(name=row[10])

        #La through table en cambio no volvemos a extraer de row los datos,
        # ya los sacamos, entonces le ponemos el nombre de las columnas y
        # nomás DIRECCIONAMOS (justo como se hace con un variable es literalemente
        # eso) a las variables que YA existen, con esto no repetimos datos.
        # AHORA por qué el get_or_create y no ponerlos a manos con Site(name...) como hacemos
        # con los otros? Bueno JUSTAMENTE por el get_or create, en Site vamos direccionar a get_or_create
        # y no a los datos, si ya existen hará un get y obtendrá los datos de la otra tabal y nos los guardará
        # si no existen bueno los creará en la tabla original de hecho.
        # En cambio si direccionamos a la variable Site(name..) estaríamos duplicando el dato en la tabla Site,
        # porque no hace un get, directamente lo crea!

        # PERO ADEMÁS debemos meter la otra data que no necesita relationships
        # la metemos de manera más facilonga directo en Site.
        # Hay un temita y es que los que tienen números pueden
        # tener valores vacíos, así que a esos les meteremos un try, y si no hay nada
        # le meteremos un None como para que NO quede vacía la database
        # el script nos tira error si no porque espera números el field.

        # Es importante transformar las filas que extrae a int o float
        # porque si se encuentra con algo vacío se tilda igual
        # por mucho try que hagamos tira error igual y se frena, malísimo.
        #Try for Year
        try:
            y=int(row[3])
        except:
            y=None
        # Latitude
        try:
            la=float(row[5])
        except:
            la=None

        # Longitude
        try:
            l=float(row[4])
        except:
            l=None

        # area_hectares
        try:
            a=float(row[6])
        except:
            a=None

        si= Site(name=row[0], year=y, latitude=la, longitude=l, description=row[1], justification=row[2], area_hectares=a, category=c, state=s, iso=i, region=r)

        # Como no usamos el método get_or_create, finalmente debemos darle un save
        # para que quede gaurdado posta.
        si.save()

