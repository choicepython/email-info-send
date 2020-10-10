import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import configparser
import os

path = os.path.join(os.path.dirname(os.getcwd()), 'config')


def get_email(env):
    """
    用来获取邮件服务的相关信息
    :param env:
    :return:
    """
    config = configparser.ConfigParser()
    if env == 'DEVELOPMENT':
        config.read(os.path.join(path, 'DEVELOPMENT.cfg'))
        sender = config.get('email', 'sender')
        email = config.get('email', 'user')
        pwd = config.get('email', 'pwd')    # 授权码不是邮箱密码
        server = config.get('email', 'server')
        return sender, pwd, server, email
    elif env == 'TEST':
        config.read(os.path.join(path, 'DEVELOPMENT.cfg'))
        sender = config.get('email', 'user')
        email = config.get('email', 'sender')
        pwd = config.get('email', 'pwd')
        server = config.get('email', 'server')
        return sender, pwd, server, email
    return config


class SendEmail:
    sender, pwd, server, email = get_email('TEST')
    print(email, pwd, server)

    def __init__(self):
        self.Obj = smtplib.SMTP_SSL(host=self.server, port=465)
        self.Obj.login(self.email, self.pwd)

    def text_email(self, text: str, title="SPM TEXT", receiver=''):

        """
        :param text:    邮件文本
        :param title:   邮件标题
        :param receiver:  邮件接收人
        :return:
        """
        try:
            msg = MIMEText(text)
            msg['From'] = self.email  # 发送人信息
            msg['Subject'] = title    # 邮件标题
            msg['To'] = receiver    # 收件人信息
            self.Obj.sendmail(self.email, receiver, msg.as_string())
            print("Successfully sent email")

        except Exception as e:
            print("Error: unable to send email", e)

    def html_email(self, text: str, receiver: str, title="HTML email"):
        """
        <b>This is HTML message.</b>
        <h1>This is headline.</h1>
        msg['Content-type'] = 'text/html'
        :param text:
        :param title:
        :param receiver:
        :return:
        """
        try:
            msg = MIMEText(text)
            msg["Content-type"] = 'text/html'
            msg['From'] = self.email  # 发送人信息
            msg['Subject'] = title  # 邮件标题
            msg['To'] = receiver  # 收件人信息
            self.Obj.sendmail(self.email, receiver, msg.as_string())
            print("Successfully sent email")

        except Exception as e:
            print("Error: unable to send email", e)

    def accessory_email(self, text: str, receiver: str or list, file: dict, title='Maxsu的邮件'):
        """
        msg = MIMEMultipart()
        text = "你好，<p>这是带有附件的邮件发送测试：</p><p><a href='http://www.yiibai.com'>易百教程</a></p>"
        msg.attach(MIMEText(text, 'html'))
        att1 = MIMEText(open('../data/attach.txt', 'rb').read(), 'base64', 'utf-8')
        # 命名附件名
        att1["Content-Disposition"] = 'attachment;filename="hhh.txt"'
        msg.attach(att1)

        :param text:  MIMEMultipart
        :param title: 邮件标题
        :param receiver:  接受人
        :param file:  附件名：附件地址
        :return: None
        """
        try:
            msg = MIMEMultipart()
            email_data = MIMEText(text)
            email_data["Content-type"] = 'text/html'
            msg.attach(email_data)
            if len(file) > 1:
                for key, value in file.items():
                    att1 = MIMEText(open(value, 'rb').read(), 'base64', 'utf-8')
                    att1["Content-Disposition"] = 'attachment;filename="{}.txt"'.format(key)
                    msg.attach(att1)
            elif len(file) == 1:
                att1 = MIMEText(open(file.values().__iter__().__next__(), 'rb').read(), 'base64', 'utf-8')
                att1["Content-Disposition"] = 'attachment;filename="{}.txt"'.format(file.keys().__iter__().__next__())
                msg.attach(att1)
            # text["Content-type"] = 'multipart/mixed'
            msg["Content-type"] = 'application/octet-stream'
            msg['From'] = self.email  # 发送人信息
            msg['Subject'] = title  # 邮件标题
            self.Obj.sendmail(self.email, receiver, msg.as_string())
            print("Successfully sent email")

        except Exception as e:
            print("Error: unable to send email", e)
        pass

    def mass_email(self, text: str, receivers: list, title="mass email"):
        """

        :param text:
        :param receivers: ['yiibai.com@gmail.com','****su@gmail.com']
        :param title:
        :return:
        """
        try:
            msg = MIMEText(text)
            msg["Content-type"] = 'text/html'
            msg['From'] = self.email  # 发送人信息
            msg['Subject'] = title  # 邮件标题
            # text['To'] = receivers  # 收件人信息
            self.Obj.sendmail(self.email, receivers, msg.as_string())
            print("Successfully sent email")

        except Exception as e:
            print("Error: unable to send email", e)
        pass

    def img_email(self, text: str, filepath: str, receiver: str or list, title="IMG email"):
        """        :param text:  <p>你好，Python 邮件发送测试...</p>\n<p>这是使用python登录qq邮箱发送HTML格式和图片的测试邮件：</p>
                     <p>图片演示：</p>
                     <p><img src='cid:send_image'></p>
        :param filepath: 图片路径
        :param receiver:
        :param title:
        :return:
        """
        try:
            if "<img src='cid:send_image'" not in text:
                text += "<img src='cid:send_image'>"
            msg = MIMEMultipart('related')
            msgText = MIMEText(text, 'html', 'utf-8')
            msg.attach(msgText)
            # 指定图片为当前目录
            fp = open(filepath, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            # 定义图片 ID，在 HTML 文本中引用
            msgImage.add_header('Content-ID', '<send_image>')
            msg.attach(msgImage)

            msg['From'] = self.email  # 发送人信息
            msg['Subject'] = title  # 邮件标题
            # text['To'] = receivers  # 收件人信息
            msg["Content-type"] = 'text/html'
            self.Obj.sendmail(self.email, receiver, msg.as_string())
            print("Successfully sent email")

        except Exception as e:
            print("Error: unable to send email", e)
        pass


if __name__ == '__main__':
    se = SendEmail()
    accept = "***@qq.com"
    data = """
    <b>This is HTML message.</b>
    <h1>This is headline.</h1>
    """
    file_dict = {'hh': '../data/attach.txt'}
    se.img_email(data, receiver=accept, filepath='../img/my.png')
    print('over')
