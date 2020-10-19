const { Builder, By, Key, until } = require('selenium-webdriver');
const cheerio = require('cheerio');

async function example() {
    let driver = await new Builder().forBrowser('chrome').build();

    await driver.get('https://auth.ncloud.com/nsa');
    await driver.findElement(By.id('username')).sendKeys('id', Key.RETURN);
    await driver.findElement(By.id('passwordPlain')).sendKeys('pw', Key.RETURN);

    var html = await driver.getPageSource();

    // var $ = cheerio.load(html);
    // var text = $('#app > div > header > div.center-wrap > div.fr > div.util.hidden-sm-down > a').text();

    await driver.findElement(By.css('#app > div > header > div.center-wrap > div.fr > div.util.hidden-sm-down > a')).click();
    var apiKey = await driver.manage().getCookie('ncp_nnb');

    console.log(apiKey.value);
    // console.log(html)
}
example();