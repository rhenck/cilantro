const e = require("../util/elements");
const message = require('../modules/messages');
const EC = protractor.ExpectedConditions;

const subobject = function() {

    this.goToSubObject = docNr => browser.get(browser.baseUrl)
        .then(e.start.startBtn.click)
        .then(e.documents.treeViewItemsTopLevel.get(docNr).all(by.css('.load')).first().click)
        .then(message.waitForMessage)
        .then(e.documents.proceedBtn.click)
        .then(e.overview.proceedBtn.click);

    this.getRowTitles = () => new Promise((resolve, reject) =>
        e.subobject.tableRows
            .then(rows => Promise.all(rows.map(row => row.all(by.css("td")).get(0).getText()))
                .then(resolve).catch(reject)));

    this.getRowContent = title => new Promise((resolve, reject) =>
        this.getRowTitles()
            .then(titles => e.subobject.tableRows.get(titles.indexOf(title)))
                .then(resolve).catch(reject));
};

module.exports = new subobject();