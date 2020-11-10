const { Builder, By, Key, until } = require('selenium-webdriver');
const request = require('request');

const readlineSync = require('readline-sync');
const cron = require('node-cron');
const testff = require('./test');
const message = 'enter password: ';
const options = {
    hideEchoBack: true,
    mask: '*'
};

const id = readlineSync.question('enter id: ');
const answer = readlineSync.question(message, options);


// cron.schedule('*/1 * * * *', () => {
example(id, answer);

console.log(testff.test());

// })

/*
1. npm init -> main에 실행 js 입력
2. npm install nexe -D
3. scripts에 "build": "nexe" 추가
4. npm run build
*/


async function example(userid, userpw) {
    let driver = await new Builder().forBrowser('chrome').build();
    driver.manage().setTimeouts({implicit: 5000, pageLoad: 5000, script: 5000});


    // timeout 지정
    // 로딩을 마냥 기다릴수 없을때에 설정
    driver.manage().setTimeouts({
        implicit: 5000, // 요소를 찾을 때 로케이터를 기다리는 시간 기본값은 0 ms
        pageLoad: 5000, // 페이지 로딩이 완료될때까지 최대 시간 기본값은 300,000 ms 5minute
        script: 5000 // 스크립트가 실행되기를 기다리는 시간 설정 기본값은 30,000 ms, null로 설정시 무한초 대기
    });

    await driver.get('https://auth.ncloud.com/nsa/bizspring');
    await driver.findElement(By.id('username')).sendKeys(userid, Key.RETURN);
    await driver.findElement(By.id('passwordPlain')).sendKeys(userpw, Key.RETURN);

    var html = await driver.getPageSource();

    // var $ = cheerio.load(html);
    // var text = $('#app > div > header > div.center-wrap > div.fr > div.util.hidden-sm-down > a').text();

    // await driver.findElement(By.css('#app > div > header > div.center-wrap > div.fr > div.util.hidden-sm-down > a')).click();
    var apiKey = await driver.manage().getCookie('ncp');
    console.log(apiKey);
    // const option = {
    //     uri: 'https://monitoring-api.ncloud.com/monapi/pfmnc',
    //     method: 'POST',
    //     headers : {
    //         'X-NCP-access-token' : apiKey.value
    //     },
    //     body: {
    //         "targets": [
    //             { 
    //                 "metric": "avg.svr.cpu.used.rto",
    //                 "name": "avg.svr.cpu.used.rto____0", 
    //                 "key": "F2:20:CD:AD:38:85", 
    //                 "startTime": "202010191159", 
    //                 "endTime": "202010191259" }
    //             ]
    //     },
    //     json: true
    // }
    
    request.post(option, function (error, response, body) {
        console.log(response.body.csv);
    });


    // console.log(html)
}