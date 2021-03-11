require('dotenv').config({path: '../.env'});
const { Scrapper } = require('./class/Scrapper');
const { getYesterdayDate } = require('./functions/common');

(async () => {

    let target = new Scrapper();
    let waitTime = 20000;

    await target.moveSite('target site');
    await target.login('idElementName', 'pwElementName', process.env.id, process.env.pw);

})()