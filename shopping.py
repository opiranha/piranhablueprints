from flask import Flask, render_template,json,jsonify,request

import mysql.connector
import mysql.connector.pooling


app = Flask(__name__)




def renew_tables():
    p_table_new = "CREATE TABLE IF NOT EXISTS `shopping`.`productos` (`id` INT NOT NULL AUTO_INCREMENT,`nombre` VARCHAR(45) NULL ,`clasificacion` VARCHAR(45) NULL,`presentacion` VARCHAR(45) NULL,`marca` VARCHAR(45) NULL,`adicional` VARCHAR(300) NULL, `codigo` VARCHAR(45) NULL,`creado_por` VARCHAR(45) NULL,`time_stamp` TIMESTAMP(6) NULL DEFAULT NOW(6),PRIMARY KEY (`id`));"
    p_table_drop = "DROP TABLE IF EXISTS `shopping`.`productos`;"
    s_table_new = "CREATE TABLE `shopping`.`tiendas` (`id` INT NOT NULL AUTO_INCREMENT,`nombre` VARCHAR(45) NULL,`direccion` VARCHAR(45) NULL,`lat` VARCHAR(45) NULL,`lng` VARCHAR(45) NULL,`creado_por` VARCHAR(45) NULL,`time_stamp` TIMESTAMP(6) NULL DEFAULT NOW(6),PRIMARY KEY (`id`),UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC));"
    s_table_drop = "DROP TABLE IF EXISTS `shopping`.`tiendas`;"
    s_s_table_new = "CREATE TABLE `shopping`.`tiendas_scores` (`id` INT NOT NULL AUTO_INCREMENT,`tienda_id` INT NULL, `tienda_score1` INT NULL, `tienda_score2` INT NULL, `tienda_score3` INT NULL, `tienda_score4` INT NULL, `tienda_score5` INT NULL, `creado_por` VARCHAR(45) NULL, `time_stamp` TIMESTAMP(6) NULL DEFAULT NOW(6), PRIMARY KEY (`id`));"
    s_s_table_drop = "DROP TABLE IF EXISTS `shopping`.`tiendas_scores`;"
    s_d_table_new = "CREATE TABLE `shopping`.`tiendas_descripciones` ( `id` INT NOT NULL AUTO_INCREMENT, `creado_por` VARCHAR(45) NULL, `descripcion` VARCHAR(120) NULL, `time_stamp` TIMESTAMP(6) NULL DEFAULT NOW(6), PRIMARY KEY (`id`));"
    s_d_table_drop = "DROP TABLE IF EXISTS `shopping`.`tiendas_descripciones`;"
    r_table_new = "CREATE TABLE `shopping`.`precios` ( `id` INT NOT NULL AUTO_INCREMENT, `producto_id` INT NULL, `tienda_id` INT NULL, `es_promo` TINYINT(1) NULL, `expiracion` DATETIME(6) NULL, `time_stamp` TIMESTAMP(6) NULL DEFAULT NOW(6), PRIMARY KEY (`id`));"
    r_table_drop = "DROP TABLE IF EXISTS `shopping`.`precios`;"
    l_table_new = ""
    l_table_drop = ""
    l_i_table_new = ""
    l_i_table_drop = ""
    log_table_new = "CREATE TABLE `shopping`.`loggins` ( `id` INT NOT NULL AUTO_INCREMENT, `usuario` VARCHAR(45) NULL, `password` VARCHAR(45) NULL, `time_stamp` TIMESTAMP(6) NULL DEFAULT NOW(6), `grupo` INT NULL, PRIMARY KEY (`id`), UNIQUE INDEX `usuario_UNIQUE` (`usuario` ASC));"
    log_table_drop = "DROP TABLE IF EXISTS `shopping`.`loggins`;"
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        #renovar productos
        cursor.execute(p_table_drop)
        cursor.execute(p_table_new)
        #renovar tiendas
        cursor.execute(s_table_drop)
        cursor.execute(s_table_new)
        cursor.execute(s_s_table_drop)
        cursor.execute(s_s_table_new)
        cursor.execute(s_d_table_drop)
        cursor.execute(s_d_table_new)
        #renovar precios
        cursor.execute(r_table_drop)
        cursor.execute(r_table_new)
        #renovar listas
        #cursor.execute(l_table_drop)
        #cursor.execute(l_table_new)
        #cursor.execute(l_i_table_drop)
        #cursor.execute(l_i_table_new)
        #renovar loggins
        cursor.execute(log_table_drop)
        cursor.execute(log_table_new)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print("Error " + str(err))
        return False
    return True

dbconfig = {
    "database":"shopping",
    "user":"root",
    "password":"110042"
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)

def error_codes(function,desc,code):
    q = {}
    Data = []
    d = {}
    q['Funcion'] = function
    q['Code'] = code
    q['Descripcion'] = desc
    Data.append(q)
    d['Error'] = Data
    return jsonify(d)

def add_prod(user,nombre,clasificacion,presentacion,marca,adicional,codigo):
    try:
        cnx = cnxpool.get_connection()
        qry = ("INSERT INTO productos (nombre, clasificacion,presentacion,marca,adicional,codigo,creado_por) VALUES (%s,%s,%s,%s,%s,%s,%s);")
        data_to_send = (nombre,clasificacion,presentacion,marca,adicional,codigo,user)
        cursor = cnx.cursor()
        cursor.execute(qry,data_to_send)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print("Error " + str(err))
        return False



def productos(_ss):


    _user = _ss[0]
    _pass = _ss[1]
    #_unid = _ss[2]


    if(_ss[1]=="add"):
        if(add_prod("admin",_ss[2],_ss[3],_ss[4],_ss[5],_ss[6],_ss[7])):
            d = {}
            q = {}
            Data = []
            q['Nombre'] = _ss[2]
            q['Clasificacion'] = _ss[3]
            q['Presentacion'] = _ss[4]
            q['Marca'] = _ss[5]
            q['Informacion Adicional'] = _ss[6]
            q['Codigo'] = _ss[7]
            Data.append(q)
            d['Producto Agregado'] = Data
            return jsonify(d)
        else:
            return error_codes("Productos","Agregando producto","1")
    elif(_ss[1]=="get"):
        print "Se envio un producto."
        d = {}
        for i in range(0,15,1):
            q = {}
            Data = []
            q['Nombre'] = "producto_"+str(i)
            q['Marca'] = "Marca_"+str(i)
            q['Presentacion'] = "Presentacion_"+str(i)
            q['Descripcion'] = "descripcion_"+str(i)
            q['Codigo'] = "codigo_"+str(i)
            q['Precio_1'] = "precio_1_"+str(i)
            q['Precio_2'] = "precio_1_"+str(i)
            q['Tienda_1'] = "tienda_1_"+str(i)
            q['Tienda_2'] = "tienda_1_"+str(i)
            Data.append(q)
            d['Producto '+str(i)] = Data
        return jsonify(d)
    else:
        print "Opcion de producto no valida."
        return error_codes("Productos","Opcion no valida","0")


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/get',methods=['POST','GET'])
def function_creator():

    #print "Debug 1 = "+str(request.full_path)
    #print "Debug 2 = "+str(request.headers)
    #print "Debug 3 = "+str(request.args)
    #_usuario = request.args.get('user')
    #_pass = request.args.get('password')
    #_nombre = request.args.get('nombre')
    #_clasificacion = request.args.get('clasificacion')
    #_presentacion = request.args.get('presentacion')
    #_marca = request.args.get('marca')
    #_adicional = request.args.get('adicional')
    #_codigo = request.args.get('codigo')
    #if(_pass=="opira11!"):
    #    d = productos([_usuario,"add",_nombre,_clasificacion,_presentacion,_marca,_adicional,_codigo])
    #    return d


    _s = request.args.get('string')
    _ss = str(_s).split(":")
      #no hay swich mejorar con alguna funcion?
    if(_ss[0]=="producto"):
        print "Debug 1 = "+str(request.full_path)
        print "Debug 2 = "+str(request.headers)
        print "Debug 3 = "+str(request.args)
        d = productos(_ss)

    elif(_ss[0]=="tienda"):
        print "tienda solicitada"
    elif(_ss[0]=="lista"):
        print "lista solicitada"
    elif(_ss[0]=="precio"):
        print "precios solicitado"
    elif(_ss[0]=="articulo"):
        print "articulos solicitado"
    elif(_ss[0]=="renew"):
        #renew_tables()
        d = "Tablas reiniciadas"
    else:
        d = "Error"


    #try:
        #cnx = cnxpool.get_connection()
        #prepareqry = ("Algo")
        #data_to_send = ("algo","algo")
        #cursor = cnx.cursor()
        #cursor.execute(prepareqry,data_to_send)
        #rows = cursor.fetchall()
        #i = 0
        #q = {}
        #for row in rows:
        #    i=i+1
        #    print(str(row))
    #except mysql.connector.Error as err:
    #    print "algo salio mal "+err.message

    return d

if __name__ == '__main__':
    app.run(host='0.0.0.0')
