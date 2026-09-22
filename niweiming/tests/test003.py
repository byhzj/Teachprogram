import requests

#=========第一步：发请求=========
base_url = "https://kdtx-test.itheima.net"
url = base_url+"/api/captchaImage"


#=========第二步：定义请求头=============
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
    "Content-Type":"application/json",
    "referer":"https://kdtx-test.itheima.net",

}

#=========第三步：发送请求=============
response = requests.get(url,headers=headers)

#========第四步：接受请求=========
#查看状态码
print("="*50)
print("状态码",response.status_code)
print("响应头",response.headers)
print("响应内容",response.text[:200])
print("json数据",response.json())

#==========如果返回请求为200======
print("="*50)
if response.status_code==200:
    try:
        data = response.json()
        print("json数据",data)

        #从字典提取字段
        code = data["code"]
        uuid = data["uuid"]

        print(f"验证文字：{code}")
        print(f"验证码：{uuid}")

    except Exception as e:
        print("json解析失败")

else:
    print(f"请求失败，状态码：{response.status_code}")


#=============登录===============
login_url = base_url+"/api/login"

data_login = {
    "username": "admin",
    "password": "HM_2023_test",
    "code": "2",
    "uuid": uuid
}

response_login = requests.post(login_url,json=data_login,headers=headers)

#查看状态码
print("="*50)
print("状态码",response_login.status_code)

if response_login.status_code==200:
    response_result = response_login.json()
    if response_result.get("code")==200:

        login_code = response_result.get("code")
        login_msg = response_result.get("msg")
        login_token = response_result.get("token")
        print(response_login.text)

        print("操作成功",response_login.status_code)
        print("code是：",login_code)
        print("msg是：",login_msg)
        print("token是：",login_token)
    else:
        print("访问失败",response_login.status_code)





