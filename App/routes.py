from App import app
from flask import render_template, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql as pys


#Estabelecendo um connection 
connection = pys.connect(db='health_card', user='root', password='')

#Instanciando um cursor
cursor = connection.cursor()

#--------------------------------------
#              Page INICIAL
#--------------------------------------
@app.route('/')
@app.route('/home')
def home_page():

    return render_template('home.html')

#----------------------------------------------------
#   Page das vacinas disponiveis e tbm para cadastrar 
#   a vacina para o user
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
#    cadastrar vacina no db vaccine_user 
#-----------------------------------------
@app.route('/insert', methods= ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        date = request.form['date']
        batch= request.form['batch']

        __dataform = (name, date, batch)

        # cursor.execute("INSERT INTO vaccine_user(name, datte, batch) VALUES(%s, %s, %s)", (name, date, batch))
        __query = "INSERT INTO vaccine_user(name, datte, batch) VALUES(%s, %s, %s)"
        
        cursor.execute(__query, __dataform)

        #Commit in db
        connection.commit()

        #redirect for page vaccine_show.html
        return redirect (url_for('show_page'))

#----------------------------------------
#           Exibir as vacinas do user
#----------------------------------------
@app.route('/show')
def show_page():

    #Select de dados()
    sql = "SELECT * FROM vaccine_user"
    cursor.execute(sql)

    query = cursor.fetchall()

    return render_template('vaccine_show.html', query=query) 

#-----------------------------------------
#  notification Exibi a cadastro de notificações       
#-----------------------------------------
@app.route('/notification')
def page_notification_method():

    sql_notif = "SELECT * FROM list_notification"
    cursor.execute(sql_notif)

    query_notif = cursor.fetchall()

    return render_template('register_notification.html', query=query_notif)

#------------------------------------------
#           Registrar um notificação            
#------------------------------------------
@app.route('/register_notification', methods = ['POST'])
def add_notification_method():

    if request.method == 'POST':

        email = request.form['email']
        date  = request.form['date']
        phone = request.form['phone']

        __query = "INSERT INTO list_notification(email, birth, phone) VALUES(%s, %s, %s)"
        __date = (email, date, phone)

        cursor.execute(__query, __date)
        connection.commit()

        return redirect(url_for('page_notification_method'))

#----------------------------------------------
#           Delete notification
#----------------------------------------------
@app.route('/delnotfication/<int:id>')
def __delnotification(id):

    __del_query = "DELETE FROM list_notification WHERE id=%s"

    cursor.execute(__del_query, id)
    connection.commit()

    return redirect(url_for('page_notification_method'))


#----------------------------------------------
#   Edit vaccine user
#----------------------------------------------
@app.route('/edit/<int:id>')
def edit_view(id):

    query = "SELECT * FROM vaccine_user WHERE id=%s"
    cursor.execute(query, id)

    row = cursor.fetchone()

    if row:
        return render_template('edit.html', row=row)


#-----------------------------------------------
#       Update vaccine user
#-----------------------------------------------
@app.route('/update', methods = ['GET', 'POST'])
def __update():

    if request.method == 'POST':

        name = request.form['name']  #name="name"  <- value
        date = request.form['date']  #name="date"  <- value
        batch=request.form['batch']  #name="batch" <- value
        _id  = request.form['id']    #name="id"    <- value

        # save edits
        sql_update = "UPDATE vaccine_user SET name=%s, datte=%s, batch=%s WHERE id=%s"
        _data = (name, date, batch, _id)  #Dados form name

        cursor.execute(sql_update, _data) #execute
        connection.commit()               #persistencia

        return redirect(url_for('show_page'))

#-------------------------------------------
#       delete vaccine user
#-------------------------------------------
@app.route('/delete/<int:id>')
def __delete(id):

    query_delete = "DELETE FROM vaccine_user WHERE id=%s"
    id_delete = id

    cursor.execute(query_delete, id_delete)
    connection.commit()

    return redirect(url_for('show_page'))

#-------------------------------------------
#       Adicionar vaccine EM CONSTRUÇÃO
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
#       register - page account 
#----------------------------------------
@app.route('/register')
def register_page():

    return render_template('account.html')

#-------- Action Register ---------------
@app.route('/action_register', methods=['POST'])
def __action_register():
     if request.method == 'POST':

        __name = request.form['name']
        __email= request.form['email']
        __password = request.form['password']

        password_hash = generate_password_hash(__password) #preciso testar

        __dataform = (__name, __email, password_hash)

        quey_user = "INSERT INTO user(name, email, password) VALUES(%s, %s, %s)"
        cursor.execute(quey_user, __dataform) 

        connection.commit() 

        return redirect(url_for('register_page'))


#----------------------------------------
#       login - Page account
#----------------------------------------
@app.route('/login')
def login_page():

    return render_template('account.html')

#------------ Action login --------------
@app.route('/action_login', methods=['POST'])
def __action_login():

    if request.method == 'POST':

            email_form = request.form['email']
            password_form =  request.form['password']

            __data_in= (email_form, password_form)

            __query_user = "SELECT * FROM user WHERE email=%s AND password=%s"

            results = cursor.execute(__query_user, __data_in)

            if check_password_hash(password_form, results[3]):  #Preciso testar
            # if results:
                return redirect(url_for('session_page'))
            else:
                return redirect(url_for('login_page'))


#----------------------------------------
#       Session user
#----------------------------------------
@app.route('/session')
def session_page():

    return render_template('session_user.html') 

