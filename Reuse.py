# def __init__(self, user_credentials=None, paymentHash=None, merchantCodesHash=None, cmnMobileSdk=None,
#              detailsForMobileSdk=None, key=None, surl=None, furl=None, curl=None, txnid=None, amount=None,
#              productinfo=None, firstname=None, email=None, udf1=None, udf2=None, offer_key=None, ccnum=None,
#              ccname=None, ccvv=None, ccexpmon=None, ccexpyr=None, store_card_token=None, appVersion=None,
#              paymentUrl=None, pg=None, bankcode=None, hash=None, paymentGateway=None, store_card=None):
import base64
import json
import random

import requests
from fastapi import Response
from sqlalchemy.orm import Session

import models


class CoreReusable:
    def __init__(self, **words):
        map = {}
        for arg in words:
            map[arg] = words[arg]
        print(str(map))
        self.map = map
        # return map

    def val(self, db):
        return CoreReusable.set_payment_dto_payu(self, self.map, db)

    def set_payment_dto_payu(self, req, db: Session):
        core = req
        newPaymentInfo = models.Core(**core)
        db.add(newPaymentInfo)
        db.commit()
        db.refresh(newPaymentInfo)
        return self.map

    def get_success(self, orderid, db: Session):
        response = requests.get("http://0.0.0.0:8000/payu/form/" + orderid + "/verify_payment")
        orderData = None
        orderData = db.query(models.payu).filter(models.payu.txnid == orderid).first()
        if orderData is None:
            return 'No Record Found'
        else:
            orderData.status = 'SUCCESS'
        db.commit()
        return orderid

    def get_succ(self, orderid):
        return "http://0.0.0.0:8000/items/" + orderid

    def updatePaymentStatus(self, txnid, success, db):
        num1 = random.randint(10000000000000000000000, 99999999999999999999999)
        orderData = None
        orderData = db.query(models.payu).filter(models.payu.txnid == txnid).first()
        url = ''
        if orderData is None:
            return 'No Record Found'
        else:
            if success.casefold() == 's':
                orderData.status = 'success'
                orderData.unmappedstatus = 'captured'
                orderData.error_Message = 'NO ERROR'
                orderData.error_code = 'E000'
                orderData.field9 = 'SUCCESS|Completed Using Callback'
                orderData.mihpayid = str(num1)
                url = orderData.surl
            elif success.casefold() == 'd':
                orderData.status = 'failure'
                orderData.unmappedstatus = 'dropped'
                orderData.error_Message = 'Bank was unable to authenticate.'
                orderData.error_code = 'E501'
                orderData.field9 = 'Marked dropped as transaction has timed out'
                orderData.mihpayid = str(num1)
                url = orderData.surl
            elif success.casefold() == 'b':
                orderData.status = 'failure'
                orderData.unmappedstatus = 'bounced'
                orderData.error_Message = 'NO ERROR'
                orderData.error_code = 'E408'
                orderData.field9 = 'Marked bounced as transaction has timed out'
                orderData.mihpayid = str(num1)
                url = orderData.surl
            elif success.casefold() == 'c':
                orderData.status = 'failure'
                orderData.unmappedstatus = 'userCancelled'
                orderData.error_Message = 'Transaction interrupted by pressing back button'
                orderData.error_code = 'E1206'
                orderData.field9 = 'User interrupted by pressing back button'
                orderData.mihpayid = str(num1)
                url = orderData.surl
            elif success.casefold() == 'pd':
                orderData.status = 'Not Found'
                orderData.unmappedstatus = ''
                orderData.error_Message = ''
                orderData.error_code = ''
                orderData.field9 = ''
                orderData.status_code = '0'
                orderData.mihpayid = str(num1)
                url = orderData.surl
            elif success.casefold() == 'i':
                orderData.status = 'pending'
                orderData.unmappedstatus = 'initiated'
                orderData.error_Message = 'User initiated'
                orderData.error_code = 'E000'
                orderData.field9 = 'User initiated'
                orderData.mihpayid = str(num1)
                url = orderData.surl
            elif success.casefold() == 'p':
                orderData.status = 'pending'
                orderData.unmappedstatus = 'in progress'
                orderData.error_Message = ''
                orderData.error_code = ''
                orderData.field9 = ''
                orderData.mihpayid = str(num1)
                url = orderData.surl
            else:
                orderData.status = 'failure'
                orderData.unmappedstatus = 'failed'
                orderData.error_Message = 'Transaction declined due to invalid expiry or cvv details'
                orderData.error_code = 'E1632'
                orderData.field9 = 'Transaction declined due to invalid expiry or cvv details'
                orderData.mihpayid = str(num1)
                url = orderData.furl
        db.commit()
        # return fastapi.responses.RedirectResponse(url=url, status_code=303)
        return url

    def paymentResponseV2(self, key=None, command=None, var1=None, hash=None, db=None):
        num1 = random.randint(10000000000000000000000, 99999999999999999999999)
        orderData = db.query(models.payu).filter(models.payu.txnid == var1).first()
        if orderData is None:
            return {"status": "fail"}
        else:
            response = {
                "status": orderData.status_code,
                "msg": "1 out of 1 Transactions Fetched Successfully"
            }
            transaction_details = \
                {
                    "addedon": str(orderData.created),
                    "disc": "0.00",
                    "mode": str(orderData.pg),
                    "udf2": str(orderData.udf2),
                    "udf1": str(orderData.udf1),
                    "additional_charges": "0.00",
                    "field9": orderData.field9,
                    "bankcode": str(orderData.bankcode),
                    "transaction_amount": orderData.amount,
                    "unmappedstatus": orderData.unmappedstatus,
                    "net_amount_debit": str(int(float(orderData.amount))),
                    "txnid": var1,
                    "status": orderData.status,
                    "error_Message": orderData.error_Message,
                    "error_code": orderData.error_code,
                    "firstname": "dummy",
                    "productinfo": var1,
                    "bank_ref_num": str(num1),
                    "amt": orderData.amount,
                    "request_id": "",
                    "card_type": "MAST",
                    "mihpayid": str(num1)
                }
            transaction = {str(var1): transaction_details}
            response['transaction_details'] = transaction
            resp = json.dumps(response)
            # print(response)
            return response

    def paymentResponseV2Upi(self, txnid, db):
        orderData = db.query(models.payu).filter(models.payu.txnid == txnid).first()
        url = {"status": orderData.status,
               "result": {"mihpayid": orderData.mihpayid, "mode": orderData.pg, "status": orderData.status,
                          "key": orderData.key,
                          "txnid": orderData.txnid, "amount": orderData.amount, "addedon": str(orderData.created),
                          "productinfo": orderData.txnid, "firstname": "dummy", "lastname": "", "address1": "",
                          "address2": "", "city": "", "state": "", "country": "", "zipcode": "",
                          "email": "void@payu.com",
                          "phone": "9999999999", "udf1": str(orderData.udf1), "udf2": str(orderData.udf2), "udf3": "",
                          "udf4": "", "udf5": "",
                          "udf6": "", "udf7": "", "udf8": "", "udf9": "", "udf10": "", "card_token": "", "card_no": "",
                          "field0": "", "field1": orderData.vpa, "field2": "", "field3": "", "field4": "ASHOK TAK",
                          "field5": "", "field6": "", "field7": "", "field8": "",
                          "field9": "Transaction Initiated Successfully", "payment_source": "payuPureS2S",
                          "PG_TYPE": "UPI-PG", "error": orderData.error_code, "error_Message": orderData.error_Message,
                          "net_amount_debit": "0",
                          "discount": "0.00", "offer_key": "", "offer_availed": "", "unmappedstatus": "in progress",
                          "hash": orderData.hash,
                          "bank_ref_no": "", "bank_ref_num": "", "bankcode": orderData.pg,
                          "surl": orderData.surl,
                          "curl": orderData.curl,
                          "furl": orderData.furl}}
        user_encode_data = json.dumps(url).encode('utf-8')
        base64_bytes = base64.b64encode(user_encode_data)
        base64_string = base64_bytes.decode("ascii")

        if orderData is None:
            return 'No Record Found'
        else:
            # if orderData.status == 'success':
            return Response(content=base64_string, media_type="text/plain")

    def addPaymentSplit(self, db: Session):
        orderData = db.query(models.payu).filter(models.payu.txnid == self.map['merchantTransactionId']).first()
        orderData.merchantKey = self.map['merchantKey']
        orderData.merchantTransactionId = self.map['merchantTransactionId']
        orderData.totalAmount = self.map['totalAmount']
        orderData.totalDiscount = self.map['totalDiscount']
        orderData.jsonSplits = self.map['jsonSplits']
        db.commit()
        return self.map