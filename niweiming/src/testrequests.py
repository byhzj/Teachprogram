import requests


class Apiclient():
    base_url = "https://kdtx-test.itheima.net"

    def __init__(self,timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
                "Content-Type":"application/json",
                "referer":"https://kdtx-test.itheima.net",
            }

    def get_captcha(self):
        url = self.base_url + "/api/captchaImage"
        try:
            response = self.session.get(url,headers=self.headers,timeout=self.timeout)
            return response
        except requests.exceptions.RequestException as e:
            print(f"获取验证码请求失败: {e}")
            return None
        except ValueError as e:
            print(f"获取验证码返回数据失败: {e}")
            return None

    def login(self,username,password,code,uuid):
        url = self.base_url + "/api/login"
        data = {
            "username":username,
            "password":password,
            "code":code,
            "uuid":uuid
        }
        response = self.session.post(url,json=data,headers=self.headers)
        data = response.json()
        token = data.get("token")
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
            print("登录成功，Token 已保存")
        return response

    def close(self):
        self.session.close()