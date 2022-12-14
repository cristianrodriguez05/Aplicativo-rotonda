import cx_Oracle
from flask import Flask, render_template, redirect, request, url_for, make_response

conexion = cx_Oracle.connect(
user='CINEMA',
password='cinema',
dsn='localhost/xe')



app = Flask(__name__)

#peliculas = consulta que trae las peliculas
def traerpelis(): 
    cur_01=conexion.cursor()
    select_FUNCION= " SELECT * FROM PELICULA"
    cur_01.execute(select_FUNCION)
    resultados=cur_01.fetchall()
    resultadosjson=[]
    for resultado in resultados: 
       resultadosjson.append({
        "titulo":resultado[1],
        "ruta":"/static/images/"+resultado[1]+".jpg",
        "formato":resultado[3],
        })   

    print(resultadosjson)
    return resultadosjson


def sillas(a,filas,columnas):
    #esta funcion no esta bien pero al menos es algo
    retorno=''
    if a=='t':
        for i in range(filas):
            retorno=retorno*(columnas+i)
    if a=='c':
        for i in range(filas):
            retorno=retorno*columnas
    return retorno




@app.route('/', methods = ['POST','GET'])
def inicio():
    resp=make_response(render_template('index.html'))
    resp.set_cookie('usuario', '0')
    resp.set_cookie('name_user','0')
    resp.set_cookie('fichas','0')
    resp.set_cookie('typeU','0')
    resp.set_cookie('peli','0')
    return resp
    
def pasara(cantidad):
    num = int(cantidad)
    enviar=[]
    for i in range(1,num+1):
        enviar.append(i)
    return enviar

@app.route('/inicio', methods = ['POST','GET'])
def iniciou():
    userExist = request.cookies.get('usuario')
    nombre=request.cookies.get('name_user')
    typeU=''
    cantidad=''
    if userExist == None or nombre=='0':
        correo=request.form['email']
        password=request.form['Pass']
        #aqui se debe hacer la consulta para saber si si es el usuario o no
        #y aqui añadir una variable para asi saber si se es un admin, taquilla, gerente o cliente
        if '@usu.cine.com' in correo:
            cur_01=conexion.cursor()
            select_usuario= " select * from usuario WHERE correo ='"+correo+"'"
            cur_01.execute(select_usuario)
            resultados_usu=cur_01.fetchone()
            print(resultados_usu)
            if '@usu.cine.com' in resultados_usu[3]:
                if  password == str(resultados_usu[4]):
                    print(resultados_usu[4])
                    typeU='Usuario'
                    #nombre=consulta para el nombre del usuario
                    #cantidad=consulta para conseguir las fichas
                    nombre=resultados_usu[1]
                    cantidad=str(resultados_usu[7])
                    exist='si'
                    resp = make_response(render_template ('iniciou.html',typeU=typeU,nombre=nombre,fichas=cantidad))
                    resp.set_cookie('name_user',nombre)
                    resp.set_cookie('typeU', typeU)
                    resp.set_cookie('fichas', cantidad)
                    resp.set_cookie('usuario', exist)
                    return resp
                else:
                    return redirect ('/')
        else:
            cur_01=conexion.cursor()
            select_empleado= " select * from empleado WHERE correo_emp ='"+correo+"'"
            print(correo)
            cur_01.execute(select_empleado)
            resultados=cur_01.fetchone()
            print(resultados)
            
            #aqui se debe hacer la consulta para saber si si es el usuario o no
            #y aqui añadir una variable para asi saber si se es un admin, taquilla, gerente o cliente
            if '@adm.cine.com' in resultados[7]:
                typeU='Admin'
                #nombre = consulta para el nombre del admin
                #cantidad = consulta opara la cantidad de salas
                nombre=resultados[1]
                print('imprimo nombre')
                cur_01=conexion.cursor()
                select_sala= " SELECT * FROM SALA"
                cur_01.execute(select_sala)
                resultado_tam=len(cur_01.fetchall())
                cantidad=str(resultado_tam)
                print('imprimo cantidad')
                print(cantidad)
                cantenv=pasara(cantidad)
                exist='si'
                resp = make_response(render_template('iniciou.html',typeU=typeU,nombre=nombre,cantidad=cantenv))
                resp.set_cookie('name_user',nombre)
                resp.set_cookie('typeU', typeU)
                resp.set_cookie('fichas', cantidad)
                resp.set_cookie('usuario', exist)
                return resp
            if '@taq.cine.com' in resultados[7]:
                typeU='Taquilla'
                #nombre = consulta para el nombre del admin
                #cantidad = consulta opara la cantidad de salas
                nombre=resultados[1]
                cur_01=conexion.cursor()
                select_sala= " SELECT * FROM SALA"
                cur_01.execute(select_sala)
                resultado_tam=len(cur_01.fetchall())
                cantidad=str(resultado_tam)
                cantenv=pasara(cantidad)
                exist='si'
                resp = make_response(render_template('iniciou.html',typeU=typeU,nombre=nombre,cantidad=cantenv))
                resp.set_cookie('name_user',nombre)
                resp.set_cookie('typeU', typeU)
                resp.set_cookie('fichas', cantidad)
                resp.set_cookie('usuario', exist)
                return resp
            if '@ger.cine.com' in resultados[7]:
                typeU='Gerente'
                nombre=resultados[1]
                cur_01=conexion.cursor()
                select_sala= " SELECT * FROM SALA"
                cur_01.execute(select_sala)
                resultado_tam=len(cur_01.fetchall())
                cantidad=str(resultado_tam)
                cantenv=pasara(cantidad)
                exist='si'
                resp = make_response(render_template('iniciou.html',typeU=typeU,nombre=nombre,cantidad=cantenv))
                resp.set_cookie('name_user',nombre)
                resp.set_cookie('typeU', typeU)
                resp.set_cookie('fichas', cantidad)
                resp.set_cookie('usuario', exist)
                return resp
            
    else:
        typeU=request.cookies.get('typeU')
        if typeU=='Usuario':
            nombre=request.cookies.get('name_user')
            cantidad=request.cookies.get('fichas')
            return render_template ('iniciou.html',typeU=typeU,nombre=nombre,fichas=cantidad)
        if typeU=='Admin':
            #aqui se deberia recibir el formulario para nueva sala o nueva persona
            #forma, fila y columna son datos que vienen del front
            forma='trapecio'
            filas=5
            columna=10
            if (forma=='trapecio'):
                sillas=('t',filas,columna)
            if (forma=='cuadrado'):
                sillas=('c',filas,columna)
            nombre=request.cookies.get('name_user')
            #cantidad = consulta opara la cantidad de salas
            cur_01=conexion.cursor()
            select_sala= " SELECT * FROM SALA"
            cur_01.execute(select_sala)
            resultado_tam=len(cur_01.fetchall())
            cantidad=str(resultado_tam)
            resp = make_response(render_template('iniciou.html',typeU=typeU,nombre=nombre,fichas=cantidad,cantidad=pasara(cantidad)))
            resp.set_cookie('fichas',cantidad)
            return resp
        if typeU=='Taquilla':
            nombre=request.cookies.get('name_user')
            cantidad=request.cookies.get('fichas')
            render_template('iniciou.html',typeU=typeU,nombre=nombre,cantidad=pasara(cantidad))


@app.route('/mas/<peli>', methods = ['POST','GET'])
def mostrarmas(peli):
    #sentencia SQL para traer los detalles (sala, horario, tipo (2D, 3D, cinemax, etc de la peli)), el nombre de la pelicula esta en la variable peli
    cur_01=conexion.cursor()
    select_FUNCION= " SELECT * FROM FUNCION"
    cur_01.execute(select_FUNCION)
    resultados=cur_01.fetchall()
    resultadosjson=[]
    for resultado in resultados: 
       # resultadosjson.append({
        #    "sala":resultado[3],
         #   "fecha":resultado[0],
          #  "formato":resultado[4],
       # })
        resultadosjson.append({'Sala': resultado[3],
        'Horario':resultado[0],
        'tipo':resultado[4],
        })
   # ]
    #disposicion=[
     #   {'Sala': resultado[3],'Horario':resultado[0],'tipo':resultado[4]},
      #  {'Sala': 'Sala1','Horario':'1 pm','tipo':'2D'},
       # {'Sala': 'Sala2','Horario':'2 pm','tipo':'3D'},  
   # ]
    #traer la sinopsis de la pelicula 
    sinopsis='sinopsis de la pelicula'
    #traer la ubicacion de la pelicula si algo es solo poner el nombre de la pelicula luego de el resto
    ubicacion="/static/images/Toy Story 3.jpg"
    resp = make_response(render_template('mas.html', peli=peli, disposicion=resultadosjson,sinopsis=sinopsis,ubicacion=ubicacion))
    resp.set_cookie('peli',peli)
    return resp


@app.route('/about', methods = ['POST','GET'])
def aboutUs():
    return render_template('about-us.html')

@app.route('/articles', methods = ['POST','GET'])
def articles():
    return render_template('articles.html')


@app.route('/article', methods = ['POST','GET'])
def article():
    return render_template('article.html')


@app.route('/contact', methods = ['POST','GET'])
def contact():
    return render_template('contact-us.html')

@app.route('/map', methods = ['POST','GET'])
def map():
    return render_template('sitemap.html')

@app.route('/newSala', methods = ['POST','GET'])
def newSala():
    nombre=request.cookies.get('name_user')
    return render_template('newSala.html',nombre=nombre)

@app.route('/empleado', methods = ['POST','GET'])
def empleado():
    nombre=request.cookies.get('name_user')
    return render_template('empleado.html',nombre=nombre)

@app.route('/vista/<sala>/<horario>', methods = ['POST','GET'])
def registroLlegada(sala,horario):
    
    #forma = consulta para traer la forma de la sala, la sala es la variable sala
    
    forma='trapecio'
    #matriz = aqui se debe traer la disposicion de la sala, es decir ocupado o no y se necesita la variable horario
    matriz = [
    {'A1':True,'A2':False,'A3':True},
    {'B1':False,'B2':True,'B3':True,'B4':True},
    {'C1':True,'C2':True,'C3':True,'C4':True,'C5':True},
    {'D1':True,'D2':True,'D3':False,'D4':True,'D5':True,'D6':False},    
    {'D1':True,'D2':True,'D3':False,'D4':True,'D5':True,'D6':False},    
    {'D1':True,'D2':True,'D3':False,'D4':True,'D5':True,'D6':False},    
    ]
    heib = len(matriz)
    #peli = pelicula que se ve en esa sala y ese horario
    peli='pelicula1'
    return render_template('registrollegada.html',forma=forma,matriz=matriz,heif=heib,sala=sala,horario=horario,peli=peli)

@app.route('/versalas/<sala>', methods = ['POST','GET'])
def versala(sala):
    #aqui se debe traer el horario de la sala, el numero de la sala es la variable sala
    horario=[
        {'Hora':'11 am','Pelicula':'nombre pelicula','tipo':'2D'},
        {'Hora':'11 am','Pelicula':'nombre pelicula','tipo':'2D'},
        {'Hora':'11 am','Pelicula':'nombre pelicula','tipo':'2D'},  
    ]
    typeU=request.cookies.get('typeU')
    return render_template('versala.html',sala=sala,horario=horario,typeU=typeU)   

@app.route('/nuevafuncion/<sala>', methods=['POST','GET'])
def nuevafuncion(sala):
    #traer las peliculas
    peliculas=['pelicula1','pelicula2','pelicula3',]
    return render_template('newFuncion.html',peliculas=peliculas,sala=sala)


if __name__ == '__main__':
    app.run(debug=True)