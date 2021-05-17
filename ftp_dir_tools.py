#! /usr/bin/python # -*- coding: utf-8 -*
# import unittest # 单元测试用例
import logging
import os
import time
import traceback
from ftplib import FTP  # 定义了FTP类，实现ftp上传和下载

FTP_PERFECT_BUFF_SIZE = 8192


def ftpconnect(host, username, password, port):
    try:
        ftp = FTP()
        # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
        ftp.connect(host, port)  # 连接
        ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
        print('--------- ftp连接成功：host[{}]-port[{}]-username[{}]-password[{}]'.format(host, port, username, password))
        return ftp
    except Exception as err:
        print('========= ftp连接失败：', err)


# 检查是否下载/上传完整
def is_same_size(ftp=None, local_file=None, remote_file=None):
    """判断远程文件和本地文件大小是否一致

       参数:
         local_file: 本地文件
         remote_file: 远程文件
    """
    try:
        remote_file_size = ftp.size(remote_file)
    except Exception as err:
        logging.debug("get remote file_size failed, Err:%s" % err)
        remote_file_size = -1

    try:
        local_file_size = os.path.getsize(local_file)
    except Exception as err:
        logging.debug("get local file_size failed, Err:%s" % err)
        local_file_size = -1

    # 三目运算符
    result = True if (remote_file_size == local_file_size) else False

    return (result, remote_file_size, local_file_size)


'''
@实际负责上传功能的函数
'''


def upload_file(local_file=None, remote_file=None, ftp=None):
    # 本地是否有此文件
    if not os.path.exists(local_file):
        logging.debug('no such file or directory [%s].'(local_file))
        return False
    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
    if True != result:
        print('--- 远程文件不存在，正在尝试上传... [%s] ' % (remote_file))
        logging.debug('远程文件不存在，正在尝试上传... [%s] ' % (remote_file))
        global FTP_PERFECT_BUFF_SIZE
        bufsize = FTP_PERFECT_BUFF_SIZE
        try:
            with open(local_file, 'rb') as file_handler:
                if ftp.storbinary('STOR ' + remote_file, file_handler, bufsize):
                    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
        except Exception as err:
            logging.debug('some error happend in storbinary file :[%s]. Err:%s' % (local_file, traceback.format_exc()))
            result = False
        logging.debug('上传 %s 【%s】, 远程文件大小 = %d, 本地文件大小 = %d.' \
                      % ('success' if (result == True) else 'failed', remote_file, remote_file_size, local_file_size))
        print('--- 上传 %s 【%s】, 远程文件大小 = %d, 本地文件大小 = %d.' \
              % ('success' if (result == True) else 'failed', remote_file, remote_file_size, local_file_size))
    else:
        logging.debug(
            '上传失败，ftp已存在文件[{}]，remote_file_size = {}, local_file_size = {}.'.format(remote_file, remote_file_size,
                                                                                    local_file_size))
        print('--- 上传失败，ftp已存在文件[{}]，remote_file_size ={}, local_file_size = {}.'.format(remote_file, remote_file_size,
                                                                                     local_file_size))


# 上传整个目录下的文件
def upload_file_tree(local_path=None, remote_path=None, ftp=None, IsRecursively=True):
    # print("remote_path:", remote_path)
    # print("local_path:", local_path)

    # 创建服务器目录 如果服务器目录不存在 就从当前目录创建目标外层目录
    # 打开该远程目录
    try:
        ftp.cwd(remote_path)  # 切换工作路径
    except Exception as e:
        # print('ftp切换路径失败：', e)
        base_dir = ''
        part_path = remote_path.split('/')
        # print('part_path: ', part_path)
        for subpath in part_path:
            # print('subpath: ', subpath)
            # 针对类似  '/home/billing/scripts/zhf/send' 和 'home/billing/scripts/zhf/send' 两种格式的目录
            # 如果第一个分解后的元素是''这种空字符，说明根目录是从/开始，如果最后一个是''这种空字符，说明目录是以/结束
            # 例如 /home/billing/scripts/zhf/send/ 分解后得到 ['', 'home', 'billing', 'scripts', 'zhf', 'send', ''] 首位和尾都不是有效名称
            if '' == subpath:
                continue
            base_dir = base_dir + r'/' + subpath  # base_dir + subpath + '/'  # 拼接子目录
            try:
                ftp.cwd(base_dir)  # 切换到子目录, 不存在则异常
            except Exception as e:
                print('--- 远端文件夹不存在, 正在创建[%s]' % (base_dir))
                logging.debug('远端文件夹不存在, 正在创建[%s]' % (base_dir))
                ftp.mkd(base_dir)  # 不存在创建当前子目录 直到创建所有
                continue
    # 本地目录切换
    try:
        # os.chdir(local_path)
        # 远端目录通过ftp对象已经切换到指定目录或创建的指定目录

        file_list = os.listdir(local_path)
        # print(file_list)
        for file_name in file_list:
            if os.path.isdir(os.path.join(local_path, file_name)):
                print('--- [%s] 是目录...' % (file_name))
                if IsRecursively:  # 递归目录上传
                    # 创建相关的子目录 创建不成功则目录已存在
                    try:
                        cwd = ftp.pwd()
                        ftp.cwd(file_name)  # 如果cwd成功 则表示该目录存在 退出到上一级
                        ftp.cwd(cwd)
                    except Exception as e:
                        print('--- 检查远端文件夹[%s]是否存在, 现在正在创建!' % (file_name))
                        ftp.mkd(file_name)

                    print('--- 尝试上传文件夹 [%s] --> [%s] ...' % (file_name, remote_path))
                    logging.debug('尝试上传文件夹 [%s] --> [%s] ...' % (file_name, remote_path))
                    p_local_path = os.path.join(local_path, file_name)
                    p_remote_path = os.path.join(ftp.pwd(), file_name)
                    upload_file_tree(p_local_path, p_remote_path, ftp, IsRecursively)
                    # 对于递归 ftp 每次传输完成后需要切换目录到上一级
                    ftp.cwd("..")
                else:
                    logging.debug('非递归上传文件夹, [%s] 是目录, continue ...' % (file_name))
                    continue
            else:
                # 是文件 直接上传
                local_file = local_path + r'/' + file_name
                remote_file = remote_path + r'/' + file_name
                if upload_file(local_file, remote_file, ftp):
                    pass
                    # logging.debug('upload %s success, delete it ...' %(local_file))
                    # os.unlink(local_file)
    except:
        logging.debug('上传文件[%s]出错:\n Err:%s' % (file_name, traceback.format_exc()))
    return


# 下载文件
def download_file(local_file=None, remote_file=None, ftp=None):  # 下载当个文件
    # 本地是否有此文件
    if os.path.exists(local_file):
        logging.debug('文件或者文件夹 [%s] 已存在.' % (local_file))

    # 在下载前判断两端的文件大小是否相同，如果本地没有文件，则result为False
    # print('local_file:', local_file)
    # print('remote_file:', remote_file)
    result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
    # result为false，说明本地不存在该文件，或者本地文件的大小和ftp不一致，也需要下载
    if not result:
        # print('本地文件 [%s] 不存在, 正在下载...' % (local_file))
        logging.debug('本地文件 [%s] 不存在, 正在下载...' % (local_file))
        global FTP_PERFECT_BUFF_SIZE
        bufsize = FTP_PERFECT_BUFF_SIZE
        try:
            fp = open(local_file, 'wb')  # 以写模式在本地打开文件
            if ftp.retrbinary('RETR ' + remote_file, fp.write, bufsize):  # 接收服务器上文件并写入本地文件
                if os.path.exists(local_file):
                    logging.debug('下载成功，{}文件已存在'.format(local_file))
                    print('--- 下载成功，{}文件已存在'.format(local_file))
                # 下载结束，查看本地和远程文件的大小是否一致
                # result, remote_file_size, local_file_size = is_same_size(ftp, local_file, remote_file)
                # print('result:{} , remote_file_size:{} , local_file_size:{} '.format(result, remote_file_size,
                #                                                                      local_file_size))
        except Exception as err:
            print('--- 下载文件[%s]失败: \nErr:%s' % (local_file, traceback.format_exc()))
            logging.debug('下载文件[%s]失败: \nErr:%s' % (local_file, traceback.format_exc()))
            result = False
        # logging.debug('Download 【%s】 %s , remote_file_size = %d, local_file_size = %d.' \
        #               % (remote_file, 'success' if (result == True) else 'failed', remote_file_size, local_file_size))
        # print('Download 【%s】 %s , remote_file_size = %d, local_file_size = %d.' \
        #       % (remote_file, 'success' if (result == True) else 'failed', remote_file_size, local_file_size))
    else:
        logging.debug(
            '下载失败，ftp已存在文件[{}]，remote_file_size = {}, local_file_size = {}.'.format(remote_file, remote_file_size,
                                                                                    local_file_size))
        print('--- 下载失败，ftp已存在文件[{}]，remote_file_size = {}, local_file_size = {}.'.format(remote_file, remote_file_size,
                                                                                      local_file_size))


# 下载整个目录下的文件
def download_file_tree(local_path=None, remote_path=None, ftp=None, IsRecursively=True):
    # print("remote_path:", remote_path)
    # print("local_path:", local_path)
    try:
        # 判断本地路径是否存在
        if not os.path.exists(local_path):
            # 不存在则创建文件夹
            print('--- 检查本地路径[ %s ]是否存在, 正在创建路径' % (local_path))
            os.makedirs(local_path)
        remote_dirname = remote_path.split('/')[-1]
        print('--- 远端文件夹名称为：', remote_dirname)
        local_path = local_path + '\\' + remote_dirname
        os.makedirs(local_path)
        print('--- 创建本地路径：', local_path)
        # 打开该远程目录
        try:
            ftp.cwd(remote_path)  # 切换工作路径
            # 读取该路径下的所有文件
            remote_files = ftp.nlst(remote_path)
            # print("remote_files: ", remote_files)
            for remote_file in remote_files:
                # 判断远程文件是否是文件，还是目录
                s = str(remote_file).find('.')
                fs = ftp.nlst(remote_file)
                if s < 0:
                    # 是目录，则进入目录循环下载
                    print("--- {}是文件夹，需要进入文件夹".format(remote_file))
                    ftp.cwd(remote_file)
                    for f in fs:
                        print('--- 包含文件：', f)
                        dir_name = str(f).split('/')[-2]
                        file_name = str(f).split('/')[-1]
                        d_local_file = local_path + '\\' + file_name  # 下载到本地后，没有新建对应的文件夹
                        d_remote_file = remote_path + r'/' + dir_name + r'/' + file_name
                        download_file(local_file=d_local_file, remote_file=d_remote_file, ftp=ftp)
                else:
                    # 是文件，则直接下载
                    file_name = str(remote_file).split('/')[-1]
                    d_local_file = local_path + '\\' + file_name
                    d_remote_file = remote_file
                    download_file(local_file=d_local_file, remote_file=d_remote_file, ftp=ftp)
        except Exception as e:
            print('--- Except INFO:', e)
    except Exception as err:
        print('--- Except INFO:', err)


if __name__ == '__main__':
    """  定义LOG名 """
    current_time = time.time()
    str_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(current_time))
    log_file_name = './ftp_logs/ftpput_' + str_time + '.txt'

    LOG_FORMAT = "%(message)s"  # "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "#配置输出日志格式
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '  # 配置输出时间的格式，注意月份和天数不要搞乱了
    LOG_PATH = os.path.join(os.getcwd(), log_file_name)
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filemode='w',  # 覆盖之前的记录 'a'是追加
                        filename=LOG_PATH  # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                        )

    # ftp_host = "192.168.30.54"
    # ftp_port = 8887
    ftp_host = "10.10.88.193"
    ftp_port = 21
    ftp_username = "test"
    ftp_password = "1q2w3e"
    ftp = ftpconnect(ftp_host, ftp_username, ftp_password, ftp_port)

    if ftp:
        '''  上传本地指定文件 '''
        local_file = r'E:\ftp_test\wq_test3.txt'
        remote_file = '/home/ftp/自动化测试_日志记录/ftp_upload/wq_test3.txt'
        # upload_file(local_file=local_file, remote_file=remote_file, ftp=ftp)

        ''' 上传整个路径下的文件 '''
        local_path = r'E:\ftp_test'
        remote_path = '/home/ftp/自动化测试_日志记录/ftp_upload/sssss'
        # 递归传输本地所有文件包括目录 递归开关 IsRecursively
        # upload_file_tree(local_path=local_path, remote_path=remote_path, ftp=ftp)

        '''  下载指定文件 '''
        download_remote_file = '/home/ftp/自动化测试_日志记录/ftp_upload/wq_test.txt'
        download_local_file = r'E:\ftp_test\wq_test.txt'
        # download_file(local_file=download_local_file, remote_file=download_remote_file, ftp=ftp)

        '''  下载指定文件夹 '''
        download_remote_path = '/home/ftp/自动化测试_日志记录/平台自动上传_log/20210421_16-56-59'
        download_local_path = r'E:\ftp_test'
        download_file_tree(local_path=download_local_path, remote_path=download_remote_path, ftp=ftp)

        # 关闭ftp
        ftp.quit()
        print('--------- ftp断开连接：host[{}]-port[{}]-username[{}]-password[{}]'.format(ftp_host, ftp_port, ftp_username,
                                                                                     ftp_password))
    else:
        print('--------- ftp主机{} 连接失败'.format(ftp_host))
        logging.debug('--------- ftp主机{} 连接失败'.format(ftp_host))
