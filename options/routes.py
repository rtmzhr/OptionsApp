from flask import render_template, flash, redirect, url_for, session
from options import app
from options.forms import InterviewForm, SimulateForm
from options.Models.managers import OptionsManager, option_data
from options.Models.strategies import IronCodorStrategy

dates = option_data.get_dates_texts()


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', dates=dates, title="Choose Date:")


@app.route('/date/<string:date_text>', methods=['GET', 'POST'])
def date(date_text):
    form = InterviewForm()
    session['date'] = date_text
    if form.validate_on_submit():
        session['answers'] = {
            'Option Period': int(option_data.set_options_date(date_text)),
            'Price Estimation': int(form.price_estimation.data),
            'Estimation Likelihood': int(form.estimation_likelihood.data) / 100,
            'Stock Increase Likelihood': int(form.stock_increase_likelihood.data) / 100,
            'Stock Decrease Likelihood': int(form.stock_decrease_likelihood.data) / 100,
            'Risk Appetite': int(form.risk_appetite.data)
        }
        return redirect(url_for('simulation', chosen_strategy='IronCodor'))
    return render_template('interview.html', date=date_text, form=form, title='Interview')


@app.route('/strategy')
def strategy():
    return render_template('strategy.html', date=session.get('date')
                           , title="Choose Strategy:")


@app.route('/simulation/<string:chosen_strategy>', methods=['GET', 'POST'])
def simulation(chosen_strategy):
    form = SimulateForm()
    option_manager = OptionsManager(session.get('answers'))
    if chosen_strategy == "IronCodor":
        s = IronCodorStrategy(option_manager)
        s.execute()
    if form.validate_on_submit():
        profit = option_manager.simulate_profit(int(form.future_strike.data))
        if profit > 0:
            flash(f'The simulation indicated that you will gain {profit}$ in total', 'success')
        else:
            flash(f'The simulation indicated that you will gain {profit}$ in total', 'danger')
    return render_template('simulation.html', strategy=chosen_strategy, form=form, date=session.get('date'),
                           option_manager=option_manager, title="Simulation")
