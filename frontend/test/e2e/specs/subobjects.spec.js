const e = require("../modules/elements");
const so = require('../modules/subobject');
const EC = protractor.ExpectedConditions;

describe('subobject view', () => {

    it('should select article', () => {
        so.goToSubObject(3);
        browser.wait(EC.visibilityOf(e.subobject.add), 20000);
        e.subobject.selectBtn.click();
        e.subobject.select.get(1).click();
        const cell = so.getRowContent("title");
        const input = cell.element(by.css("input"));
        expect(input.getAttribute("value")).toEqual("UNITED");
    });


    it('should move dismissed article to trash', () => {
        so.goToSubObject(3);
        browser.wait(EC.visibilityOf(e.subobject.add), 20000);
        e.subobject.selectBtn.click();
        e.subobject.select.get(1).click();
        e.subobject.dismissBtn.click();
        const cell = so.getRowContent("title");
        const input = cell.element(by.css("input"));
        expect(input.getAttribute("value")).toEqual("");
        expect(e.subobject.select.count()).toEqual(2);
        expect(e.subobject.trash.count()).toEqual(1);
    });

    it('should create new article', () => {
        so.goToSubObject(2);
        browser.wait(EC.visibilityOf(e.subobject.add), 20000);
        e.subobject.add.click();
        const cell = so.getRowContent("title")
        const input = cell.element(by.css("input"));
        expect(input.getAttribute("value")).toEqual("Article 2");
        expect(e.subobject.select.count()).toEqual(2);
    });

    it('should restore article from trash', () => {
        so.goToSubObject(2);
        browser.wait(EC.visibilityOf(e.subobject.dismissBtn), 20000);
        e.subobject.dismissBtn.click();
        e.subobject.trashBtn.click();
        e.subobject.trash.get(0).click();
        expect(e.subobject.select.count()).toEqual(0);
        // e.subobject.undelete.click();
        // expect(e.subobject.select.count()).toEqual(1);
    });

    it('should only confirm validated article', () => {
        so.goToSubObject(2);
        browser.wait(EC.visibilityOf(e.subobject.table), 20000);
        const cell = so.getRowContent("title");
        const input = cell.element(by.css("input"));
        input.clear();
        expect(e.subobject.confirmBtn.isDisplayed()).toBeFalsy();
        input.sendKeys("shit");
        expect(e.subobject.confirmBtn.isDisplayed()).toBeTruthy();
    });

});
