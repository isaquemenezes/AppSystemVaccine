from App import app
from flask import render_template, redirect, request, url_for
import pymysql as pys

#DataScience--------
import requests
import pandas as ps

#Estabelecendo um connection 
connection = pys.connect(db='health_card', user='root', password='')

#Instanciando um cursor
cursor = connection.cursor()

#Page INICIAL
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#----------------------------------------------------
#Page das vacinas disponiveis e tbm para cadastrar 
# a vacina para o user
#----------------------------------------------------
@app.route('/register-vaccine')
def vaccine_register_page():

    #Select de vacinas disponíveis para cadastrar
    sql = "SELECT * FROM vaccine_card"
    cursor.execute(sql)
    query = cursor.fetchall()
    list_vaccine = query
   
    return render_template('register_vaccine.html', vaccine=list_vaccine)


#-----------------------------------------
#  cadastrar vacina no db vaccine_user 
#-----------------------------------------
@app.route('/insert', methods= ['POST'])
def insert():
    if request.method == 'POST':

        name = request.form['name']
        date = request.form['date']
        batch= request.form['batch']

        cursor.execute("INSERT INTO vaccine_user(name, datte, batch) VALUES(%s, %s, %s)", (name, date, batch))
    
        #Commit in db
        connection.commit()

        #redirect for page vaccine_show.html
        return redirect (url_for('show_page'))

#----------------------------------------
# Exibir as vacinas do user
#----------------------------------------
@app.route('/show')
def show_page():

    #Select de dados()
    sql = "SELECT * FROM vaccine_user"
    cursor.execute(sql)
    query = cursor.fetchall()

    return render_template('vaccine_show.html', query=query) 

#------------------------------------------
#Page notification
#-----------------------------------------
@app.route('/notification')
def add_notification_page():

    sql_notif = "SELECT * FROM list_notification"
    cursor.execute(sql_notif)
    query_notif = cursor.fetchall()

    return render_template('register_notification.html', query=query_notif)

#-------------------------------------------------------
#Registrar um notificação
#-------------------------------------------------------
@app.route('/register_notification', methods = ['POST'])
def add_notification():

    if request.method == 'POST':

        email = request.form['email']
        date  = request.form['date']
        phone = request.form['phone']

        __query = "INSERT INTO list_notification(email, birth, phone) VALUES(%s, %s, %s)"
        __date = (email, date, phone)

        cursor.execute(__query, __date)

        connection.commit()

        return redirect(url_for('add_notification_page'))

#-----------------------------------------------------
#Edit
#-----------------------------------------------------
@app.route('/edit/<int:id>')
def edit_view(id):
    query = "SELECT * FROM vaccine_user WHERE id=%s"

    cursor.execute(query, id)

    row = cursor.fetchone()

    if row:
        return render_template('edit.html', row=row)


#-----------------------------------------------
#Update
#-----------------------------------------------
@app.route('/update', methods = ['GET', 'POST'])
def __update():

    if request.method == 'POST':

        name = request.form['name']
        date = request.form['date']
        batch=request.form['batch']
        _id  = request.form['id']

        # save edits
        sql_update = "UPDATE vaccine_user SET name=%s, datte=%s, batch=%s WHERE id=%s"
        _data = (name, date, batch, _id) #Dados form name

        cursor.execute(sql_update, _data) #execute

        connection.commit() #persistencia

        return redirect(url_for('show_page'))

#-------------------------------------------
#delete
#-------------------------------------------
@app.route('/delete/<int:id>')
def __delete(id):
    query_delete = "DELETE FROM vaccine_user WHERE id=%s"
    id_delete = id

    cursor.execute(query_delete, id_delete)
    connection.commit()

    return redirect(url_for('show_page'))

#-------------------------------------------
#Adicionar vaccine EM CONSTRUÇÃO
#-------------------------------------------
@app.route('/addvaccine/<int:id>')
def add_vaccine(id):

    return render_template('add_vaccine.html')




#----------------------------------------
#    Information das vacinas disponíveis
#---------------------------------------
@app.route('/info')
def __info():
    return render_template('single.html')

#----------------------------------------
#Page register
@app.route('/register')
def register_page():
    return render_template('register.html')

#----------------------------------------
#Page login
@app.route('/login')
def login_page():
    return render_template('login.html')

#----------------------------------------
#Session user
@app.route('/session', methods=['GET', 'POST'] )
def session_page():
    return render_template('session_user.html') 

#----------------------------------------------------
#------------- Testes analise de dados --------------
#----------------------------------------------------

#Rotas
@app.route('/data_science')
def __data_science():
    csv_file = 'Acara_covid-19.csv'
    file = requests.get(csv_file)
    
    data_set = ps.read_csv(file)
    _data = {}  # Criando um dic vazio
    _data['dados'] = data_set.head().to_html() #Exportando pra html

    return render_template('dataScience.htm', dados=_data)
