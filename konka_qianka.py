from config import Config
from ehr import EHR

config_path = 'conf/config.ini'
url='https://eip.konka.com/login.jsp'

if __name__ == '__main__':
    try:
        conf = Config(config_path)
        ehr = EHR(driver=conf.DRIVER, path=conf.DRIVER_PATH, url=url)
        ehr.login(url=url, username=conf.USER, password=conf.PASSWORD)
        ehr.enter_ehr()
        ehr.enter_kaoqin()
        ehr.filter_month(start_year=conf.YEAR, start_month=conf.MONTH)
        reports = ehr.get_reports(id=conf.ID, threshold=conf.THRESHOLD)
        ehr.submit_reports(reports=reports)

    except Exception as e:
        print(f"运行异常: {e}")
    finally:
        print("OK!")