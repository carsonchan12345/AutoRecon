from autorecon.plugins import ServiceScan


class IKEScan(ServiceScan):

	def __init__(self):
		super().__init__()
		self.name = "ike-scan"
		self.tags = ['default', 'safe', 'isakmp', 'vpn']

	def configure(self):
		self.match_port('udp', 500)
		self.match_service_name(['^isakmp', '^ike'])
		self.run_once(True)

	async def run(self, service):
		if service.target.ipversion == 'IPv4':
			await service.execute('ike-scan {address} -M -A', outfile='{protocol}_{port}_isakmp_ike-scan.txt')
