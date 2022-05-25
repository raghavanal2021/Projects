'''
Runs the Service Runner Container
'''

from ast import Load
from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container
from ScreenerGateway import ScreenerService
from Screeners.NRScreener import NarrowRange
runner = ServiceRunner(config={
'AMQP_URI' : 'pyamqp://guest:guest@localhost',
'WEB_SERVER_ADDRESS' : '0.0.0.0:8201',
'rpc_exchange' : 'nameko-rpc',
'max_worker' : 10,
'parent_calls_tracked' : 10
})
runner.add_service(ScreenerService)
runner.add_service(NarrowRange)
runner.start()

