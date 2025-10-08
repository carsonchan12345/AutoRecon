from autorecon.plugins import ServiceScan


class NmapISAKMP(ServiceScan):

	def __init__(self):
		super().__init__()
		self.name = "Nmap ISAKMP"
		self.tags = ['default', 'safe', 'isakmp', 'vpn']

	def configure(self):
		self.match_port('udp', 500)
		self.match_service_name(['^isakmp', '^ike'])
		self.run_once(True)

	async def run(self, service):
		await service.execute('nmap {nmap_extra} -sV -p {port} --script="ike-version" -oN "{scandir}/{protocol}_{port}_isakmp_nmap.txt" -oX "{scandir}/xml/{protocol}_{port}_isakmp_nmap.xml" {address}')
