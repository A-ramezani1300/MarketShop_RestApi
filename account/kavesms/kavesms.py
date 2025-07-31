from kavenegar import *
from urllib.error import HTTPError


def send_sms_with_template(receptor, tokens: dict, template):
    """
        sending sms that needs template
    """
    try:
        api = KavenegarAPI(
            'کلید api'
            # کلید api خود را در استرینگ بالا جایگزاری بکنید
        )
        params = {
            'receptor': receptor,
            'template': template,
        }
        for key, value in tokens.items():
            params[key] = value

        response = api.verify_lookup(params)
        print(response)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPError as e:
        print(e)
        return False


def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI(
            'کلید api')
        # کلید api خود را در استرینگ بالا جایگزاری بکنید
        params_buyer = {
            'receptor': receptor,
            'message': f'محصول {str(product)} به سبد خرید شما اضافه شد',  # message,
            'sender': '2000500666'
        }
        response = api.sms_send(params_buyer)
        print(response)
    except APIException as e:
        print(e)
    except HTTPError as e:
        print(e)
