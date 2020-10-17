# Selenium with Node.js

## 1. WebDriver 설치

- [https://www.npmjs.com/package/selenium-webdriver](https://www.npmjs.com/package/selenium-webdriver) 로 들어가서
- 사용할 브라우저의 driver를 받아 프로젝트 폴더에 넣어줌

### 2. npm 설치

- selenium-webdriver를 npm으로 설치

  ```bash
  $ npm install selenium-webdriver
  ```

## 3. js 파일 생성

```javascript
const { Builder, By, Key, until } = require('selenium-webdriver');

async function example() {
    let driver = await new Builder().forBrowser('chrome').build();
    try {
        await driver.get('http://www.google.com/ncr');
        await driver.findElement(By.name('q')).sendKeys('webdriver', Key.RETURN);
        await driver.wait(until.titleIs('webdriver - Google Search'), 1000);
    } finally {
        await driver.quit();
    }
}
example();
```

- 위 코드를 입력하고 터미널에서

  ```bash
  $ node index.js
  ```

  

