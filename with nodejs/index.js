const { Builder, By, Key, until } = require('selenium-webdriver');
const cheerio = require('cheerio');
const request = require('request');

async function example() {
    let driver = await new Builder().forBrowser('chrome').build();

    await driver.get('https://auth.ncloud.com/nsa/');
    await driver.findElement(By.id('username')).sendKeys('id', Key.RETURN);
    await driver.findElement(By.id('passwordPlain')).sendKeys('pw', Key.RETURN);

    var html = await driver.getPageSource();

    // var $ = cheerio.load(html);
    // var text = $('#app > div > header > div.center-wrap > div.fr > div.util.hidden-sm-down > a').text();

    await driver.findElement(By.css('#app > div > header > div.center-wrap > div.fr > div.util.hidden-sm-down > a')).click();
    var apiKey = await driver.manage().getCookie('ncp');

    console.log(apiKey.value);

    const option = {
        uri: 'https://monitoring-api.ncloud.com/monapi/pfmnc',
        method: 'POST',
        headers : {
            'X-NCP-access-token' : apiKey.value
        },
        body: {
            "targets": [
                { 
                    "metric": "avg.svr.cpu.used.rto",
                    "name": "avg.svr.cpu.used.rto____0", 
                    "key": "F2:20:CD:AD:38:85", 
                    "startTime": "202010191159", 
                    "endTime": "202010191259" }
                ]
        },
        json: true
    }
    request.post(option, function (error, response, body) {
        console.log(response.body.csv);
    });


    // console.log(html)
}
example();