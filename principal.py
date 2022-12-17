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
            if '@adm.com' in resultados[2]:
                typeU='Admin'
                #nombre = consulta para el nombre del admin
                #cantidad = consulta opara la cantidad de salas
                nombre=resultados[0]
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
    cur_01=conexion.cursor()
    select_menu= "SELECT * FROM menu"
    cur_01.execute(select_menu)
    resultados=cur_01.fetchall()

    resultadosjson=[]
    for r in resultados: 
        resultadosjson.append({
                "nombre":r[1],
            })
    print(resultadosjson)

    cur_02=conexion.cursor()
    select_prod= "SELECT * FROM producto"
    cur_02.execute(select_prod)
    resultadosprod=cur_02.fetchall()

    resultadosprodjson=[]
    for r in resultadosprod: 
        resultadosprodjson.append({
                "nombre":r[0],
            })
    print(resultadosprodjson)
    return render_template('restaurantepizza.html',resultados=resultadosjson, resultadosprod=resultadosprodjson)
def pasaramenu():
    cur_01=conexion.cursor()
    select_menu= "SELECT * FROM menu"
    cur_01.execute(select_menu)
    resultadosmenu=cur_01.fetchall()
    resultadosmenujson=[]
    for r in resultadosmenu: 
            resultadosmenujson.append({
                "id":r[0],
                "nombre":r[1],
                "precio":r[2],
                "restaurante":r[3],
            })
    print(resultadosmenujson)
    return render_template('pizzamenu.html',resultadosmenu=resultadosmenujson)


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
    if request.method == 'POST':
        id_menu = request.form['id_menu']
        nombre_menu = request.form['nombre_menu']
        precio_menu = request.form['precio_menu']
        restaurante_menu = request.form['restaurante_menu']
        print(id_menu, nombre_menu, precio_menu, restaurante_menu)
        cur_01=conexion.cursor()
        insert_datos= "insert into menu (id_menu, nombre_menu, precio_menu, restaurante_menu) VALUES (:1, :2, :3, :4)"
        print(insert_datos)
        cur_01.execute(insert_datos,[id_menu, nombre_menu, precio_menu, restaurante_menu])
        conexion.commit()
        return render_template('agremenu.html')
    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_menu= "SELECT * FROM menu"
        cur_01.execute(select_menu)
        print(select_menu)
        resultadosmenu=cur_01.fetchall()
        resultadosmenujson=[]
        print(resultadosmenu)
        for r in resultadosmenu: 
            resultadosmenujson.append({
                "id":r[0],
                "nombre":r[1],
                "precio":r[2],
                "restaurante":r[3],
            })
        print(resultadosmenujson)
        return render_template('agremenu.html',resultadosmenu=resultadosmenujson)

@app.route('/agreprod', methods = ['POST','GET'])
def agreprod():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        precio_producto = request.form['precio_producto']
        tipo_producto = request.form['tipo_producto']
        restaurante_producto = request.form['restaurante_producto']
        print(id_producto, precio_producto, tipo_producto, restaurante_producto)
        cur_01=conexion.cursor()
        insert_datos= "insert into producto (id_producto, precio_producto, tipo_producto, restaurante_producto) VALUES (:1, :2, :3, :4)"
        print(insert_datos)
        cur_01.execute(insert_datos,[id_producto, precio_producto, tipo_producto, restaurante_producto])
        conexion.commit()
        return render_template('agreprod.html')
    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_prod= "SELECT * FROM producto"
        cur_01.execute(select_prod)
        print(select_prod)
        resultadosprod=cur_01.fetchall()
        resultadosprodjson=[]
        print(resultadosprod)
        for r in resultadosprod: 
            resultadosprodjson.append({
                "id":r[0],
                "precio":r[1],
                "tipo":r[2],
                "restaurante":r[3],
            })
        print(resultadosprodjson)
        return render_template('agreprod.html',resultadosprod=resultadosprodjson)

@app.route('/agreing', methods = ['POST','GET'])
def agreing():
    if request.method == 'POST':
        id_ingrediente = request.form['id_ingrediente']
        precio_ingrediente = request.form['precio_ingrediente']
        restaurante_ingrediente = request.form['restaurante_ingrediente']
        print(id_ingrediente, precio_ingrediente, restaurante_ingrediente)
        cur_01=conexion.cursor()
        insert_datos= "insert into ingrediente (id_ingrediente, precio_ingrediente, restaurante_ingrediente) VALUES (:1, :2, :3)"
        print(insert_datos)
        cur_01.execute(insert_datos,[id_ingrediente, precio_ingrediente, restaurante_ingrediente])
        conexion.commit()
        return render_template('agreing.html')
    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_ing= "SELECT * FROM ingrediente"
        cur_01.execute(select_ing)
        print(select_ing)
        resultadosing=cur_01.fetchall()
        resultadosingjson=[]
        print(resultadosing)
        for r in resultadosing: 
            resultadosingjson.append({
                "id":r[0],
                "precio":r[1],
                "restaurante":r[2],
            })
        print(resultadosingjson)
        return render_template('agreing.html',resultadosing=resultadosingjson)


@app.route('/modmenu', methods = ['POST','GET'])
def modmenu():
    resultadosjson={
                    "Id":"id",
                    "Nombre":"nombre",
                    "Precio":"precio",
                    "Restaurante":"restaurante",        
                    }
    if request.method == 'POST':
        id = request.form['id_menu']
        nombre = request.form['nombre_menu']
        precio = request.form['precio_menu']
        restaurante = request.form['restaurante_menu']
        update_menu='UPDATE menu set '
        update_menu_bool=False
        update_menu_atributos=[]
        if nombre and nombre!='':
                update_menu_bool=True
                update_menu_atributos.append("nombre_menu='"+nombre+"'")
        if precio and precio!='':
                update_menu_bool=True
                update_menu_atributos.append("precio_menu='"+precio+"'")
        if restaurante and restaurante!='':
                update_menu_bool=True
                update_menu_atributos.append("restaurante_menu='"+restaurante+"'")
        cur_01=conexion.cursor()
        if update_menu_bool:
                update_menu=update_menu+','.join(update_menu_atributos)+" Where id_menu = '"+id+"'"
                print(update_menu)
                cur_01.execute(update_menu)
                conexion.commit()
        return render_template('modmenu.html',form=resultadosjson)
    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_menu= "SELECT * FROM menu"
        cur_01.execute(select_menu)
        print(select_menu)
        resultadosmenu=cur_01.fetchall()
        resultadosmenujson=[]
        print(resultadosmenu)
        for r in resultadosmenu: 
            resultadosmenujson.append({
                "id":r[0],
                "nombre":r[1],
                "precio":r[2],
                "restaurante":r[3],
            })
        print(resultadosmenujson)
        return render_template('modmenu.html',resultadosmenu=resultadosmenujson)

@app.route('/pizzamenu', methods = ['POST','GET'])
def pizzamenu():
    return render_template('pizzamenu.html')

@app.route('/pizzamenucarta', methods = ['POST','GET'])
def pizzamenucarta():
    return render_template('pizzamenucarta.html')

@app.route('/pizzamenucheck', methods = ['POST','GET'])
def pizzamenucheck():
    return render_template('pizzamenucheck.html')

@app.route('/pizzamenuorden', methods = ['POST','GET'])
def pizzamenuorden():
    return render_template('pizzamenuorden.html')   


if __name__ == '__main__':
    app.run(debug=True)