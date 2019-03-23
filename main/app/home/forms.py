from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms_alchemy import ModelForm

from app.home.model import Feature, Client


class FeatureRequestForm(ModelForm, FlaskForm):
    client = SelectField(coerce=str)
    product_area = SelectField(
        choices=Feature.PRODUCT_AREAS,
        coerce=int,
    )

    class Meta:
        model = Feature
        only = [
            'title',
            'description',
            'client',
            'client_priority',
            'target_date',
            'product_area'
        ]

    def __init__(self, *args, **kwargs):
        """Initialize form for requesting a feature."""
        super(FeatureRequestForm, self).__init__(*args, **kwargs)
        clients = [(str(client.id), client.name) for client in Client.query.all()]
        self.client.choices = clients
