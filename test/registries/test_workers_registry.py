
import pytest

from eventsflow.registries.queues import QueuesRegistry
from eventsflow.registries.workers import WorkersRegistry

from eventsflow.workers.process import ProcessingWorker


def test_workers_registry_init_no_queues_registry():

    with pytest.raises(TypeError):
        registry = WorkersRegistry()
        assert registry is not None


def test_workers_registry_init():

    registry = WorkersRegistry(queues=QueuesRegistry())
    assert registry is not None


def test_workers_registry_load_empty_workers_config():

    registry = WorkersRegistry(queues=QueuesRegistry())
    with pytest.raises(TypeError):
        registry.load([])


def test_workers_registry_load_incorrect_workers_config():
    ''' incorrect workers config, shall be the list of workers, passed as dict
    '''
    registry = WorkersRegistry(queues=QueuesRegistry())
    with pytest.raises(TypeError):
        registry.load({'name': 'TestWorker', })


def test_workers_registry_load_workers_config_wo_worker_type():
    ''' incorrect workers config, missed worker type
    '''
    registry = WorkersRegistry(queues=QueuesRegistry())
    with pytest.raises(TypeError):
        registry.load([
            {'name': 'TestWorker', },
        ])

def test_workers_registry_load_workers_config_incorrect_worker_type():
    ''' incorrect worker type
    '''
    registry = WorkersRegistry(queues=QueuesRegistry())

    with pytest.raises(TypeError):
        registry.load([
            {'name': 'TestWorker', 'type': 'eventsflow.workers.ProcessingWorker', },
        ])

    with pytest.raises(TypeError):
        registry.load([
            {'name': 'TestWorker', 'type': 'eventsflow.workers.v2.ProcessingWorker', },
        ])


def test_workers_registry_load_workers_config():
    ''' correct load of workers config to registry
    '''
    registry = WorkersRegistry(queues=QueuesRegistry())
    registry.load([
        {'name': 'TestWorker', 'type': 'eventsflow.workers.process.ProcessingWorker', },
    ])
    assert [ type(w) for w in registry.workers] == [ ProcessingWorker, ] 


def test_workers_registry_load_workers_queues():
    ''' load workers to registry with queues
    '''

    QUEUES = [
        {'name': 'SourceQueue', 'type': 'eventsflow.queues.local.EventsQueue', },
        {'name': 'TargetQueue', 'type': 'eventsflow.queues.local.EventsQueue', },
    ]
    queues = QueuesRegistry()
    queues.load(QUEUES)

    WORKERS = [
        {   'name': 'TestWorker', 
            'type': 'eventsflow.workers.process.ProcessingWorker', 
            'inputs': 'SourceQueue', 
            'outputs':  'TargetQueue',
        },
    ]
    registry = WorkersRegistry(queues=queues)
    registry.load(WORKERS)

    assert [ type(w) for w in registry.workers] == [ ProcessingWorker, ] 
