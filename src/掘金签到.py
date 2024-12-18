"""
    @author TJ
    @github https://github.com/devotion-coding/qinglong-script.git
    @described 掘金签到脚本
    觉得不错麻烦点个star谢谢
"""

import requests
import json
import notify
import urllib.parse

# --------------------------------------------------------------------------------------------------------------------
# 自行在浏览器控制台获取
cookies = "填写你的掘金cookie"
# --------------------------------------------------------------------------------------------------------------------
# 下面的不用管理 直接 Fire！！！

# 解析后的cookie
cookies_parsed = {}
# 用户uuid  从cookie中解析
uuid = 0
# 没啥用的字段
aid = 0
# 上下问对象
context = {
    #  签到状态
    "sign_status": False,
    # 连续签到天数
    "cont_count": 0,
    # 总签到天数
    "sum_count": 0,
    # 矿石数量
    "point_count": 0,
    # 日历建议
    "should_or_not": "",
    # 日历格言
    "aphorism": ""
}


# 从cookie的uuid
def parse_uuid():
    if not cookies or cookies == "填写你的掘金cookie":
        print("请在脚本中设置cookie!!!")
        return

    cookie_items = cookies.split(";")
    for item in cookie_items:
        if not item.strip():
            continue
        item_kv = item.split("=")
        if len(item_kv) != 2:
            continue

        key = item_kv[0].strip()
        value = item_kv[1].strip()
        cookies_parsed[key] = value
        if not key.startswith("__tea_cookie_tokens_"):
            continue
        aid = key.replace("__tea_cookie_tokens_", "")
        value = urllib.parse.unquote(value)
        value = urllib.parse.unquote(value)
        value_json = json.loads(value)
        uuid = value_json["user_unique_id"]
    print(f"解析cookie成功! aid={aid}, uuid={uuid}")


# 获取今日签到状态
def get_sign_status():
    api_url = f"https://api.juejin.cn/growth_api/v2/get_today_status?uuid={uuid}"
    response = requests.get(api_url, cookies=cookies_parsed)
    resp_json = json.loads(response.text)
    print(f"查询签到状态响应：{resp_json}")
    resp_code = resp_json["err_no"]
    if resp_code != 0:
        print(resp_json['err_msg'])
        return
    data = resp_json['data']
    context['sign_status'] = data['check_in_done']


# 获取签到天数
def get_sign_count():
    api_url = f"https://api.juejin.cn/growth_api/v1/get_counts?uuid={uuid}"
    response = requests.get(api_url, cookies=cookies_parsed)
    resp_json = json.loads(response.text)
    print(f"查询签到天数响应：{resp_json}")
    resp_code = resp_json["err_no"]
    if resp_code != 0:
        print(resp_json['err_msg'])
        return
    data = resp_json['data']
    context["cont_count"] = data['cont_count']
    context["sum_count"] = data['sum_count']


# 获取矿石数量
def get_point_count():
    api_url = f"https://api.juejin.cn/growth_api/v1/get_cur_point?uuid={uuid}"
    response = requests.get(api_url, cookies=cookies_parsed)
    resp_json = json.loads(response.text)
    print(f"查询矿石总数响应：{resp_json}")
    resp_code = resp_json["err_no"]
    if resp_code != 0:
        print(resp_json['err_msg'])
        return
    data = resp_json['data']
    context["point_count"] = data


# 获取程序员日历
def get_coder_calendar():
    api_url = f"https://api.juejin.cn/growth_api/v1/get_coder_calendar?uuid={uuid}"
    response = requests.get(api_url, cookies=cookies_parsed)
    resp_json = json.loads(response.text)
    print(f"查询日历建议响应：{resp_json}")
    resp_code = resp_json["err_no"]
    if resp_code != 0:
        print(resp_json['err_msg'])
        return
    data = resp_json['data']
    context["aphorism"] = data['aphorism']
    context["should_or_not"] = data['should_or_not']


# 推送消息
def fire():
    # 消息通知模版
    content = f"""
    掘金签到提醒～
        当前签到状态：{context["sign_status"]}
        连续签到天数：{context["cont_count"]}
        累计签到天数：{context["sum_count"]}
        获得矿石总数：{context["point_count"]}
        程序员老黄历：{context["should_or_not"]} -- {context["aphorism"]}
    """
    print(content)
    notify.send("掘金每日签到提醒", content)


if __name__ == '__main__':
    parse_uuid()
    get_sign_status()
    get_sign_count()
    get_point_count()
    get_coder_calendar()
    print(f"上下文构建完成：{context}")
    fire()
