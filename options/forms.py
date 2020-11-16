from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class FormQuestion(IntegerField):
    def __init__(self, question, label=None, validators=None, **kwargs):
        self.question = question
        IntegerField.__init__(self, label, validators, **kwargs)


class InterviewForm(FlaskForm):
    price_estimation = FormQuestion("What do you think the price of the stock will be then? Please write an Integer.",
                                    'Price Estimation', validators=[DataRequired(), NumberRange(0, 500)])

    estimation_likelihood = FormQuestion("What are the chances the stock will reach your estimation? Please write an "
                                         "Integer percentage %. ", 'Estimation Likelihood',
                                         validators=[DataRequired(), NumberRange(0, 100)])
    risk_appetite = FormQuestion("Rate from 1 - 10 the risk level you wish (10 is the highest)", 'Risk Appetite',
                                 validators=[DataRequired(), NumberRange(1, 10)])
    stock_decrease_likelihood = FormQuestion("Whats are the chances the stock price will increase in this period? "
                                             "Please write an Integer percentage %", 'Stock Decrease Likelihood',
                                             validators=[DataRequired(), NumberRange(0, 100)])
    stock_increase_likelihood = FormQuestion("Whats are the chances the stock price will decrease in this period? "
                                             "Please write am Integer percentage%", 'Stock Increase Likelihood',
                                             validators=[DataRequired(), NumberRange(0, 100)])
    submit = SubmitField('Consult Me!')


class SimulateForm(FlaskForm):
    future_strike = FormQuestion("What is the future strike you wish to simulate?",
                                 'Future Strike', validators=[DataRequired(), NumberRange(0, 500)])
    simulate = SubmitField("Simulate!")
