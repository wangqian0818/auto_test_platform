"""
收取邮件就是编写一个MUA作为客户端，从MDA把邮件获取到用户的电脑或者手机上.
取邮件最常用的协议是POP协议，目前版本号是3，俗称POP3。
Python内置一个poplib模块，实现了POP3协议，可以直接用来收邮件。
所以，收取邮件分两步：
第一步：用poplib把邮件的原始文本下载到本地；
第二部：用email解析原始文本，还原为邮件对象。
"""
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


def get_email(email,password,pop3_server_host,pop3_server_port):
    try:
        # 链接到POP3服务器
        server = poplib.POP3(pop3_server_host, pop3_server_port)
        # 打开调试，打印出会话内容，可选
        server.set_debuglevel(1)
        # 打印POP3服务器的欢迎文字，可选
        # print(server.getwelcome().decode('utf-8'))

        # 进行身份认证
        server.user(email)
        server.pass_(password)

        # stat() 返回邮件数量和占用空间，返回两个。
        messages, size = server.stat()
        # print('Messages: %s. Size: %s' %(messages, size))

        # list 返回所有邮件编号，第一个是返回状态信息，第二个是列表
        resp, mails, octets = server.list()
        # print("邮件列表",mails)

        # 获取最新一封邮件, 注意索引号从1开始,最后是最新的
        index = len(mails)
        resp, lines, octets = server.retr(index)

        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 解析成massage对象,但是这个 Message 对象本身可能是一个 MIMEMultipart 对象，即包含嵌套的其他 MIMEBase 对象，嵌套可能还不止一层。所以要递归地打印出 Message 对象的层次结构
        msg = Parser().parsestr(msg_content)
        # print(type(msg))    # <class 'email.message.Message'>
        # print(msg)

        # 可以根据邮件索引号直接从服务器删除邮件:
        # server.dele(index)
        # 关闭连接
        server.quit()
        return msg
    except Exception:
        return 0

    # # 解析邮件正文
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

mail_list = []

def print_info(msg, indent=0):
    global mail_list
    if indent == 0:
        for header in ['From', 'To', 'Cc', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            mail_list.append(value)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
            mail_list.append(content)
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
            mail_list.append(content_type)
    return mail_list


if __name__ == "__main__":
    # 获取邮箱密码和对应邮箱POP3服务器
    email = "m53667987@163.com"
    password = "GWCARVNCOYZWYHYB"
    pop3_server_host = "pop.163.com"
    pop3_server_port = 110
    msg = get_email(email,password,pop3_server_host,pop3_server_port)
    print(msg)
    mail_list = print_info(msg)  # 解析
    print(mail_list)