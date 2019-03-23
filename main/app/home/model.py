import uuid
from datetime import datetime

from sqlalchemy_utils import ChoiceType, UUIDType

from app import db


class Feature(db.Model):
    """Model for tracking feature requests."""
    __tablename__ = "home_feature"

    REQUEST_STATUS_PENDING = 0
    REQUEST_STATUS_APPROVED = 1
    REQUEST_STATUS_REJECTED = 2
    REQUEST_STATUS_ONGOING = 3
    REQUEST_STATUS_RESCHEDULED = 4
    REQUEST_STATUS_COMPLETED = 5

    REQUEST_STATUS = (
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_APPROVED, 'Approved'),
        (REQUEST_STATUS_REJECTED, 'Rejected'),
        (REQUEST_STATUS_ONGOING, 'Ongoing'),
        (REQUEST_STATUS_RESCHEDULED, 'Rescheduled'),
        (REQUEST_STATUS_COMPLETED, 'Completed')
    )

    PRODUCT_AREA_POLICIES = 0
    PRODUCT_AREA_BILLING = 1
    PRODUCT_AREA_CLAIMS = 2
    PRODUCT_AREA_REPORTS = 3

    PRODUCT_AREAS = (
        (PRODUCT_AREA_POLICIES, 'Policies'),
        (PRODUCT_AREA_BILLING, 'Billing'),
        (PRODUCT_AREA_CLAIMS, 'Claims'),
        (PRODUCT_AREA_REPORTS, 'Reports')
    )

    id = db.Column(UUIDType(binary=False), primary_key=True, unique=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    client = db.Column(db.ForeignKey('home_client.id'), nullable=False)
    client_priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    product_area = db.Column(ChoiceType(PRODUCT_AREAS, impl=db.Integer()), default=PRODUCT_AREA_POLICIES)
    requested_by = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    request_status = db.Column(ChoiceType(REQUEST_STATUS, impl=db.Integer()), default=REQUEST_STATUS_PENDING)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "{}_{}".format(self.shortened_title, self.shortened_id)

    @property
    def shortened_title(self):
        """Get shortened version title."""
        return str(self.title)[:20]

    @property
    def shortened_id(self):
        """Get shortened version of id."""
        return str(self.id)[-8:]


class Client(db.Model):
    """Model for clients."""
    __tablename__ = "home_client"

    id = db.Column(UUIDType(binary=False), primary_key=True, unique=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
