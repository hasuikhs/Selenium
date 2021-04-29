const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const request = require('request');
// npm i chromedriver@version
// 위 명령어를 실행하면 chromedriver를 따로 받지 않아도 됨 단 버전은 정해야함
require('chromedriver');

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


(async function example(userid, userpw) {
    // let options = new chrome.Options().setChromeBinaryPath('path')  // 리눅스나 mac의 경우 chrome이 설치된 path 지정 보통 /opt/google/chrome/chrome
    let options = new chrome.Options();

    // chrome dirver options 설정
    options.addArguments('--headless');
    options.addArguments('--no-sandbox');
    options.addArguments('--disabled-gpu');
    options.addArguments('--disabled-dev-shm-usage');

    let driver = await new Builder().forBrowser('chrome').setChromeOptions(options).build();

    // timeout 지정
    // 로딩을 마냥 기다릴수 없을때에 설정
    driver.manage().setTimeouts({
        implicit: 5000, // 요소를 찾을 때 로케이터를 기다리는 시간 기본값은 0 ms
        pageLoad: 5000, // 페이지 로딩이 완료될때까지 최대 시간 기본값은 300,000 ms 5minute
        script: 5000 // 스크립트가 실행되기를 기다리는 시간 설정 기본값은 30,000 ms, null로 설정시 무한초 대기
    });

    var parse_url = 'https://sample.com'

    // 페이지 이동
    await driver.get(parse_url);

    // input 입력
    await driver.findElement(By.id('username')).sendKeys(userid);
    await driver.findElement(By.id('passwordPlain')).sendKeys(userpw, Key.RETURN);

    // 페이지 로딩을 sleep으로 기다리기
    await driver.sleep(5000);

    // html element source 가져오기
    var html = await driver.getPageSource();

    // 현재 페이지 url 반환
    var url = await driver.getCurrentUrl();

    // 요소를 찾을 때 시간을 계속 기다리지 않고 0.5초마다 확인하고 요소가 찾아진다면 바로 실행 explicit wait (ms)
    var explicitTimeWait = 5000;
    await driver.wait(until.elementLocated(By.css('#btn')), explicitTimeWait).click();


    // driver 종료
    await driver.quit();
})();