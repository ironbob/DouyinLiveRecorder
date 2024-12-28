from typing import Any
import os
import sys
import json
from douyinliverecorder import spider, stream
import configparser

script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
config_file = f'{script_path}/config/config.ini'
text_encoding = 'utf-8-sig'
config = configparser.RawConfigParser()

def read_config_value(config_parser: configparser.RawConfigParser, section: str, option: str, default_value: Any) \
        -> Any:
    try:

        config_parser.read(config_file, encoding=text_encoding)
        if '录制设置' not in config_parser.sections():
            config_parser.add_section('录制设置')
        if '推送配置' not in config_parser.sections():
            config_parser.add_section('推送配置')
        if 'Cookie' not in config_parser.sections():
            config_parser.add_section('Cookie')
        if 'Authorization' not in config_parser.sections():
            config_parser.add_section('Authorization')
        if '账号密码' not in config_parser.sections():
            config_parser.add_section('账号密码')
        return config_parser.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        config_parser.set(section, option, str(default_value))
        with open(config_file, 'w', encoding=text_encoding) as f:
            config_parser.write(f)
        return default_value
dy_cookie = read_config_value(config, 'Cookie', '抖音cookie', '')

def get_liveroom_json(url: str):
    json_data = spider.get_douyin_stream_data(
        url=url,
        proxy_addr=None,
        cookies=dy_cookie)
    
    port_info = stream.get_douyin_stream_url(json_data, "原画")
    return port_info

if __name__ == '__main__':
    json = get_liveroom_json("https://live.douyin.com/670238762772")
    anchor_name = json.get("anchor_name", '')
    record_url = json['record_url']
    # print("json--=--------------->\n\n\n")
    # print(json)
    print("anchor_name--=--------------->\n\n\n")
    print(anchor_name)
    print("record_url--=--------------->\n\n\n")
    print(record_url)   