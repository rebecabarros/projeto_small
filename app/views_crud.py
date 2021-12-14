from app import app
import psycopg2 as psy
from flask import redirect, url_for, render_template, flash, request
from app.forms import GravadoraForm

def conexao():
    try:
        conn = psy.connect(dbname = 'bd_pratica', user='postgres', 
        password='postgres')
    except (Exception, psy.Error) as error :
        print ("Erro na tentativa de conexão", error)
    return conn


@app.route("/gravadora", methods=['GET', 'POST'])
def gravadora():
    try:
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gravadora;")
        result = cursor.fetchall()      
    except (Exception, psy.Error) as error :
        print ("Erro na tentativa de commit", error)

    form = GravadoraForm()
    if form.validate_on_submit():
        nome = form.nome.data
        endereco = form.endereco.data
        telefone = form.telefone.data
        site = form.site.data
        contato = form.contato.data
        cursor.execute("INSERT INTO gravadora (idgravadora, nome, endereco, \
        telefone, site, contato) VALUES (default, %s, %s, %s, %s, %s)", 
        (nome, endereco, telefone, site, contato))
        conn.commit()
        if (cursor.rowcount > 0):
            flash('Gravadora inserida!')
        return redirect(url_for("gravadora"))

    if(conn):
        cursor.close()
        conn.close()
    
    return render_template("gravadora.html", form = form, result=result)  

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    form = GravadoraForm()
    try: 
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gravadora where idgravadora = %s", (id,))
        result = cursor.fetchone()
        cursor.execute("SELECT * FROM gravadora;")
        todos = cursor.fetchall()
    except (Exception, psy.Error) as error :
        print ("Erro na tentativa de commit", error)

    if request.method == 'GET':
        form.nome.data = result[1]
        form.endereco.data = result[2]
        form.telefone.data = result[3]
        form.site.data = result[4]
        form.contato.data = result[5]

    if form.validate_on_submit():
        nome = form.nome.data
        endereco = form.endereco.data
        telefone = form.telefone.data
        site = form.site.data
        contato = form.contato.data
        cursor.execute("UPDATE gravadora set nome = %s, endereco = %s, \
        telefone = %s, site = %s, contato = %s where idgravadora = %s",
        (nome, endereco, telefone, site, contato, id))
        conn.commit()
        if (cursor.rowcount > 0):
            flash('Gravadora atualizada!')
        return redirect(url_for("gravadora"))
    if(conn):
        cursor.close()
        conn.close()
    return render_template("gravadora.html", form=form, result=todos)

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    try: 
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute("DELETE from gravadora where idgravadora = %s", (id,))
        conn.commit()
        if (cursor.rowcount == 1):
            flash("Gravadora deletada")
        return redirect(url_for("gravadora"))
    except (Exception, psy.Error) as error :
        print ("Erro na tentativa de commit", error)

