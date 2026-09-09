
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');
const html = fs.readFileSync('d:/dbmss/templates/delivery_dashboard.html', 'utf8');
const virtualConsole = new jsdom.VirtualConsole();
virtualConsole.on('error', (err) => { console.error('ERROR:', err); });
virtualConsole.on('jsdomError', (err) => { console.error('JSDOM ERROR:', err); });
const dom = new JSDOM(html, { runScripts: 'dangerously', virtualConsole });
dom.window.addEventListener('load', () => {
    try {
        dom.window.switchTab('tracking', dom.window.document.querySelector('.nav-link'));
        console.log('Success');
    } catch(e) {
        console.log('Exception in switchTab:', e);
    }
});
