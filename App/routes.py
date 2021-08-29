from App import app
from flask import render_template, redirect, request, url_for, flash
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

#--------------------------------------
#               Page ERROR
#--------------------------------------
@app.route('/error')
def error_method():

    return render_template('error_page.html')

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


#----------------- UPDATE ACTION --------------- 
@app.route('/update', methods = ['GET', 'POST'])
def __update():

    if request.method == 'POST':

        name = request.form['name']  #name="name"  <- value
        date = request.form['date']  #name="date"  <- value
        batch= request.form['batch']  #name="batch" <- value
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
#       Add vaccine 2 option
#-------------------------------------------
@app.route('/add_vaccine/<int:id>')
def add_vaccine(id):

    __id = id
    __query_select = 'SELECT * FROM vaccine_card WHERE id=%s'

    cursor.execute( __query_select, __id)

    results = cursor.fetchone()

    if results:
        return render_template('add_vaccine.html', rows=results)

#---------------- ACTION  ADD VACCINE ------------
@app.route('/addvaccine', methods=['GET', 'POST'])
def __add_vaccine():

    if request.method == 'POST':

        __name_form = request.form.get('name')
        __date_form = request.form.get('date')
        __batch_form= request.form.get('batch')

        date_form =(__name_form, __date_form, __batch_form)

        __query_insert = 'INSERT INTO vaccine_user(name, datte, batch) VALUES(%s, %s, %s)'

        cursor.execute(__query_insert, date_form)

        connection.commit()

        return redirect( url_for('show_page') )

    return render_template('add_vaccine.html')
    


#----------------------------------------
#       page account 
#----------------------------------------
@app.route('/account')
def __account():

    return render_template('account.html')

#-------------- REGISTER -----------------------
@app.route('/register', methods=['GET', 'POST'])
def __action_register():

    if request.method == 'POST':

        name_form = request.form.get('name')
        email_form = request.form.get('email')
        password_form = request.form.get('password')

        password_hash = generate_password_hash(password_form)

        # user_data = (form.username.data, form.email.data, form.password.data)
        user_data = (name_form, email_form, password_hash)

        _user = "INSERT INTO user(name, email, password) VALUES(%s, %s, %s)"

        cursor.execute(_user, user_data)

        connection.commit()

        flash('Thanks for registering')

        return redirect(url_for('__account'))

    return render_template('account.html')


#------------------- LOGIN ---------------------
@app.route('/login', methods = ['GET', 'POST'])
def __action_login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        error = None

        query_user = 'SELECT * FROM user WHERE email=%s'

        cursor.execute(query_user, (email))

        results =  cursor.fetchone()

        if results is None:
            error = 'Incorrect username.'
        elif not check_password_hash(results[3], password):
            error = 'Incorrect password.'

        if error is None:

            return redirect(url_for('session_page'))

        flash(error)
    
    return redirect(url_for('error_method'))


#----------------------------------------
#       Session user
#----------------------------------------
@app.route('/session')
def session_page():

    return render_template('session_user.html') 

