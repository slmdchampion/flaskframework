from flask_wtf import FlaskForm

from wtforms import ( 
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    FileField,
    IntegerField,
    DecimalField,
    DateField,
    SelectField,
    FloatField
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Optional)

class LeadStandardCalibrationForm(FlaskForm):
    # hidden field for the gauge id (not the calibration cert id)
    id = IntegerField('ID: ', validators=[DataRequired()])
    certificate_number = IntegerField('Certification No:', validators=[DataRequired()])
    # instrument = StringField('Instrument:', validators=[DataRequired()])
    # serial_number = StringField('Serial Number:', validators=[DataRequired()])
    calibration_date = DateField('Date of calibration', validators=[DataRequired()])
    due_date = DateField('Date Due:', validators=[DataRequired()])
    as_found = SelectField('Condition As found:', choices=[('In Tolerance','In Tolerance'),('Out of Tolerance','Out of Tolerance')], validators=[DataRequired()])
    as_left = SelectField('Condition as left:', choices=[('In Tolerance','In Tolerance'),('Out of Tolerance','Out of Tolerance')], validators=[DataRequired()])
    measurement1 = FloatField(validators=[InputRequired()])
    measurement2 = FloatField(validators=[InputRequired()])
    measurement3 = FloatField(validators=[InputRequired()])
    measurement4 = FloatField(validators=[InputRequired()])
    measurement5 = FloatField(validators=[InputRequired()])
    measurement6 = FloatField(validators=[InputRequired()])
    measurement7 = FloatField(validators=[InputRequired()])
    measurement8 = FloatField(validators=[InputRequired()])
    measurement9 = FloatField(validators=[InputRequired()])
    measurement10 = FloatField(validators=[InputRequired()])
    measurement11 = FloatField(validators=[InputRequired()])
    measurement12 = FloatField(validators=[InputRequired()])
    measurement13 = FloatField(validators=[InputRequired()])
    # uncertainty = FloatField(validators=[DataRequired()])
    # temperature = FloatField(validators=[DataRequired()])
    submit = SubmitField('Save Record')

class EditCalibrationReferencesForm(FlaskForm):
    gauge_type = SelectField("Gauge Type:", choices=(), validate_choice=False)
    id = IntegerField('ID: ', validators=[DataRequired()])
    requirement1 = FloatField("Requirement 1", default="")
    requirement2 = FloatField("Requirement 2", default=0)
    requirement3 = FloatField("Requirement 3", default=0)
    requirement4 = FloatField("Requirement 4", default=0)
    requirement5 = FloatField("Requirement 5", default=0)
    requirement6 = FloatField("Requirement 6", default=0)
    requirement7 = FloatField("Requirement 7", default=0)
    requirement8 = FloatField("Requirement 8", default=0)
    requirement9 = FloatField("Requirement 9", default=0)
    requirement10 = FloatField("Requirement 10", default=0)
    requirement11 = FloatField("Requirement 11", default=0)
    requirement12 = FloatField("Requirement 12", default=0)
    requirement13 = FloatField("Requirement 13", default=0)
    requirement14 = FloatField("Requirement 14", default=0)
    requirement15 = FloatField("Requirement 15", default=0)
    requirement16 = FloatField("Requirement 16", default=0)
    requirement17 = FloatField("Requirement 17", default=0)
    requirement18 = FloatField("Requirement 18", default=0)
    requirement19 = FloatField("Requirement 19", default=0)
    requirement20 = FloatField("Requirement 20", default=0)
    requirement21 = FloatField("Requirement 21", default=0)
    requirement22 = FloatField("Requirement 22", default=0)
    requirement23 = FloatField("Requirement 23", default=0)
    requirement24 = FloatField("Requirement 24", default=0)
    requirement25 = FloatField("Requirement 25", default=0)
    requirement26 = FloatField("Requirement 26", default=0)
    requirement27 = FloatField("Requirement 27", default=0)
    requirement28 = FloatField("Requirement 28", default=0)
    requirement29 = FloatField("Requirement 29", default=0)
    requirement30 = FloatField("Requirement 30", default=0)
    bool1 = SelectField('Bool 1:', choices=[('PASS','PASS'),('FAIL','FAIL')], default='PASS')
    bool2 = SelectField('Bool 2:', choices=[('PASS','PASS'),('FAIL','FAIL')])
    bool3 = SelectField('Bool 3:', choices=[('PASS','PASS'),('FAIL','FAIL')])
    standard1 = IntegerField("Standard 1:", default=168)
    standard2 = IntegerField("Standard 2:", default=168)
    standard3 = IntegerField("Standard 3:", default=168)
    standard4 = IntegerField("Standard 4:", default=168)
    submit = SubmitField('Save Record')

class ListGaugeTypesForm(FlaskForm):
    submit = SubmitField('Save Record')

class EditGaugeTypesForm(FlaskForm):
    id = IntegerField('ID: ', validators=[DataRequired()], default=0)
    description = StringField('Description:', validators=[DataRequired()])
    calibration_reference = IntegerField('Calibration Reference:', validators=[Optional()])
    calibration_link = StringField('Calibration Link')
    submit = SubmitField('Save Record')

class AddGaugeTypesForm(FlaskForm):
    id = IntegerField('ID: ', default=0)
    description = StringField('Description:', validators=[DataRequired()])
    calibration_reference = IntegerField('Calibration Reference:', validators=[Optional()])
    calibration_link = StringField('Calibration Link')
    submit = SubmitField('Save Record')


class EditUncertaintiesForm(FlaskForm):
    id = IntegerField('ID: ', default=0)
    process_field = StringField('Process:', validators=[DataRequired()])
    # process = StringField("Process:", validators=[DataRequired()])
    # process = StringField('Process:', validators=[DataRequired()])
    gauge_type = SelectField("Gauge Type:", choices=(), validate_choice=False)
    uncertainty = FloatField("Uncertainty", default=0)
    submit = SubmitField('Save Record')