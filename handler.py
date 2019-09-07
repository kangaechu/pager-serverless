import json
import os
import boto3
import requests

sns = boto3.client('sns')


def encode(event, context):
    message_digits = event['Details']['ContactData']['Attributes']['MessageDigits']
    print("message_digits:", message_digits)
    message_text = encode_pager(message_digits)
    print("message text:", message_text)

    # publish_sns_topic(os.environ['SNS_TOPIC'], message_text, '')
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    send_slack(message_text, webhook_url)
    body = {
        "messageText": encode_pager(message_digits),
        "messageDigits": message_digits
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body, ensure_ascii=False)
    }
    return response


def encode_pager(message_digits):
    pager_table = {
        "11": "ア", "12": "イ", "13": "ウ", "14": "エ", "15": "オ", "16": "Ａ", "17": "Ｂ", "18": "Ｃ", "19": "Ｄ", "10": "Ｅ",
        "21": "カ", "22": "キ", "23": "ク", "24": "ケ", "25": "コ", "26": "Ｆ", "27": "Ｇ", "28": "Ｈ", "29": "Ｉ", "20": "Ｊ",
        "31": "サ", "32": "シ", "33": "ス", "34": "セ", "35": "ソ", "36": "Ｋ", "37": "Ｌ", "38": "Ｍ", "39": "Ｎ", "30": "Ｏ",
        "41": "タ", "42": "チ", "43": "ツ", "44": "テ", "45": "ト", "46": "Ｐ", "47": "Ｑ", "48": "Ｒ", "49": "Ｓ", "40": "Ｔ",
        "51": "ナ", "52": "ニ", "53": "ヌ", "54": "ネ", "55": "ノ", "56": "Ｕ", "57": "Ｖ", "58": "Ｗ", "59": "Ｘ", "50": "Ｙ",
        "61": "ハ", "62": "ヒ", "63": "フ", "64": "ヘ", "65": "ホ", "66": "Ｚ", "67": "？", "68": "！", "69": "ー", "60": "／",
        "71": "マ", "72": "ミ", "73": "ム", "74": "メ", "75": "モ", "76": "¥", "77": "＆", "78": "", "79": "☎️", "70": "",
        "81": "ヤ", "82": "（", "83": "ユ", "84": "）", "85": "ヨ", "86": "＊", "87": "＃", "88": " ", "89": "❤️", "80": "",
        "91": "ラ", "92": "リ", "93": "ル", "94": "レ", "95": "ロ", "96": "１", "97": "２", "98": "３", "99": "４", "90": "５",
        "01": "ワ", "02": "ヲ", "03": "ン", "04": "＂", "05": "", "06": "６", "07": "７", "08": "８", "09": "９", "00": "０"
    }
    it = iter(message_digits)
    return "".join([pager_table[i + next(it)] for i in it])


def publish_sns_topic(topic_arn, message, subject):
    request = {
        'TopicArn': topic_arn,
        'Message': message,
        'Subject': subject
    }
    response = sns.publish(**request)
    return response


def send_slack(message, webhook_url):
    payload = {
        "text": message,
    }

    data = json.dumps(payload)

    requests.post(webhook_url, data)


if __name__ == "__main__":
    print(encode_pager("123456"))
