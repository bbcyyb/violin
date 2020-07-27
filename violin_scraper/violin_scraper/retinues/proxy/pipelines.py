from violin_scraper.retinues.proxy.items import ProxyItem
from utility.file import File
import datetime
from pathlib import Path


class Pipeline:
    def process_item(self, item, spider):
        folder_path = r'./proxy_pool'
        if isinstance(item, ProxyItem):
            path = Path(folder_path)
            if not path.is_dir():
                path.mkdir(parents=True)

            content = '{},{},{},{},{}'.format(item['ip'], item['port'], item['location'], item['kind'], item['last_verify_time'])
            f = File(spider.logger)
            date_now = datetime.datetime.now()
            full_path = path.joinpath('66ip_cn_{}{}{}{}.proxy'.format(date_now.year, date_now.month, date_now.day, date_now.hour))

            f.open_file(str(full_path.resolve()), mode='a')
            f.writeline(content, True)
            f.close_file()

        return item
