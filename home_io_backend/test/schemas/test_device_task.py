import uuid

import pytest

from ...models import Device, User, TypeEnum, DeviceTask
from ...api.v1.schemas import DeviceTaskReadSchema, DeviceTasksReadSchema, \
    DeviceTaskCreateSchema, DeviceTaskUpdateSchema, DeviceTasksReadSchema
from marshmallow.exceptions import ValidationError


@pytest.fixture(scope='function')
def device_id(app, db):
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(user)
        db.session.flush()

        device = Device(
            id=uuid.uuid4(),
            name='testdevice',
            device_type=TypeEnum.blinker,
            owner_id=user.id
        )
        db.session.add(device)
        db.session.commit()
        return device.id


@pytest.fixture(scope='function')
def device_task(app, db, device_id):
    with app.app_context():
        dev_task = DeviceTask(
            device_id=device_id,
            task={
                "task": "task1"
            }
        )
        db.session.add(dev_task)
        db.session.commit()
        return dev_task


class TestDeviceTaskReadSchema:
    def test_read(self, app, device_task):
        with app.app_context():
            dev_task = DeviceTask.query.all()[0]
            try:
                res = DeviceTaskReadSchema.dump(dev_task)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceTasksReadSchema:
    def test_read(self, app, device_task):
        with app.app_context():
            dev_task = DeviceTask.query.all()
            try:
                res = DeviceTaskReadSchema.dump(dev_task)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceTaskCreateSchema:
    @pytest.mark.parametrize(
        'task',
        (tuple(), )
    )
    def test_invalid_device_task(self, app, task):
        try:
            with app.app_context():
                DeviceTaskCreateSchema.load(task)
                assert False, 'Exception must occur'
        except ValidationError as e:
            pass

    @pytest.mark.parametrize(
        'task',
        ({ "task": "task" },)
    )
    def test_valid_data(self, app, task, device_id):
        try:
            with app.app_context():
                task['device_id'] = device_id
                DeviceTaskCreateSchema.load(task)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'

    @pytest.mark.parametrize(
        'id, task, created_at',
        (
            (1, {"task": "task"}, 'ANYTIME'),
        )
    )
    def test_pass_not_allowed_keys(self, app, id, task, created_at, device_id):
        device_task_data = {
            'id': id,
            'task': task,
            'created_at': created_at,
            'device_id': device_id,
        }
        try:
            with app.app_context():
                DeviceTaskCreateSchema.load(device_task_data)
                assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages


class TestDeviceTaskUpdateSchema:
    @pytest.mark.parametrize(
        'id, created_at',
        ((1, 'ANYTIME'),)
    )
    def test_pass_not_allowed_keys(self, app, id, created_at, device_id):
        device_task_data = {
            'id': id,
            'created_at': created_at,
            'device_id': device_id
        }
        try:
            with app.app_context():
                DeviceTaskUpdateSchema.load(device_task_data)
                assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'task',
        (({"task": "task"}, ),)
    )
    def test_partial_update(self, task):
        device_task_data = {
            'task': task,
        }
        try:
            DeviceTaskUpdateSchema.load(device_task_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'