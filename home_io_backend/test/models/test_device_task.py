import uuid

import pytest
from sqlalchemy import bindparam
from sqlalchemy_utils import JSONType, ArrowType

from ...models import DeviceLog, Device, User, TypeEnum, DeviceTask


@pytest.fixture(scope='function')
def dev_task_id(app, db):
    with app.app_context():
        user = User(
            email="hi@gmail.com",
            username="newUser",
            password="password"
        )
        db.session.add(user)
        db.session.flush()

        dev = Device(
            id=uuid.uuid4(),
            name="deviceD",
            device_type=TypeEnum.blinker,
            owner_id=user.id
        )
        db.session.add(dev)
        db.session.flush()

        dev_task = DeviceTask(
            device_id=dev.id,
            task={
                "task": "mainTask"
            }
        )
        db.session.add(dev_task)
        db.session.commit()
        return dev_task.id


class TestDeviceTask():
    def test_create(self,app, db):
        with app.app_context():
            user = User(
                email = "privet@gmail.com",
                username="mainUser",
                password = "password"
            )
            db.session.add(user)
            db.session.flush()

            dev = Device(
                id=uuid.uuid4(),
                name = "deviceName",
                device_type = TypeEnum.blinker,
                owner_id= user.id
            )
            db.session.add(dev)
            db.session.flush()

            dev_task = DeviceTask(
                device_id= dev.id,
                task = {
                    "task": "mainTask"
                }
            )
            db.session.add(dev_task)
            db.session.commit()

    def test_read(self, app, db, dev_task_id):
        with app.app_context():
            # read device task
            bq = DeviceTask.baked_query + (lambda q: q
                .filter(DeviceTask.id == bindparam('dev_task_id'))
            )
            bq_params = {
                'dev_task_id': dev_task_id
            }
            dev_task = (bq(app.db.session())
                .params(bq_params)
                .one_or_none())

            # update device data
            assert dev_task.id == dev_task_id

    def test_update(self, app, db, dev_task_id):
        with app.app_context():
            # read device task
            bq = DeviceTask.baked_query + (lambda q: q
                .filter(DeviceTask.id == bindparam('dev_task_id'))
            )
            bq_params = {
                'dev_task_id': dev_task_id
            }
            dev_task = (bq(app.db.session())
                 .params(bq_params)
                 .one_or_none())

            # update device data

            dev_task.task = {
                'enabled': True
            }
            db.session.add(dev_task)
            db.session.commit()

    def test_delete(self, app, db, dev_task_id):
        with app.app_context():
            # read device task
            bq = DeviceTask.baked_query + (lambda q: q
                .filter(DeviceTask.id == bindparam('dev_task_id'))
            )
            bq_params = {
                'dev_task_id': dev_task_id
            }
            dev_task = (bq(app.db.session())
                .params(bq_params)
                .one_or_none())

            # update device data
            db.session.delete(dev_task)
            db.session.commit()
