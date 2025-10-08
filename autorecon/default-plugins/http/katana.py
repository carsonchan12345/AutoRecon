from shutil import which

from autorecon.plugins import ServiceScan


class Katana(ServiceScan):

        def __init__(self):
                super().__init__()
                self.name = 'Katana Web Crawler'
                self.slug = 'katana'
                self.tags = ['default', 'safe', 'http']

        def configure(self):
                self.add_option('extras', default='', help='Any extra options to pass to katana. Default: %(default)s')
                self.match_service_name('^http')
                self.match_service_name('^nacn_http$', negative_match=True)

        def check(self):
                if which('katana') is None:
                        self.error('The katana program could not be found. Make sure it is installed. (On Kali, run: sudo apt install '
                                   'katana)')
                        return False

        async def run(self, service):
                if service.protocol == 'tcp':
                        extras = ' ' + self.get_option('extras') if self.get_option('extras') else ''
                        await service.execute(
                                'katana -jc -jsl -kf all -fx -u {http_scheme}://{addressv6}:{port}/' + extras +
                                ' 2>&1 | tee "{scandir}/{protocol}_{port}_{http_scheme}_katana.txt"'
                        )

        def manual(self, service, plugin_was_run):
                if not plugin_was_run:
                        extras = ' ' + self.get_option('extras') if self.get_option('extras') else ''
                        service.add_manual_command(
                                '(katana) Modern web crawling and JS discovery tool:',
                                'katana -jc -jsl -kf all -fx -u {http_scheme}://{addressv6}:{port}/' + extras +
                                ' 2>&1 | tee "{scandir}/{protocol}_{port}_{http_scheme}_katana.txt"'
                        )
