from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://onit_zadanie_3:1234@localhost:5432/onit_zadanie_3"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class DoctorsModel(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    second_name = db.Column(db.String())
    specialization = db.Column(db.String())
    salary = db.Column(db.Integer())
    birthday = db.Column(db.String())
    hospital_id = db.Column(db.Integer(), db.ForeignKey("hospitals.id"), nullable=False)


class HospitalsModel(db.Model):
    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    opening_date = db.Column(db.String())
    number_buildings = db.Column(db.String())


def add_data_doctors(first_name, second_name, specialization, salary, birthday, hospital_id):
    new_doctor = DoctorsModel(first_name=first_name, second_name=second_name, specialization=specialization, salary=salary, birthday=birthday, hospital_id=hospital_id)
    db.session.add(new_doctor)
    db.session.commit()


def add_data_hospitals(name, address, opening_date, number_buildings):
    new_hospital = HospitalsModel(name=name, address=address, opening_date=opening_date, number_buildings=number_buildings)
    db.session.add(new_hospital)
    db.session.commit()


@app.route('/', methods=['GET'])
@app.route('/main', methods=['GET'])
def start():
    return render_template('main.html')


@app.route('/delete_doctor_data/<id>')
def delete_doctor_data(id):
    doctor = DoctorsModel.query.filter_by(id=id).first()
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('doctors_manager'))


@app.route('/do_change_doctor_data/<id>', methods=['POST'])
def do_change_doctor_data(id):
    result = request.form.to_dict()
    doctor = DoctorsModel.query.filter_by(id=id).first()
    doctor.first_name = result['first_name']
    doctor.second_name = result['second_name']
    doctor.specialization = result['specialization']
    doctor.salary = result['salary']
    doctor.birthday = result['birthday']
    doctor.hospital_id = result['hospital_id']
    db.session.commit()
    return redirect(url_for('doctors_manager'))


@app.route('/change_doctor_data/<id>/<first_name>/<second_name>/<specialization>/<salary>/<birthday>', methods=['GET', 'POST'])
def change_doctor_data(id, first_name, second_name, specialization, salary, birthday):
    return render_template('change_data_doctors.html', hospital_id_list={'hospital_id_list': HospitalsModel.query.all()}, data={'id': id,
                                                             'first_name': first_name,
                                                             'second_name': second_name,
                                                             'specialization': specialization,
                                                             'salary': salary,
                                                             'birthday': birthday
                                                             })


@app.route('/doctors_add', methods=['POST'])
def doctors_add():
    add_data_doctors(**request.form.to_dict())
    return redirect(url_for('doctors_manager'))


@app.route('/doctors_operation', methods=['GET','POST'])
def doctors_operation():
    return render_template('add_data_doctors.html', hospital_id_list={'hospital_id_list': HospitalsModel.query.all()})


@app.route('/doctors_manager', methods=['GET', 'POST'])
def doctors_manager():
    all = DoctorsModel.query.all()
    if DoctorsModel.query.all():
        return render_template('doctors_operation.html', data=all)
    return render_template('doctors_operation.html', data='')


@app.route('/hospitals_manager', methods=['GET', 'POST'])
def hospitals_manager():
    all = HospitalsModel.query.all()
    if HospitalsModel.query.all():
        return render_template('hospitals_operation.html', data=all)
    return render_template('hospitals_operation.html', data='')


@app.route('/hospitals_operation', methods=['GET', 'POST'])
def hospitals_operation():
    return render_template('add_data_hospitals.html')


@app.route('/hospitals_add', methods=['POST'])
def hospitals_add():
    add_data_hospitals(**request.form.to_dict())
    return redirect(url_for('hospitals_manager'))


@app.route('/change_hospital_data/<id>/<name>/<adress>/<opening_date>/<number_buildings>', methods=['GET', 'POST'])
def change_hospital_data(id, name, adress, opening_date, number_buildings):
    return render_template('change_data_hospitals.html', data={'id': id,
                                                               'name': name,
                                                               'address': adress,
                                                               'opening_date': opening_date,
                                                               'number_buildings': number_buildings
                                                               })


@app.route('/do_change_hospital_data/<id>', methods=['POST'])
def do_change_hospital_data(id):
    result = request.form.to_dict()
    hospital = HospitalsModel.query.filter_by(id=id).first()
    hospital.name = result['name']
    hospital.adress = result['address']
    hospital.opening_date = result['opening_date']
    hospital.number_buildings = result['number_buildings']
    db.session.commit()
    return redirect(url_for('hospitals_manager'))


@app.route('/delete_hospital_data/<id>')
def delete_hsopital_data(id):
    hospital = HospitalsModel.query.filter_by(id=id).first()
    db.session.delete(hospital)
    db.session.commit()
    return redirect(url_for('hospitals_manager'))


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.form.to_dict().get('table_doctors'):
        return redirect(url_for('doctors_manager'))
    elif request.form.to_dict().get('table_hospitals'):
        return redirect(url_for('hospitals_manager'))
    elif request.form.to_dict().get('table_join'):
        return redirect((url_for('join_tables')))


@app.route('/join_tables', methods=['GET'])
def join_tables():
    result = db.session.query(DoctorsModel, HospitalsModel).join(DoctorsModel).all()
    return render_template('join_tables.html', data=result)


if __name__ == '__main__':
    app.run(debug=True)
