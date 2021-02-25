from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
'''
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
'''

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'startup_details.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL

app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
'''

db = SQLAlchemy(app)
ma = Marshmallow(app)
'''
jwt = JWTManager(app)
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
    t_start1 = iDetails(strtup_name='human',
                      foundr_name='tech',
                      amnt_raised=12365.12,
                      no_of_members=3,
                      eqty_prop=234.23,
                      interested_investing='something',
                      role='founder',
                      strtup_logo='image',
                      invested_companies='tech',
                      list_of_companies='tech1',
                      # kyc upload files
                      Adhar_card_front='adharfront',
                      Adhar_card_back='adharback',
                      pan='pan card',
                      bank_Statement='bank statement'
                      )

    db.session.add(t_start1)

    test_user = User(founder_first_name = 'manoj',
                     founder_last_name = 'bhaiya',
                     phone = 23984738,
                     email = 'email@email.com',
                     password = 'ashishj')

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
    inv_list = iDetails.query.all()
    result = invs_schema.dump(inv_list)
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
    investor_dtl = iDetails.query.filter_by(strtup_id=strtup_id).first()
    if investor_dtl:
        result = inv_schema.dump(investor_dtl)
        return jsonify(result.data)
    else:
        return jsonify(message="That investor_dtl does not exist"), 404
'''
#create

@app.route('/add_investor', methods=['POST'])
@jwt_required
def add_investor():
    strtup_name = request.form['strtup_name']
    test = iDetails.query.filter_by(strtup_name=strtup_name).first()
    if test:
        return jsonify("There is already a investor_dtl by that name"), 409
    else:
        foundr_name = request.form['foundr_name']
        strtup_name = request.form['strtup_name']
        role = request.form['role']
        business_model = float(request.form['business_model'])
        amnt_raised = float(request.form['amnt_raised'])
        no_of_members = int(request.form['no_of_members'])
        # eqty_prop=float['eqty_prop']
        # interested_investing = request.form['interested_investing']
        # upload
        strtup_logo = request.form['strtup_logo']
        # invested_companies = request.form['invested_companies']
        # list_of_companies = request.form['list_of_companies']
        # kyc upload files
        Adhar_card_front = request.form['Adhar_card_front']
        Adhar_card_back = request.form['Adhar_card_back']
        pan = request.form['pan']
        bank_statement = request.form['bank_Statement']

        new_inv = iDetails(strtup_name=strtup_name,
                           foundr_name=foundr_name,
                           role=role,
                           business_model=business_model,
                           amnt_raised=amnt_raised,
                           # no_of_members=no_of_members,
                           # eqty_prop=eqty_prop,
                           interested_investing='tech and healthcare',
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

        db.session.add(new_inv)
        db.session.commit()
        return jsonify(message="You added a investor_dtl"), 201
'''
#update
'''
@app.route('/update_investors', methods=['PUT'])
@jwt_required
def update_investors():
    strtup_id = int(request.form['strtup_id'])
    investor_dtl = iDetails.query.filter_by(strtup_id=strtup_id).first()
    if investor_dtl:
        investor_dtl.strtup_name = request.form['strtup_name']
        investor_dtl.foundr_name = request.form['foundr_name']
        investor_dtl.role = request.form['role']
        investor_dtl.business_model = float(request.form['business_model'])
        investor_dtl.radius = float(request.form['radius'])
        investor_dtl.distance = float(request.form['distance'])
        investor_dtl.amnt_raised = float(request.form['amnt_raised'])
        investor_dtl.strtup_id = int(request.form['no_of_members '])
        investor_dtl.business_model = float['eqty_prop = Column(Float)']
        investor_dtl.interested_investing = request.form['interested_investing']
        investor_dtl.role = request.form['role']
        # upload
        investor_dtl.strtup_logo = request.form['strtup_logo']
        investor_dtl.business_model = request.form['business_model']
        investor_dtl.invested_companies = request.form['invested_companies']
        investor_dtl.list_of_companies = request.form['list_of_companies']
        # kyc upload files
        investor_dtl.Adhar_card_front = request.form['Adhar_card_front']
        investor_dtl.Adhar_card_back = request.form['Adhar_card_back']
        investor_dtl.pan = request.form['pan']
        investor_dtl.bank_Statement = request.form['bank_Statement']

        db.session.commit()
        return jsonify(message="You updated a investor_dtl"), 202
    else:
        return jsonify(message="That investor_dtl does not exist"), 404
'''

'''
#delete

@app.route('/remove_investors_details/<int:strtup_id>', methods=['DELETE'])
@jwt_required
def remove_idetails(strtup_id: int):
    investor_dtl = iDetails.query.filter_by(strtup_id=strtup_id).first()
    if investor_dtl:
        db.session.delete(investor_dtl)
        db.session.commit()
        return jsonify(message="You deleted a investor_dtl"), 202
    else:
        return jsonify(message="That investor_dtl does not exist"), 404

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


class iDetails(db.Model):
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
    '''interested_investing = Column(String)
    role = Column(String)'''
    #file upload
    strtup_logo = Column(String)
    business_model = Column(String)
    business_desc = Column(String)
    inv_note = Column(String)
    '''invested_companies = Column(String)
    list_of_companies = Column(String)
    # kyc upload files
    Adhar_card_front = Column(String)
    Adhar_card_back = Column(String)
    pan = Column(String)
    bank_Statement = Column(String)'''
    balnc_sheet = Column(String)
    fin_details = Column(String)
    inv_pitch = Column(String)



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'founder_first_name', 'founder_last_name', 'phone', 'email', 'password')


class InvSchema(ma.Schema):
    class Meta:
        fields = ('strtup_id', 'strtup_name', 'foundr_name', 'cofoundr_name', 'amnt_raised', 'amnt_needed', 'no_of_members', 'eqty_prop', 'dt_establish', 'strtup_logo', 'approved',
        'business_model', 'business_desc', 'inv_note', 'balnc_sheet', 'fin_details', 'inv_pitch'
                  )
'''
class InvSchema(ma.Schema):
    class Meta:
        fields = ('strtup_id', 'strtup_name', 'foundr_name', 'amnt_raised', 'amnt_needed', 'no_of_members', 'eqty_prop', 'interested_investing',
                   'role', 'strtup_logo', 'business_model', 'invested_companies', 'list_of_companies', 'Adhar_card_front',
                  'Adhar_card_back',
                  'pan', 'bank_Statement'
                  )
'''
user_schema = UserSchema()
users_schema = UserSchema(many=True)

inv_schema = InvSchema()
invs_schema = InvSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)
