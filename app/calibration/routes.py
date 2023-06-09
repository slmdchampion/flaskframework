from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, request, redirect, url_for, render_template_string,flash
from flask_security import (
    login_required
)
from sqlalchemy import cast

from app.database.base import sa
from app.database.calibration import (Gauges,
                                      Gauge_types,
                                      Calibration_certificates,
                                      Calibration_references,
                                      Gauge_owners,
                                      Gauge_status,
                                      Uncertainties
)
from app.calibration.forms import (LeadStandardCalibrationForm, 
                                   EditCalibrationReferencesForm, 
                                   ListGaugeTypesForm, 
                                   EditGaugeTypesForm, AddGaugeTypesForm, EditUncertaintiesForm)

index_blueprint = Blueprint('index', __name__, template_folder='templates', static_folder='static')
calibration_blueprint = Blueprint('calibration', __name__, template_folder='templates', static_folder='static', url_prefix='/calibration')

@index_blueprint.route("/")
@calibration_blueprint.route("/")
@calibration_blueprint.route("/index")
def index():
    duedate = datetime.today() + timedelta(days=30)
    gaugesdue = sa.session.scalars(sa.select(Gauges).where(Gauges.calibration_due<duedate, 
        Gauges.gauge_status==1).order_by(Gauges.calibration_due)).all()
    
    return render_template('index.html', title='Home', table_data=gaugesdue)

@calibration_blueprint.route('listgaugetypes', methods=['POST', 'GET'])
def listgaugetypes():
    form = ListGaugeTypesForm()
    if request.method == 'GET':
        # gauge_types = sa.session.scalars(sa.select(Gauge_types)).all()
        gauge_types = sa.session.execute(sa.select(Gauge_types,Uncertainties).join(Uncertainties, Gauge_types.id==Uncertainties.gauge_type, isouter=True).order_by(Gauge_types.id)).all()
        return render_template('listgaugetypes.html', form=form, table_data=gauge_types, 
                               title='Gauge Types', action=url_for('calibration.listgaugetypes'))
    if form.validate_on_submit():
        gaugetype_id = request.form.get('edit_id')
        return redirect(url_for('calibration.addcalibrationreference', gauge_type_id=gaugetype_id))
    
@calibration_blueprint.route('editgaugetype', methods=['POST', 'GET'])
def editgaugetype():
    form = EditGaugeTypesForm()
    if request.method == 'GET':
        gaugetype_id = request.args.get('id')
        gaugetype_data = sa.get_or_404(Gauge_types, gaugetype_id)
        return render_template('editgaugetype.html', form=form, form_data=gaugetype_data, action=url_for('calibration.editgaugetype'), 
                               title='Edit Gauge Type')
    if form.validate_on_submit():
        gaugetype_data = sa.get_or_404(Gauge_types, form.id.data)
        gaugetype_data.description=form.description.data
        gaugetype_data.calibration_reference=form.calibration_reference.data
        gaugetype_data.calibration_link=form.calibration_link.data
        sa.session.commit()
        return redirect(url_for('calibration.listgaugetypes'))
    
@calibration_blueprint.route('adduncertainty', methods=['POST', 'GET'])
def adduncertainty():
    form = EditUncertaintiesForm()
    if request.method == 'GET':
        gaugetype_id = request.args.get('id')
        gauge_types = [(row.id,row.description) for row in sa.session.scalars(sa.select(Gauge_types)).all()]
        form.gauge_type.choices = gauge_types
        form.gauge_type.data = gaugetype_id
        return render_template('edituncertainty.html', form=form, form_data={'id':'0','description':'','calibration_reference':'','calibration_link':''}, 
                               action=url_for('calibration.adduncertainty'), title='Add Uncertainty')
    if form.validate_on_submit():
        uncertainty_data = Uncertainties(process=form.process_field.data, gauge_type=form.gauge_type.data, uncertainty=form.uncertainty.data)
        sa.session.add(uncertainty_data)
        sa.session.commit()
        flash('Uncertainty Added...')
        return redirect(url_for('calibration.listgaugetypes'))

@calibration_blueprint.route('edituncertainty', methods=['POST', 'GET'])
def edituncertainty():
    form = EditUncertaintiesForm()
    if request.method == 'GET':
        uncertainty_id = request.args.get('id')
        uncertainty_data = sa.get_or_404(Uncertainties, uncertainty_id)
        gauge_types = [(row.id,row.description) for row in sa.session.scalars(sa.select(Gauge_types)).all()]
        form.gauge_type.choices = gauge_types
        form.gauge_type.data = uncertainty_data.gauge_type
        return render_template('edituncertainty.html', form=form, form_data=uncertainty_data, 
                               action=url_for('calibration.edituncertainty'), title='Edit Uncertainty')
    if form.validate_on_submit():
        uncertainty_data = sa.get_or_404(Uncertainties, form.id.data)
        uncertainty_data.process=form.process_field.data
        uncertainty_data.gauge_type=form.gauge_type.data
        uncertainty_data.uncertainty=form.uncertainty.data
        sa.session.commit()
        flash('Uncertainty Modified...')
        return redirect(url_for('calibration.listgaugetypes'))
    
@calibration_blueprint.route('addgaugetype', methods=['POST', 'GET'])
def addgaugetype():
    form = AddGaugeTypesForm()
    if request.method == 'GET':
        # gaugetype_id = request.args.get('id')
        # gaugetype_data = sa.get_or_404(Gauge_types, gaugetype_id)
        return render_template('editgaugetype.html', form=form, form_data={'id':'0','description':'','calibration_reference':'','calibration_link':''}, 
                               action=url_for('calibration.addgaugetype'), title='Add Gauge Type')
    if form.validate_on_submit():
        gaugetype_data = Gauge_types(description=form.description.data, calibration_reference=form.calibration_reference.data,
                                     calibration_link=form.calibration_link.data)
        sa.session.add(gaugetype_data)
        sa.session.commit()
        flash('Gauge Type Added...')
        return redirect(url_for('calibration.listgaugetypes'))
    
@calibration_blueprint.route('addcalibrationreference', methods=['POST', 'GET'])
def addcalibrationreference():
    form = EditCalibrationReferencesForm()
    if request.method == 'GET':
        gaugetype_id = request.args.get('gauge_type_id', 0)
        reference_id = 37 # default reference data
        gauge_types = [(row.id,row.description) for row in sa.session.scalars(sa.select(Gauge_types)).all()]
        form.gauge_type.choices = gauge_types
        form.gauge_type.data = gaugetype_id
        reference_data = sa.get_or_404(Calibration_references, reference_id)
        return render_template('editcalibrationreference.html', form=form, form_data=reference_data, gaugetype_id=gaugetype_id, gauge_types=[], 
                               action=url_for('calibration.addcalibrationreference'), title='Add Calibration Reference')
    if form.validate_on_submit():
        reference = Calibration_references(requirement1=form.requirement1.data,
                                           requirement2=form.requirement2.data,
                                           requirement3=form.requirement3.data,
                                           requirement4=form.requirement4.data,
                                           requirement5=form.requirement5.data,
                                           requirement6=form.requirement6.data,
                                           requirement7=form.requirement7.data,
                                           requirement8=form.requirement8.data,
                                           requirement9=form.requirement9.data,
                                           requirement10=form.requirement10.data,
                                           requirement11=form.requirement11.data,
                                           requirement12=form.requirement12.data,
                                           requirement13=form.requirement13.data,
                                           requirement14=form.requirement14.data,
                                           requirement15=form.requirement15.data,
                                           requirement16=form.requirement16.data,
                                           requirement17=form.requirement17.data,
                                           requirement18=form.requirement18.data,
                                           requirement19=form.requirement19.data,
                                           requirement20=form.requirement20.data,
                                           requirement21=form.requirement21.data,
                                           requirement22=form.requirement22.data,
                                           requirement23=form.requirement23.data,
                                           requirement24=form.requirement24.data,
                                           requirement25=form.requirement25.data,
                                           requirement26=form.requirement26.data,
                                           requirement27=form.requirement27.data,
                                           requirement28=form.requirement28.data,
                                           requirement29=form.requirement29.data,
                                           requirement30=form.requirement30.data,
                                           bool1=form.bool1.data,
                                           bool2=form.bool2.data,
                                           bool3=form.bool3.data,
                                           standard1=form.standard1.data,
                                           standard2=form.standard2.data,
                                           standard3=form.standard3.data,
                                           standard4=form.standard4.data)
        sa.session.add(reference)    
        gaugetype_data = sa.get_or_404(Gauge_types, form.gauge_type.data)
        gaugetype_data.calibration_reference=reference.id
        sa.session.commit()
        return redirect(url_for('calibration.listgaugetypes'))
    
@calibration_blueprint.route('editcalibrationreference', methods=['POST', 'GET'])
def editcalibrationreference():
    form = EditCalibrationReferencesForm()
    if request.method == 'GET':
        reference_id = request.args.get('id')
        gaugetype_id = request.args.get('gauge_type_id')
        gauge_types = [(row.id,row.description) for row in sa.session.scalars(sa.select(Gauge_types)).all()]
        form.gauge_type.choices = gauge_types
        form.gauge_type.data = gaugetype_id
        reference_data = sa.get_or_404(Calibration_references, reference_id)
        return render_template('editcalibrationreference.html', form=form, form_data=reference_data, 
                               action=url_for('calibration.editcalibrationreference'), title='Edit Calibration Reference')
    if form.validate_on_submit():
        reference_data = sa.get_or_404(Calibration_references, form.id.data)
        reference_data.requirement1=form.requirement1.data
        reference_data.requirement2=form.requirement2.data
        reference_data.requirement3=form.requirement3.data
        reference_data.requirement4=form.requirement4.data
        reference_data.requirement5=form.requirement5.data
        reference_data.requirement6=form.requirement6.data
        reference_data.requirement7=form.requirement7.data
        reference_data.requirement8=form.requirement8.data
        reference_data.requirement9=form.requirement9.data
        reference_data.requirement10=form.requirement10.data
        reference_data.requirement11=form.requirement11.data
        reference_data.requirement12=form.requirement12.data
        reference_data.requirement13=form.requirement13.data
        reference_data.requirement14=form.requirement14.data
        reference_data.requirement15=form.requirement15.data
        reference_data.requirement16=form.requirement16.data
        reference_data.requirement17=form.requirement17.data
        reference_data.requirement18=form.requirement18.data
        reference_data.requirement19=form.requirement19.data
        reference_data.requirement20=form.requirement20.data
        reference_data.requirement21=form.requirement21.data
        reference_data.requirement22=form.requirement22.data
        reference_data.requirement23=form.requirement23.data
        reference_data.requirement24=form.requirement24.data
        reference_data.requirement25=form.requirement25.data
        reference_data.requirement26=form.requirement26.data
        reference_data.requirement27=form.requirement27.data
        reference_data.requirement28=form.requirement28.data
        reference_data.requirement29=form.requirement29.data
        reference_data.requirement30=form.requirement30.data
        reference_data.bool1=form.bool1.data
        reference_data.bool2=form.bool2.data
        reference_data.bool3=form.bool3.data
        reference_data.standard1=form.standard1.data
        reference_data.standard2=form.standard2.data
        reference_data.standard3=form.standard3.data
        reference_data.standard4=form.standard4.data

        gaugetype_data = sa.get_or_404(Gauge_types, form.gauge_type.data)
        gaugetype_data.calibration_reference=form.id.data
        sa.session.commit()
        return redirect(url_for('calibration.listgaugetypes'))
    
@calibration_blueprint.route('leadstandardcert', methods=['POST', 'GET'])
def leadstandardcert():
    form = LeadStandardCalibrationForm()
    if request.method == 'GET':
        # get the last certificate number and add 1 for the new cert number
        newcert = str(int(sa.session.execute(sa.select(Calibration_certificates).order_by(Calibration_certificates.id.desc()))
                          .scalars().first().certificate_number) + 1)
        gauge_id = request.args.get('id')
        # gauge_id = 315
        gauge_data = sa.get_or_404(Gauges, gauge_id)
        today = datetime.today()
        todaystring=today.isoformat().split("T")[0]
        newcaldue = today + relativedelta(months=gauge_data.calibration_frequency)
        newcalduestring = newcaldue.isoformat().split("T")[0]
        return render_template('leadstandard.html', form=form, gauge_data=gauge_data, newcertnumber=newcert, today=todaystring, 
                               newcaldue=newcalduestring)
    if form.validate_on_submit():
        gauge_id = form.id.data
        gauge_data = sa.get_or_404(Gauges, gauge_id)
        certificate = Calibration_certificates(certificate_number=form.certificate_number.data,
                                               calibration_date=form.calibration_date.data,
                                               due_date=form.due_date.data,
                                               gauge=form.id.data,
                                               as_found=form.as_found.data,
                                               as_left=form.as_left.data,
                                               requirement1=gauge_data.type.referencedata.requirement1,
                                               requirement2=gauge_data.type.referencedata.requirement2,
                                               requirement3=gauge_data.type.referencedata.requirement3,
                                               requirement4=gauge_data.type.referencedata.requirement4,
                                               requirement5=gauge_data.type.referencedata.requirement5,
                                               requirement6=gauge_data.type.referencedata.requirement6,
                                               requirement7=gauge_data.type.referencedata.requirement7,
                                               requirement8=gauge_data.type.referencedata.requirement8,
                                               requirement9=gauge_data.type.referencedata.requirement9,
                                               requirement10=gauge_data.type.referencedata.requirement10,
                                               requirement11=gauge_data.type.referencedata.requirement11,
                                               requirement12=gauge_data.type.referencedata.requirement12,
                                               requirement13=gauge_data.type.referencedata.requirement13,
                                               measurement1=form.measurement1.data,
                                               measurement2=form.measurement2.data,
                                               measurement3=form.measurement3.data,
                                               measurement4=form.measurement4.data,
                                               measurement5=form.measurement5.data,
                                               measurement6=form.measurement6.data,
                                               measurement7=form.measurement7.data,
                                               measurement8=form.measurement8.data,
                                               measurement9=form.measurement9.data,
                                               measurement10=form.measurement10.data,
                                               measurement11=form.measurement11.data,
                                               measurement12=form.measurement12.data,
                                               measurement13=form.measurement13.data)
        sa.session.add(certificate)
        sa.session.commit()
        return "added"

