import pytest
from niweiming.src.testrequests import Apiclient


VALID_USERNAME = 'admin'
VALID_PASSWORD = 'HM_2023_test'
CODE = 2

class Testlogin:

    # 准备夹具
    @pytest.fixture(scope="function")
    def client(self):
        client = Apiclient()
        yield client
        client.close()

    @pytest.fixture(scope="function")
    def captcha_info(self,client):
        # 获取验证码
        response = client.get_captcha()
        assert response.status_code == 200
        data = response.json()
        uuid = data["uuid"]
        return {"uuid": uuid}

    def test_login_success(self,client:Apiclient,captcha_info:dict):
        """用例1（正向）：正确用户名 + 正确密码 + 正确验证码 → 登录成功。"""
        uuid = captcha_info["uuid"]
        response = client.login(username=VALID_USERNAME,password=VALID_PASSWORD,code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["msg"] == "操作成功"
        assert "token" in data
        assert data["token"] is not None and data["token"] != ""

        print(f"登陆成功，token：{data['token']}")

    def test_login_Nullusername(self,client:Apiclient,captcha_info:dict):
        """用例2（反向）：用户名为空 + 正确密码 + 正确验证码 → 登录失败。"""
        uuid= captcha_info["uuid"]
        response = client.login(username="",password=VALID_PASSWORD,code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("用户名为空测试通过")


    def test_login_Nullpassword(self,client:Apiclient,captcha_info:dict):
        """用例3（反向）：正确用户名 + 错误为空 + 正确验证码 → 登录失败。"""
        uuid= captcha_info["uuid"]
        response = client.login(username=VALID_USERNAME,password="",code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("密码为空测试通过")

    def test_login_Nulluuid(self,client:Apiclient,captcha_info):
        """用例4（反向）：正确用户名 + 错误密码 + 验证码为空 → 登录失败。"""
        uuid = ""
        response = client.login(username=VALID_USERNAME,password=VALID_PASSWORD,code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "验证码已失效"
        print("uuid验证码为空测试通过")

    def test_login_failusername(self,client:Apiclient,captcha_info:dict):
        """用例5（反向）：用户名错误 + 正确密码 + 正确验证码 → 登录失败。"""
        uuid= captcha_info["uuid"]
        response = client.login(username="sss",password=VALID_PASSWORD,code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("用户名错误测试通过")


    def test_login_failpassword(self,client:Apiclient,captcha_info:dict):
        """用例6（反向）：正确用户名 + 错误错误 + 正确验证码 → 登录失败。"""
        uuid= captcha_info["uuid"]
        response = client.login(username=VALID_USERNAME,password="123",code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "用户不存在/密码错误"
        print("密码错误测试通过")

    def test_login_failuuid(self,client:Apiclient,captcha_info):
        """用例7（反向）：正确用户名 + 错误密码 + 验证码错误 → 登录失败。"""
        uuid = "aaa"
        response = client.login(username=VALID_USERNAME,password=VALID_PASSWORD,code=CODE,uuid=uuid)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 500
        assert data["msg"] == "验证码已失效"
        print("uuid验证码错误测试通过")