from flask import  Flask, render_template, abort, request, redirect
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import sqlite3
import os

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

conn = sqlite3.connect("productos_test.db")
cursor= conn.cursor()
#cursor.execute('Create table productos (id int,descripcion text, precio real,imagen text)')
#cursor.execute('insert into productos values(1,"Playstation 4",18000,"ps4.jpg")')
#cursor.execute('insert into productos values(2,"Xbox One Controller",2800,"xbox.jpeg")')
#cursor.execute('insert into productos values(3,"God of War Ps4",2000,"gow.jpeg")')
#cursor.execute("delete from productos")
#conn.commit()


def cconsultar():
    conn = sqlite3.connect("productos_test.db")
    cursor= conn.cursor()
    campos=["id","description","price","imageUrl"]
    producticos=[]
    for producto in cursor.execute("select * from productos").fetchall():
        dicc=dict()
        for x in range(4):
            dicc[campos[x]]=producto[x]
        producticos.append(dicc)
    conn.close()
    return producticos

def insertar(dato):
    conn = sqlite3.connect("productos_test.db")
    cursor= conn.cursor()
    valores=(dato["id"],dato["description"],dato["price"],dato["imageUrl"])
    cursor.execute("insert into productos values (?,?,?,?)",valores)
    conn.commit()
    conn.close()

def update(dato):
    conn = sqlite3.connect("productos_test.db")
    cursor= conn.cursor()
    valores=(dato["description"],dato["price"],dato["imageUrl"],dato["id"])
    cursor.execute("update productos set descripcion=?,precio=?,imagen=? where id=?",valores)
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect("productos_test.db")
    cursor= conn.cursor()
    print(id)
    cursor.execute("delete from productos where id=?",(int(id),))
    conn.commit()
    conn.close()







app = Flask(__name__, static_url_path='',static_folder='C:\\Users\\roh_9\\Documents\\pywebdemo-master') #Modificar acorde


products=cconsultar()
filteredProducts = products


@app.route("/")
def home():
    return render_template("home.html",products = filteredProducts, pageTitle="Game Store")

@app.route("/product/<int:id>")
def getProductById(id):
    global products
    for product in products:
        if (int(product["id"]) == id):
            return render_template("productdetail.html", product = product)
    return abort(404)

@app.route("/delete/<int:id>")
def deleteProduct(id):
    global products
    global filteredProducts
    delete(id)
    filteredProducts=cconsultar()
    products=cconsultar()
    return redirect("/")

@app.route("/findProducts", methods=['POST'])
def findProducts():
    global filteredProducts
    filteredProducts = []
    dato = request.form["filtertext"]
    print(dato)
    for p in products:
        if ( dato in p["description"]  ):
        # if (p["description"].startswith(dato)):
            print(p['description'])
            filteredProducts.append(p)
    return redirect("/")


@app.route("/form/", methods=["GET","POST"], defaults={"id":0})
@app.route("/form/<int:id>", methods=["GET","POST"])
def createOrEditProduct(id):
    if len(request.form)==0 :
        if id==0:
            return render_template("productForm.html", product={"id":len(products)+1})
        else:
            return render_template("productForm.html",product =products[id -1])
    else:
        if id==0:
            products.append(dict())
            index=len(products)-1
            flag=1
        else:
            index=int(id)-1
            flag=0
        for key in request.form.keys():
            products[index][key]=request.form[key]
        file=request.files['imageUrl']
        products[index]['imageUrl']=file.filename
        file=request.files['imageUrl']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path, 'static\\img\\'+filename))
        if flag:
            insertar(products[index])
        else:
            update(products[index])
        filteredProducts=products
        return render_template("home.html",products = filteredProducts, pageTitle="Game Store")
if __name__ == "__main__":
    app.run(debug=True)