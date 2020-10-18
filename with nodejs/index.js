const { Builder, By, Key, until } = require('selenium-webdriver');

async function example() {
    let driver = await new Builder().forBrowser('chrome').build();
        await driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com');
        await driver.findElement(By.id('id')).sendKeys('id', Key.RETURN);
        await driver.findElement(By.id('pw')).sendKeys('pass', Key.RETURN);

        // await driver.findElement(By.name('q')).sendKeys('Selenium', Key.ENTER);
        
    // var html = await driver.getPageSource();
    // console.log(html)
}
example();