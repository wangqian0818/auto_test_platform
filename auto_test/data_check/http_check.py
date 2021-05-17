from urllib import request
from urllib import parse
import requests,time


#urlencode可以把key-value这样的键值对转换成我们想要的格式，返回的是a=1&b=2这样的字符串
#百度搜索的页面的请求为'http://www.baidu.com/s?wd=',wd为请求搜索的内容
#urlencode遇到中文会自动进行编码转化
#一个参数时可以采用'http://www.baidu.com/s?wd='+keywd的格式，
# 但是当keywd为中文的时候需要用urllib.request.quote(keywd)进行编码转换
def http_get(url, data=None, flag=0):
    print('-------------------')
    print('url={}, \ndata={}, \nflag={}'.format(url,data,flag))
    print('-------------------')
    # data = parse.urlencode(values)
    # response = request.urlopen(f'{url}/s?%s' % data)
    # html = response.read()
    # print(html.decode('utf-8'))
    # file = open(path,'wb')
    # file.write(html)
    # file.close()
    try:
        response = requests.get(url, data, timeout=20)
        if response.status_code == 200:
            if flag == 0:
                context = response.text
                response.raise_for_status() #如果状态不是200，则引发异常
                print('get请求成功')
                return context
            else:
                return response.status_code
        else:
            return response.status_code
    except requests.exceptions.ConnectionError:
        print('get连接出错，请等待3s')
        time.sleep(3)
        return 0
    except requests.exceptions.ChunkedEncodingError:
        print('get：服务器声明了chunked编码但发送了一个无效的chunk：请等待3s')
        return 0
    except requests.exceptions.Timeout:
        print('get请求超时')
        return 0
    except requests.exceptions.InvalidURL:
        print('get：无效的URL')
        return 0
    except Exception as err:
        print('get产生异常,异常原因是:{}'.format(err))
        return 0


def http_post(url, data=None, headers=None, flag=0):
    # data = parse.urlencode(values)
    #     # print(data)
    #     # # data = data.encode('utf-8')
    #     # req = request.Request(url, data)
    #     # req.add_header(header)
    #     # response = request.urlopen(req)
    #     #
    #     # html = response.read()
    #     # # print(html.decode('utf-8'))
    try:
        response = requests.post(url, data, headers, timeout=20)
        if response.status_code == 200:
            if flag == 0:
                context = response.text
                response.raise_for_status()  # 如果状态不是200，则引发异常
                # print(response.request)
                # print(response.headers)
                print('post请求成功')
                return context
            else:
                return response.status_code
        else:
            return response.status_code
    except requests.exceptions.ConnectionError:
        print('post连接出错，请等待3s')
        time.sleep(3)
        return 0
    except requests.exceptions.ChunkedEncodingError:
        print('post：服务器声明了chunked编码但发送了一个无效的chunk：请等待3s')
        return 0
    except requests.exceptions.Timeout:
        print('post请求超时')
        return 0
    except requests.exceptions.InvalidURL:
        print('post：无效的URL')
        return 0
    except Exception as err:
        print('post产生异常,异常原因是:{}'.format(err))
        return 0

if __name__ == '__main__':
    url = 'http://10.10.88.55:2287'
    data1 = "abc"
    data = {'data': 'test'}
    # path = 'C:/Users/admin/Desktop/1.html'
    #指定content-type类型是post的上传功能，post的下载只能是放在uri的后缀curl http://10.10.88.9:2286/1.pdf -v
    #MIME类型主要是限制用户下载的内容，请求MIME类型只能是get请求，post对请求文件没有动态处理能力，只有请求.php文件才可以进行处理
    # headers = {'Content-Type': 'application/txt'}
    a=http_get(url,flag=1)
    content = http_get(url)
    b=http_post(url,flag=1)
    print(content)
    print(b)