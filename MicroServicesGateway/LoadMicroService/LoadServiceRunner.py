'''
Runs the Service Runner Container
'''

from ast import Load
from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container
from DerivativeLoadService import DerivativeLoad
from LoadService import LoadService
from EquityLoadService import EquityLoad
#Create the runner
runner = ServiceRunner(config={
'AMQP_URI' : 'pyamqp://guest:guest@localhost',
'WEB_SERVER_ADDRESS' : '0.0.0.0:8200',
'rpc_exchange' : 'nameko-rpc',
'max_worker' : 10,
'parent_calls_tracked' : 10
})
runner.add_service(LoadService)
runner.add_service(EquityLoad)
runner.add_service(DerivativeLoad)
runner.start()

