from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow

from flask_jwt_extended import JWTManager, jwt_required, create_access_token
'''
from flask_mail import Mail, Message
'''

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'startup_details.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL
'''
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
'''

db = SQLAlchemy(app)
ma = Marshmallow(app)

jwt = JWTManager(app)
'''
mail = Mail(app)
'''

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    t_start1 = sDetails(strtup_name='Aria Travel',
                      foundr_name='Aashay',
                      cofoundr_name='Aakarsh',
                      amnt_raised=12365.12,
                      amnt_needed=250000.54,
                      no_of_members=3,
                      eqty_prop=234.23,
                      dt_establish=20092020,
                      approved=True,
                      role='founder','''
                      strtup_logo='image',
                      business_model= 'travel is life',
                      business_desc= 'travel made easy',
                      '''invested_companies='tech',
                      list_of_companies='tech1',
                      # kyc upload files
                      Adhar_card_front='adharfront',
                      Adhar_card_back='adharback',
                      pan='pan card',
                      bank_Statement='bank statement'
                      
                      inv_note= 'the next big thing',
                      balanc_sheet= 'upload file',
                      fin_details= 'upload file',
                      inv_pitch= 'upload file'
                      )

    db.session.add(t_start1)

    test_user = User(founder_first_name = 'Aashay',
                     founder_last_name = 'Kapoor',
                     phone = 23984738,
                     email = 'appdeveloper@email.com',
                     password = 'aashaykap')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Investry API.'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/age_verify/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


@app.route('/investors_details', methods=['GET'])
def investors_details():
    inv_list = sDetails.query.all()
    result = starts_schema.dump(inv_list)
    return jsonify(result.data)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test1 = User.query.filter_by(email=email).first()
    phone = request.form['phone']
    test2 = User.query.filter_by(phone=phone).first()
    if test1:
        return jsonify(message='That email already exists.'), 409
    if test2:
        return jsonify(message='That phone already exists.'), 409
    if test1 and test2:
        return jsonify(message='phone and email already exists.'), 409
    
    else:
        founder_first_name = request.form['founder_first_name']
        founder_last_name = request.form['founder_last_name']
        password = request.form['password']
        startup = User(founder_first_name=founder_first_name, founder_last_name=founder_last_name,phone=phone, email=email,
                        password=password)
        db.session.add(startup)
        db.session.commit()
        return jsonify(message="User created successfully."), 201


'''
@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401
'''

'''
@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    startup = User.query.filter_by(email=email).first()
    if startup:
        msg = Message("your investry API password is " + startup.password,
                      sender="admin@investry-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist"), 401

'''
#read

@app.route('/Inv_details/<int:strtup_id>', methods=["GET"])
def inv_details(strtup_id: int):
    startup_dtl = sDetails.query.filter_by(strtup_id=strtup_id).first()
    if startup_dtl:
        result = start_schema.dump(startup_dtl)
        return jsonify(result.data)
    else:
        return jsonify(message="That startup_dtl does not exist"), 404
'''
#create

@app.route('/add_startup', methods=['POST'])
@jwt_required
def add_startup():
    strtup_name = request.form['strtup_name']
    test = sDetails.query.filter_by(strtup_name=strtup_name).first()
    if test:
        return jsonify("There is already a startup_dtl by that name"), 409
    else:
        foundr_name = request.form['foundr_name']
        strtup_name = request.form['strtup_name']
        role = request.form['role']
        business_model = float(request.form['business_model'])
        amnt_raised = float(request.form['amnt_raised'])
        no_of_members = int(request.form['no_of_members'])
        # eqty_prop=float['eqty_prop']
        # upload
        strtup_logo = request.form['strtup_logo']
        # invested_companies = request.form['invested_companies']
        # list_of_companies = request.form['list_of_companies']
        # kyc upload files
        Adhar_card_front = request.form['Adhar_card_front']
        Adhar_card_back = request.form['Adhar_card_back']
        pan = request.form['pan']
        bank_statement = request.form['bank_Statement']

        new_start = sDetails(strtup_name=strtup_name,
                           foundr_name=foundr_name,
                           role=role,
                           business_model=business_model,
                           amnt_raised=amnt_raised,
                           # no_of_members=no_of_members,
                           # eqty_prop=eqty_prop,
                           strtup_logo=strtup_logo,
                           # table of companies investes
                           # invested_companies = invested_companies,
                           # list_of_companies = list_of_companies,
                           # kyc upload files
                           Adhar_card_front=Adhar_card_front,
                           Adhar_card_back=Adhar_card_back,
                           pan=pan,
                           bank_statement=bank_statement

                           )

        db.session.add(new_start)
        db.session.commit()
        return jsonify(message="You added a startup_dtl"), 201
'''
#update
'''
@app.route('/update_startups', methods=['PUT'])
@jwt_required
def update_startups():
    strtup_id = int(request.form['strtup_id'])
    startup_dtl = sDetails.query.filter_by(strtup_id=strtup_id).first()
    if startup_dtl:
        startup_dtl.strtup_name = request.form['strtup_name']
        startup_dtl.foundr_name = request.form['foundr_name']
        startup_dtl.role = request.form['role']
        startup_dtl.business_model = float(request.form['business_model'])
        startup_dtl.amnt_raised = float(request.form['amnt_raised'])
        startup_dtl.strtup_id = int(request.form['no_of_members '])
        startup_dtl.business_model = float['eqty_prop = Column(Float)']
        startup_dtl.role = request.form['role']
        # upload
        startup_dtl.strtup_logo = request.form['strtup_logo']
        startup_dtl.business_model = request.form['business_model']
        startup_dtl.invested_companies = request.form['invested_companies']
        startup_dtl.list_of_companies = request.form['list_of_companies']
        # kyc upload files
        startup_dtl.Adhar_card_front = request.form['Adhar_card_front']
        startup_dtl.Adhar_card_back = request.form['Adhar_card_back']
        startup_dtl.pan = request.form['pan']
        startup_dtl.bank_Statement = request.form['bank_Statement']

        db.session.commit()
        return jsonify(message="You updated a startup_dtl"), 202
    else:
        return jsonify(message="That startup_dtl does not exist"), 404
'''

'''
#delete

@app.route('/remove_investors_details/<int:strtup_id>', methods=['DELETE'])
@jwt_required
def remove_idetails(strtup_id: int):
    startup_dtl = sDetails.query.filter_by(strtup_id=strtup_id).first()
    if startup_dtl:
        db.session.delete(startup_dtl)
        db.session.commit()
        return jsonify(message="You deleted a startup_dtl"), 202
    else:
        return jsonify(message="That startup_dtl does not exist"), 404

'''

# database models
class User(db.Model):
    __tablename__ = 'investor_u'
    id = Column(Integer, primary_key=True)
    founder_first_name = Column(String)
    founder_last_name = Column(String)
    phone = Column(Float, unique=True)
    email = Column(String, unique=True)
    password = Column(String)


class sDetails(db.Model):
    __tablename__ = 'investor_details'
    strtup_id = Column(Integer, primary_key=True)
    strtup_name = Column(String)
    foundr_name = Column(String)
    cofoundr_name = Column(String)
    amnt_raised = Column(Float)
    amnt_needed = Column(Float)
    no_of_members = Column(Integer)
    eqty_prop = Column(Float)
    dt_establish = Column(Float)
    approved = Column(Boolean, default=False)

    role = Column(String)
    #file upload
    strtup_logo = Column(String)
    business_model = Column(String)
    business_desc = Column(String)
    inv_note = Column(String)
    invested_companies = Column(String)
    list_of_companies = Column(String)
    # kyc upload files
    Adhar_card_front = Column(String)
    Adhar_card_back = Column(String)
    pan = Column(String)
    bank_Statement = Column(String)
    balnc_sheet = Column(String)
    fin_details = Column(String)
    inv_pitch = Column(String)



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'founder_first_name', 'founder_last_name', 'phone', 'email', 'password')

'''
class StartSchema(ma.Schema):
    class Meta:
        fields = ('strtup_id', 'strtup_name', 'foundr_name', 'cofoundr_name', 'amnt_raised', 'amnt_needed', 'no_of_members', 'eqty_prop', 'dt_establish', 'strtup_logo', 'approved',
        'business_model', 'business_desc', 'inv_note', 'balnc_sheet', 'fin_details', 'inv_pitch'
                  )
'''
class StartSchema(ma.Schema):
    class Meta:
        fields = ('strtup_id', 'strtup_name', 'foundr_name', 'amnt_raised', 'amnt_needed', 'no_of_members', 'eqty_prop', 'deleteline',
                   'role', 'strtup_logo', 'business_model', 'invested_companies', 'list_of_companies', 'Adhar_card_front',
                  'Adhar_card_back',
                  'pan', 'bank_Statement'
                  )


user_schema = UserSchema()
users_schema = UserSchema(many=True)

start_schema = StartSchema()
starts_schema = StartSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)
