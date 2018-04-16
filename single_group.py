#!/usr/bin/env python3
# coding: utf-8

"""
功能说明：
1. 用户无需发送关键词，添加好友后，自动发送邀请消息
2. 添加好友后，会自动发送回复语（下方可修改）
3. 用户进群后，自动发送相关的邀请信息。
"""
"""
定义区，下方数据修改为你自己对应的内容
"""
# 欢迎语，{} 会变成新入群用户的昵称
welcome_text = '''🎉 欢迎 @{} 加入社区纯技术交流群。
提问为了更好的描述，尤其长代码，长错误日志，
请上 Spring For All 社区（spring4all.com），
社区有技术专家问答。
😃 更多请关注Spring For All 社区公号  
https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU0MDEwMjgwNA==&scene=124&#wechat_redirect，
为了更好的学习环境，您可以将此链接转发到朋友圈，学习的路上不孤单！
谢谢~
'''

# 回复语，在发送群邀请后会回复这个
reply_text = """你好，欢迎加入我们 Spring4all 社区群
群规是：不允许发广告、宣传信息
"""

# 群名
group_name = 'Spring For All 社区 ⑥'

"""
代码区，下方的内容不要修改
"""
from wxpy import *
import re
import platform
console_qr=(False if platform.system() == 'Windows' else True)
bot = Bot('bot.pkl', console_qr=console_qr)

target_group = bot.groups().search(group_name)[0]

'''
邀请消息处理
'''
def get_new_member_name(msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')

    for rp in rp_new_member_name:
        match = rp.search(msg.text)
        if match:
            return match.group(1)
'''
邀请信息处理
'''
rp_new_member_name = (
    re.compile(r'^"(.+)"通过'),
    re.compile(r'邀请"(.+)"加入'),
)

'''
处理加好友请求信息。
如果验证信息文本是字典的键值之一，则尝试拉群。
'''
@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    target_group.add_members(user,use_invitation=True)
    user.send(reply_text)

@bot.register(target_group, NOTE)
def welcome(msg):
    name = get_new_member_name(msg)
    if name:
        return welcome_text.format(name)

bot.join()
