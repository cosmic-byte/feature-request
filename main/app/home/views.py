from flask import render_template, Blueprint, request, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import db
from app.home.forms import FeatureRequestForm
from app.home.model import Client, Feature

app = Blueprint('home', __name__, template_folder='templates',
                static_folder='static')


@app.route('/')
@login_required
def home():
    feature_requests = Feature.query.filter_by(
        requested_by=str(current_user.id),
        deleted=False
    ).order_by('client_priority').all()
    for feature in feature_requests:
        feature.request_client = Client.query.get(feature.client)
        feature.request_status = dict(Feature.REQUEST_STATUS)[feature.request_status]
    return render_template('pages/home.html', feature_requests=feature_requests)


@app.route('/create-request', methods=['GET', 'POST'])
@login_required
def create_request():
    feature_form = FeatureRequestForm(request.form)
    if request.method == 'POST' and feature_form.validate_on_submit():
        data = {**feature_form.data}
        _ = data.pop('csrf_token', None)
        client_id = data.get('client')
        previous_requests_for_client = Feature.query.filter(
            Feature.client_priority >= data['client_priority']
        ).filter_by(
            client=client_id,
            deleted=False
        ).order_by('client_priority').all()

        assigned_request_priority = Feature.query.filter_by(
            client_priority=data['client_priority'],
            client=client_id,
            deleted=False
        ).all()

        if assigned_request_priority:
            last_changed = data['client_priority']
            for previous_request in previous_requests_for_client:
                if previous_request.client_priority == last_changed:
                    previous_request.client_priority += 1
                    last_changed = previous_request.client_priority

            previous_requests_for_client = previous_requests_for_client[::-1]
            db.session.bulk_save_objects(previous_requests_for_client)
            db.session.commit()

        feature = Feature(
            requested_by=str(current_user.id),
            request_status=Feature.REQUEST_STATUS_PENDING,
            **data
        )
        db.session.add(feature)
        db.session.commit()
        flash('Feature request created successfully!')
        return redirect(url_for('home.home'))
    return render_template('forms/request-feature.html', form=feature_form)


@app.route('/edit-request/<request_id>', methods=['GET', 'POST', 'PUT', 'PATCH'])
@login_required
def edit_request(request_id):
    feature_request = Feature.query.filter_by(id=str(request_id), requested_by=str(current_user.id)).first()
    if feature_request:
        feature_form = FeatureRequestForm(obj=feature_request, formdata=request.form)
        if request.method in ['POST', 'PUT', 'PATCH'] and feature_form.validate_on_submit():
            data = {**feature_form.data}
            _ = data.pop('csrf_token', None)
            for key, value in data.items():
                setattr(feature_request, key, value)
            db.session.add(feature_request)
            db.session.commit()
            flash('Feature request updated successfully!')
            return redirect(url_for('home.home'))
        return render_template('forms/edit-request-feature.html', form=feature_form, request_id=request_id)
    else:
        return redirect(url_for('home.home'))


@app.route('/delete-request/<request_id>', methods=['GET'])
@login_required
def delete_request(request_id):
    feature_request = Feature.query.get(str(request_id))
    feature_request.deleted = True
    db.session.add(feature_request)
    db.session.commit()
    flash('Feature deleted successfully!')
    return redirect(url_for('home.home'))
