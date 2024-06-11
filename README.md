## 配置 

请在 `conf/config.ini` 文件中配置 `user`, `password`、`driver` 等参数。

## 运行

```bash
./scripts/run.sh
```

## Web Driver
 
目前支持 firefow, chrome, edege, safari 浏览器, 默认使用 firefox 浏览器; 注意 safari 浏览器需要使用者提前配置或使能。
 
### 更新 webdriver

- [chrome](https://googlechromelabs.github.io/chrome-for-testing)
- [edge](https://msedgewebdriverstorage.z22.web.core.windows.net/)
- [firefox](https://github.com/mozilla/geckodriver/releases/latest)

### 配置支持 Safari WebDriver
>
>- High Sierra and later:
>
>Run `safaridriver --enable` once. (If you’re upgrading from a previous macOS release, you may need to use sudo.)
>
>- Sierra and earlier:
>
>If you haven’t already done so, make the Develop menu available. Choose Safari > Preferences, and on the Advanced tab, select “Show Develop menu in menu bar.” For details, see Safari Help.
>
>Choose Develop > Allow Remote Automation.
>
>Authorize safaridriver to launch the XPC service that hosts the local web server. To permit this, manually run /usr/bin/safaridriver once and follow the authentication prompt.

## TODO

部分网页元素较复杂，不太好定位，需要进一步研究; 目前提交环节需人工介入，选择审批人并提交。

## References
- [testing_with_webdriver_in_safari](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari#2957283)