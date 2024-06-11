from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from record import Record
from report_info import ReportInfo

class EHR:
    def __init__(self, driver: str, path: str, url: str):
        if driver == "firefox":
            from selenium.webdriver.firefox.service import Service
            self.driver = webdriver.Firefox(service=Service(path))
        elif driver == "chrome":
            from selenium.webdriver.chrome.service import Service
            self.driver = webdriver.Chrome(service=Service(path))
        elif driver == "edge":
            from selenium.webdriver.edge.service import Service
            self.driver = webdriver.Edge(service=Service(path))
        elif driver == "safari":
            from selenium.webdriver.safari.service import Service
            self.driver = webdriver.Safari(service=Service(path))
        else:
            raise Exception(f"{driver} not support")
        self.timeout = 10
        self.url = url
        self.driver.maximize_window()
        self.element_table : list[WebElement] = []

    def __del__(self):
        # self.driver.quit()
        print("Quit driver")

    def login(self, url, username, password):
        self.driver.get(url)
        WebDriverWait(self.driver, timeout = self.timeout).until(
            EC.element_to_be_clickable((By.NAME, 'j_username'))
        )
        # <input type="text" name="j_username" class="login-input-username" placeholder="用户名" onfocus="select();" value="">
        self.driver.find_element(By.NAME, 'j_username').send_keys(username)
        # <input type="password" name="j_password" class="login-input-password" placeholder="密码" onfocus="select();" autocomplete="off">
        self.driver.find_element(By.NAME, 'j_password').send_keys(password)
        # <button class="login-button" name="btn_submit" type="submit">登录</button>
        self.driver.find_element(By.NAME, 'btn_submit').click()

    def open_next_window(self):
        cur_win = self.driver.current_window_handle
        num=len(self.driver.window_handles)
        for index in range(0, num):
            if self.driver.window_handles[index] == cur_win:
                next_win_index = index + 1
                if next_win_index < num:
                    next_win = self.driver.window_handles[next_win_index]
                    self.driver.switch_to.window(next_win)
                    print(f"{cur_win} ---> {next_win}")
                    break

    def enter_ehr(self):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id=\"lui-id-135\"]/div/div[1]/div/div/div/div[1]"))
        )
        element.click()
        self.open_next_window()

    def enter_kaoqin(self):
        # <iframe src="mgrqispi.dll?APPNAME=HRsoft2000&amp;PRGNAME=MAIN_FRAME_STAFF&amp;ARGUMENTS=-AS0778683555492151115" id="main" width="100%" height="612" frameborder="0" scrolling="yes" name="main"></iframe>
        WebDriverWait(self.driver, self.timeout).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id=\"main\"]")))
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[1]/div[2]/div[4]")))
        self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div[2]/div[4]").click()

    def filter_month(self, start_year, start_month):
        # <select size="1" name="Year" id="Year">
        #         <option value="2024" selected="">2024</option>
        #         <option value="2023">2023</option>
        #         <option value="2022">2022</option>
        #         </select>
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id=\"Year\"]')))
        print(f"考勤页面 {start_year}-{start_month}")
        self.click_select_text(by_strategy=By.XPATH, by_value='//*[@id=\"Year\"]', text=str(start_year).zfill(4))
        print(f"年份选择: {start_year}")
        self.click_select_text(by_strategy=By.XPATH, by_value='//*[@id=\"Month\"]', text=str(start_month).zfill(2))
        print(f"月份选择: {start_month}")
        self.driver.find_element(By.XPATH, '/html/body/form/table[2]/tbody/tr/td[7]/input').click()
        print(f"筛选考勤 OK!")

    def get_records(self) -> list[Record]:
        self.element_table = self.driver.find_element(By.XPATH, '/html/body/form/table[3]/tbody').find_elements(
            By.TAG_NAME, 'tr')
        size = len(self.element_table)
        records: list[Record] = []
        for i in range(0, size):
            record = Record()
            element: WebElement = self.element_table[i]
            if element.text is None:
                continue
            if '迟到' in element.text or '缺勤' in element.text:
                print(f"待签卡考勤记录: [{i}] {element.text}")
            else:
                continue
            record.extract(i, element.text)
            records.append(record)
        return records

    def get_reports(self, id: str, threshold: int) -> list[ReportInfo]:
        records = self.get_records()
        reports = []
        for record in records:
            report = ReportInfo()
            report.transform(id=id, threshold=threshold, record=record)
            reports.append(report)
        return reports

    def fill_element_text(self, by_strategy: str, by_value: str, text: str):
        element = self.driver.find_element(by_strategy, by_value)
        element.clear()
        element.send_keys(text)

    def click_select_text(self, by_value: str, text: str, by_strategy: str):
        select_element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by_strategy, by_value))
        )

        select = Select(select_element)
        select.select_by_visible_text(text)

    # def create_report(self, report: ReportInfo):
        # self.fill_element_text(By.XPATH,'/html/body/table/tbody/tr/td[1]/div/form/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/table/tbody/tr[1]/td[2]/div[1]/xformflag/input',
        #                        report.ID)
        # print(f"已填写：{report.ID}")
        # self.fill_element_text(By.XPATH, '/html/body/table/tbody/tr/td[1]/div/form/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/table/tbody/tr[3]/td[4]/label/xformflag/div/div[1]/input',
        #                        report.date.format_str())
        # print(f"已填写：{report.date.format_str()}")
        # self.fill_element_text(By.XPATH,'/html/body/table/tbody/tr/td[1]/div/form/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/table/tbody/tr[4]/td/table/tbody/tr[2]/td[6]/label',
        #                          report.time.format_str())
        # print(f"已填写：{report.time.format_str()}")
        # self.click_select_text(by_strategy=By.XPATH,
        #     by_value='/html/body/table/tbody/tr/td[1]/div/form/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/table/tbody/tr[4]/td/table/tbody/tr[2]/td[7]/xformflag/div/select',
        #     text=report.reason)
        # print(f"已选择：{report.reason}")
        # self.fill_element_text(By.XPATH,'/html/body/table/tbody/tr/td[1]/div/form/div/div/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div/table/tbody/tr[4]/td/table/tbody/tr[2]/td[8]/div/xformflag/input',
        #                        report.memo)
        # print(f"已填写：{report.memo}")
        # 人工介入，手动提交后，会弹出窗口继续下次


    def submit_reports(self, reports: list[ReportInfo]):
        for report in reports:
            element: WebElement = self.element_table[report.index]
            element.find_element(By.TAG_NAME, 'a').click()
            print(f"准备签卡: {report.str}")
            # self.open_next_window()
            # self.create_report(report)

