import { Builder, By, Key, until } from 'selenium-webdriver';
import * as chrome from 'selenium-webdriver/chrome.js';

export default class Scrapper {

  _options = new chrome.Options();
  _driver  = new Builder().forBrowser('chrome');

  constructor() {
      this._options.addArguments('--headless');       // 크롬 창 없이 실행
      this._options.addArguments('--no-sandbox');     // 보안기능 sandbox 비활성화
      this._options.addArguments('--disabled-gpu');   // gpu 비활성화 (for linux)
      this._options.addArguments('--disabled-dev-shm-usage'); // WebDriverException 문제 
      this._driver.setChromeOptions(this._options).build();
  }

  async moveSite(siteUrl) {
      return await this._driver.get(siteUrl);
  }

  async login(idElementName, pwElementName, id, pw) {
      await this._driver.findElement(By.name(idElementName)).sendKeys(id);
      await this._driver.findElement(By.name(pwElementName)).sendKeys(pw, Key.ENTER);
  }

  // 사이트가 바로 뜨지 않는 경우의 문제를 해결하기 위해 WebDriver를 재움
  async sleepDriver(sleepMillis) {
      return await this._driver.sleep(sleepMillis);
  }

  // 원하는 요소가 자리할때까지 지속적으로 확인하면서 explicitWaitMillis 까지 기다림
  async getElementAndExplicitWaitMillis(querySelector, explicitWaitMillis) {
      await this._driver.wait(until.elementLocated(By.css(querySelector)), explicitWaitMillis);
      return await this._driver.findElement(By.css(querySelector));
  }

  getPageSource() {
      return this._driver.getPageSource();
  }

  getCurrentUrl() {
      return this._driver.getCurrentUrl();
  }

  async quitDriver() {
      return await this._driver.quit();
  }
}