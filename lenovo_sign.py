#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import base64


def sign(username, password):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/103.0.5060.42",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    # 获取leid和JSESSIONID
    session.get(url="https://reg.lenovo.com.cn/auth/rebuildleid", headers=headers)
    session.get(
        url="https://reg.lenovo.com.cn/auth/v1/login?ticket=5e9b6d3d-4500-47fc-b32b-f2b4a1230fd3&ru=https%3A%2F%2Fmclub.lenovo.com.cn%2F"
    )
    data = f"account={username}&password={base64.b64encode(str(password).encode()).decode()}&ps=1&ticket=5e9b6d3d-4500-47fc-b32b-f2b4a1230fd3&codeid=&code=&slide=v2&applicationPlatform=2&shopId=1&os=web&deviceId=BIT%2F8ZTwWmvKpMsz3bQspIZRY9o9hK1Ce3zKIt5js7WSUgGQNnwvYmjcRjVHvJbQ00fe3T2wxgjZAVSdOYl8rrQ%3D%3D&t=1655187183738&websiteCode=10000001&websiteName=%25E5%2595%2586%25E5%259F%258E%25E7%25AB%2599&forwardPageUrl=https%253A%252F%252Fmclub.lenovo.com.cn%252F"
    # login
    login_response = session.post(
        url="https://reg.lenovo.com.cn/auth/v2/doLogin", headers=headers, data=data
    )
    if login_response.json().get("ret") == "1":
        print("账号或密码错误")
        return
    # 获取签到token
    res = session.get(url="https://mclub.lenovo.com.cn/signlist/")
    token = re.findall('token\s=\s"(.*?)"', res.text)[0]
    data = {"_token": token, "memberSource": 0}
    sign_response = session.post(url="https://mclub.lenovo.com.cn/signadd", data=data)
    sign_days = (
        session.get(url="https://mclub.lenovo.com.cn/getsignincal")
        .json()
        .get("signinCal")
        .get("continueCount")
    )
    if sign_response.json().get("success"):
        print(f"账号{username}签到成功！总共签到天数为{sign_days}")
    else:
        print(f"账号{username}今天已经签到！总共签到天数为{sign_days}")
    session.close()


if __name__ == "__main__":
    username=""
    password=""
    sign(username, password)
