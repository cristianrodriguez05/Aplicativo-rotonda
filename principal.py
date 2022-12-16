import cx_Oracle
from flask import Flask, render_template, redirect, request, url_for, make_response

conexion = cx_Oracle.connect(
user='ROTONDA',
password='rotonda',
dsn='localhost/xe')



app = Flask(__name__)


@app.route('/', methods = ['POST','GET'])
def inicio():
    resp=make_response(render_template('index.html'))
    resp.set_cookie('usuario', '0')
    resp.set_cookie('name_user','0')
    resp.set_cookie('typeU','0')
    return resp


@app.route('/inicio', methods = ['POST','GET'])
def home():
    userExist = request.cookies.get('usuario')
    nombre=request.cookies.get('name_user')
    typeU=''
    if userExist == None or nombre=='0':
        correo=request.form['email']
        password=request.form['Pass']
        #aqui se debe hacer la consulta para saber si si es el usuario o no
        #y aqui añadir una variable para asi saber si se es un admin, taquilla, gerente o cliente
        if '@usu.com' in correo:
            cur_01=conexion.cursor()
            select_usuario= " select * from usuario WHERE correo ='"+correo+"'"
            cur_01.execute(select_usuario)
            resultados_usu=cur_01.fetchone()
            print(resultados_usu)
            if '@usu.com' in resultados_usu[3]:
                if  password == str(resultados_usu[4]):
                    print(resultados_usu[4])
                    typeU='Usuario'
                    #nombre=consulta para el nombre del usuario
                    #cantidad=consulta para conseguir las fichas
                    nombre=resultados_usu[1]
                    exist='si'
                    resp = make_response(render_template ('home.html',typeU=typeU,nombre=nombre))
                    resp.set_cookie('name_user',nombre)
                    resp.set_cookie('typeU', typeU)
                    resp.set_cookie('usuario', exist)
                    return resp
                else:
                    return redirect ('/')
        else:
            cur_01=conexion.cursor()
            select_restaurante= " select * from restaurante WHERE correo ='"+correo+"'"
            print(correo)
            cur_01.execute(select_restaurante)
            resultados=cur_01.fetchone()
            print(resultados)
            
            #aqui se debe hacer la consulta para saber si si es el usuario o no
            #y aqui añadir una variable para asi saber si se es un admin, taquilla, gerente o cliente
            if '@adm.com' in resultados[3]:
                typeU='Admin'
                #nombre = consulta para el nombre del admin
                #cantidad = consulta opara la cantidad de salas
                nombre=resultados[1]
                exist='si'
                resp = make_response(render_template('homerestaurante.html',typeU=typeU,nombre=nombre))
                resp.set_cookie('name_user',nombre)
                resp.set_cookie('typeU', typeU)
                resp.set_cookie('usuario', exist)
                return resp
            else:
                    return redirect ('/')        
    else:
        typeU=request.cookies.get('typeU')
        if typeU=='Usuario':
            nombre=request.cookies.get('name_user')
            return render_template ('home.html',typeU=typeU,nombre=nombre)
        print(typeU)
        if typeU=='Admin':
            nombre=request.cookies.get('name_user')
            return render_template('homerestaurante.html',typeU=typeU,nombre=nombre)

@app.route('/homerestaurante', methods = ['POST','GET'])
def homerestaurante():
    return render_template('homerestaurante.html')

@app.route('/restaurantepizza', methods = ['POST','GET'])
def restaurantepizza():
    return render_template('restaurantepizza.html')

@app.route('/restaurantehambur', methods = ['POST','GET'])
def restaurantehambur():
    return render_template('restaurantehambur.html')

@app.route('/restaurantepollo', methods = ['POST','GET'])
def restaurantepollo():
    return render_template('restaurantepollo.html')

@app.route('/restaurantebebida', methods = ['POST','GET'])
def restaurantebebida():
    return render_template('restaurantebebida.html')

@app.route('/agremenu', methods = ['POST','GET'])
def agremenu():
    return render_template('agremenu.html')

@app.route('/agreprod', methods = ['POST','GET'])
def agreprod():
    return render_template('agreprod.html')

@app.route('/agreing', methods = ['POST','GET'])
def agreing():
    return render_template('agreing.html')

@app.route('/modmenu', methods = ['POST','GET'])
def modmenu():
    return render_template('modmenu.html')

if __name__ == '__main__':
    app.run(debug=True)