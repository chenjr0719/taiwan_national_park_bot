import os
import re
import time

from bs4 import BeautifulSoup
from requests import Response, Session

from tnpb.logger import error_logger, logger
from tnpb.ocr import get_verify_code


class TNPBot:
    def __init__(self):
        self.session = Session()
        self.url = "https://npm.cpami.gov.tw"
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )

    def _get_default_inputs(self, soup):
        return {
            tag.get("name"): tag.get("value")
            for tag in soup.findAll("input", {"name": re.compile("^__")})
        }

    def get_verify_image(self):
        """
        Download the verify image
        :return: The bytestring of verify image
        :rtype: bytes
        """

        resp = self.session.get(self.url + "/CheckImageCode.aspx")
        verify_image = resp.content.split(b"\r\n\r\n")[0]

        return verify_image

    def send_query(self, id: str, email: str, retry: int = 3):
        """
        Send query

        :param str id: The ID for query
        :param str email: The email for query
        """

        while retry > 0:
            # Enter query page
            resp = self.session.get(self.url + "/apply_2_1.aspx")

            soup = BeautifulSoup(resp.text, "html.parser")

            verify_image = self.get_verify_image()
            verify_code = get_verify_code(verify_image)

            # Generate form data
            data = {
                "ctl00$txSerch": "",
                "ctl00$ContentPlaceHolder1$apply_nation": "中華民國",
                "ctl00$ContentPlaceHolder1$apply_sid": id,
                "ctl00$ContentPlaceHolder1$apply_email": email,
                "ctl00$ContentPlaceHolder1$vcode": verify_code,
                "ctl00$ContentPlaceHolder1$btnappok": "確定",
            }

            data.update(self._get_default_inputs(soup))

            # Send query
            resp = self.session.post(self.url + "/apply_2_1.aspx", data=data)

            # Get query result
            resp = self.session.get(self.url + "/apply_2_3.aspx")

            soup = BeautifulSoup(resp.text, "html.parser")
            table = soup.find("table", {"class": "DATAM"})
            first_row = table.findAll("tr")[1]

            first_col = first_row.find("td")
            if first_col.text == "尚無查詢結果":
                if retry > 1:
                    logger.warning("No query result, retry...")
                else:
                    logger.error("No query result")
            else:
                return resp

            retry -= 1
            time.sleep(5)

        return None

    def get_query_result(self, id: str, email: str, target: int = 1):
        """
        Send query and get the query result

        :param str id: The ID for query
        :param str email: The email for query
        """

        resp = self.send_query(id, email)

        if not resp:
            error_logger.error("No result found. Exit")
            exit(1)

        soup = BeautifulSoup(resp.text, "html.parser")

        table = soup.find("table", {"class": "DATAM"})
        header = table.findAll("tr")[0]
        target_row = table.findAll("tr")[target]

        header = "\t".join([tag.text for tag in header.findAll("th")])
        result = "\t".join([tag.text for tag in target_row.findAll("td")])

        logger.info(f"Found result:\n{header}\n{result}")

        data = {
            row_data.get("name"): row_data.get("value")
            for row_data in target_row.findAll("input")
        }
        data.update(self._get_default_inputs(soup))
        data.update(
            {"ctl00$txSerch": ""}
        )

        headers = self.session.headers
        headers.update({"Referer": "https://npm.cpami.gov.tw/apply_2_3.aspx"})
        resp = self.session.post(
            self.url + "/apply_2_3.aspx", data=data, headers=headers
        )

        return resp

    def send_application(self, resp: Response):
        """
        Send application

        :return: Serial number
        :rtype: str
        """

        verify_image = self.get_verify_image()
        verify_code = get_verify_code(verify_image)

        soup = BeautifulSoup(resp.text, "html.parser")

        data = {
            tag.get("name"): tag.get("value")
            for tag in soup.findAll("input", {"name": re.compile("^ctl00")})
            if "btn" not in tag.get("name")
        }

        data.update(self._get_default_inputs(soup))

        selected = {
            select_tag.get("name"): select_tag.find(
                "option", {"selected": "selected"}
            ).get("value")
            for select_tag in soup.findAll("select", {"name": re.compile("^ctl00")})
            if select_tag.find("option", {"selected": "selected"})
        }
        data.update(selected)

        data.update(
            {
                "ctl00$ScriptManager1": "ctl00$ScriptManager1|ctl00$ContentPlaceHolder1$btnsave",
                "ctl00$txSerch": "",
                "ctl00$ContentPlaceHolder1$note_user": "",
                "ctl00$ContentPlaceHolder1$vcode": verify_code,
                "__ASYNCPOST": True,
                "ctl00$ContentPlaceHolder1$btnsave": "\u78BA\u8A8D\u9001\u51FA",
            }
        )

        resp = self.session.post(self.url + "/apply_1_3.aspx", data=data)

        soup = BeautifulSoup(resp.text, "html.parser")
        serial_pattern = re.compile(r"(?<=serial=)S\d+")
        script = soup.find("script", text=serial_pattern)
        serial_num = serial_pattern.search(script.prettify()).group()

        logger.info(f"Send application success. Serial number: {serial_num}")

        return serial_num
