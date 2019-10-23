from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField

from ....models import DeviceTask, Device


class DeviceTaskSchema(Schema):
    model = DeviceTask

    id = fields.Integer()

    task = fields.Raw(
        required=True
    )
    created_at = ArrowField()

    device_id = fields.Integer(
        required=True,
        validate=[
            lambda dev_id: Device.query.get(dev_id) is not None
        ]
    )