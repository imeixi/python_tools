#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import traceback
import pyotp
from qrcode import QRCode, constants


class GoogleAuthenticatorClient:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key

    """ 
    生成google auth 需要的密钥 
    :return: 
    """
    def create_secret(self):
        self.secret_key = pyotp.random_base32(64)
        return self.secret_key

    """ 
    根据用户名及密钥生成二维码图片 
    :param name:用户名 
    :param issuer_name
    :发行人 :param 
    :save_to_file: 保存至文件 
    :return: 
    """
    def create_secret_qrcode(self, name=None, issuer_name=None, save_to_file=True):
        data = pyotp.totp.TOTP(self.secret_key).provisioning_uri(name=name, issuer_name=issuer_name)
        qr = QRCode(version=1, error_correction=constants.ERROR_CORRECT_L, box_size=6, border=4,)
        try:
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            if save_to_file:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                dir_path = os.path.join(base_dir, 'static', 'image')
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                    filepath = dir_path + os.sep + self.secret_key + '.png'
                img.save(filepath)
                return True, filepath
            else:
                return img.get_image()
        except Exception as e:
            traceback.print_exc()
            return False, None

    def verify_code_func(self, verify_code):
        t = pyotp.TOTP(self.secret_key)
        result = t.verify(verify_code)
        return result


if __name__ == '__main__':
    # secret = 'PU6PY6FWPVQ4BXE7ZP6X7YMVM3BH3ODS7SW53GL3LJPED7AAQUVF2EKP6AGNFFOX'
    # google_auth_ = GoogleAuthenticatorClient(secret_key=secret)
    google_auth_ = GoogleAuthenticatorClient()
    secret = google_auth_.create_secret()
    print(secret)
    image = google_auth_.create_secret_qrcode(name='slp', issuer_name='GoldBull', save_to_file=False)
    print(image.show())

    # 验证
    res = google_auth_.verify_code_func(verify_code='731582')
    print(res)




