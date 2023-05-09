# Robot to enter weekly sales data into the RobotSpareBin Industries Intranet.

import os

from Browser import Browser, SupportedBrowsers
from Browser.utils.data_types import SelectAttribute
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import csv

browser = Browser()


def open_the_intranet_website():
    browser.open_browser(
        "https://robotsparebinindustries.com/#/robot-order", SupportedBrowsers.chromium, False, True)


def download_the_csv_file():
    http = HTTP()
    http.download(
        url="https://robotsparebinindustries.com/orders.csv",
        overwrite=True)


def close_modal_popup():
    browser.click("text=OK")


def fill_and_submit_the_order(order):
    orderNum = order["Order number"]
    browser.select_options_by(
        "id=head",
        SelectAttribute["value"],
        str(orderNum))
    bodyNum = order["Body"]
    browser.click(f"id=id-body-{bodyNum}")
    browser.type_text("xpath=//input[@type='number']", order["Legs"])
    browser.type_text("id=address", str(order["Address"]))

    browser.click("id=preview")
    robotImage = f"{os.getcwd()}/output/robot-for-order-number-{orderNum}.png"

    browser.take_screenshot(filename=robotImage,
                            selector="id=robot-preview-image")

    browser.click("id=order")
    receiptImage = f"{os.getcwd()}/output/receipt-for-order-number-{orderNum}.png"
    browser.take_screenshot(filename=receiptImage,
                            selector="id=receipt")

def fill_the_form_using_the_data_from_the_csv_file():
    with open(f"{os.getcwd()}/orders.csv", mode='r')as file:
        csvFile = csv.DictReader(file)

        for order in csvFile:
            fill_and_submit_the_order(order)
            browser.click("id=order-another")
            close_modal_popup()

def log_out():
    browser.click("text=Log out")

def main():
    try:
        open_the_intranet_website()
        close_modal_popup()
        download_the_csv_file()
        fill_the_form_using_the_data_from_the_csv_file()
    finally:
        log_out()
        browser.playwright.close()


if __name__ == "__main__":
    main()
