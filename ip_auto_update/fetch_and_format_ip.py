import requests
import json
import re
import os

API_CONFIG_FILE = 'api_config.json'
OUTPUT_FILE = 'ip.txt'

def is_valid_ip_line(line):
    if re.match(r'^(\d+\.\d+\.\d+\.\d+)(:\d+)?(#|\s|\||$)', line):
        return True
    if re.match(r'^\[?[0-9a-fA-F:]+\]?(:\d+)?(#|\s|\||$)', line):
        return True
    if re.match(r'^(www|ct|cmcc)\.cf\.090227\.xyz:443#', line):
        return True
    if re.match(r'^[\w\.-]+:443#', line):
        return True
    return False

def format_ip_line(line):
    ipv6_match = re.match(r'\[?([0-9a-fA-F:]+)\]?(:\d+)?(.*)', line)
    if ipv6_match and ':' in ipv6_match.group(1):
        ip = ipv6_match.group(1)
        port = ipv6_match.group(2) or ':443'
        rest = ipv6_match.group(3)
        return f'[{ip}]{port}{rest}'
    ipv4_match = re.match(r'(\d+\.\d+\.\d+\.\d+)(:\d+)?(.*)', line)
    if ipv4_match:
        ip = ipv4_match.group(1)
        port = ipv4_match.group(2) or ':443'
        rest = ipv4_match.group(3)
        return f'{ip}{port}{rest}'
    return line

def ensure_remark(line, remark):
    if '#' in line:
        return line
    # 自动补备注为#IP
    # 提取IPv4或IPv6地址
    ipv4 = re.match(r'(\d+\.\d+\.\d+\.\d+)', line)
    ipv6 = re.match(r'\[?([0-9a-fA-F:]+)\]?', line)
    if ipv4:
        tag = ipv4.group(1)
    elif ipv6:
        tag = ipv6.group(1)
    else:
        tag = '无备注'
    return f"{line}#{tag}"

def parse_api_content(url, remark, text):
    text = re.sub(r'<script[\s\S]*?</script>', '', text, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if 'ip.164746.xyz' in url and '#' in text:
        valid_lines = [format_ip_line(l) for l in lines if is_valid_ip_line(l)]
        valid_lines = [ensure_remark(l, remark) for l in valid_lines]
        return valid_lines
    if 'cf.090227.xyz' in url:
        result = [
            'www.cf.090227.xyz:443#三网自适应分流-www.cf.090227.xyz',
            'ct.090227.xyz:443#电信分流-ct.090227.xyz',
            'cmcc.090227.xyz:443#移动分流-cmcc.090227.xyz'
        ]
        for line in lines:
            m = re.match(r'(电信|移动|联通|三网)\s+([\d\.]+)\s+.*?([\d\.]+MB/s)', line)
            if m:
                net, ip, speed = m.groups()
                result.append(f'{ip}:443#{net}分流-{ip}')
        result = [ensure_remark(l, remark) for l in result]
        return result
    if any(x in url for x in ['/ct', '/CloudFlareYes']):
        valid_lines = [format_ip_line(l) for l in lines if is_valid_ip_line(l)]
        valid_lines = [ensure_remark(l, remark) for l in valid_lines]
        return valid_lines
    if 'cmcc-ipv6' in url:
        valid_lines = [format_ip_line(l) for l in lines if is_valid_ip_line(l)]
        valid_lines = [ensure_remark(l, remark) for l in valid_lines]
        return valid_lines
    if 'ip.164746.xyz' in url and 'IP地址' in text:
        result = []
        for line in lines:
            m = re.match(r'(★?\s*([\d\.]+))\s+\d+\s+\d+\s+[\d\.]+%\s+[\d\.]+\s+([\d\.]+MB/s)', line)
            if m:
                ip = m.group(2)
                speed = m.group(3)
                result.append(f'{ip}:443#{ip} | ⬇️ {speed}')
        result = [ensure_remark(l, remark) for l in result]
        return result
    # 末尾统一处理所有输出行，保证带#备注
    lines_out = [format_ip_line(l) for l in lines if is_valid_ip_line(l)]
    lines_out = [ensure_remark(l, remark) for l in lines_out]
    return lines_out

def main():
    if not os.path.exists(API_CONFIG_FILE):
        print('api_config.json不存在')
        return
    with open(API_CONFIG_FILE, 'r', encoding='utf-8') as f:
        api_list = json.load(f)
    result_lines = []
    for api in api_list:
        try:
            resp = requests.get(api['url'], timeout=15)
            resp.encoding = resp.apparent_encoding
            lines = parse_api_content(api['url'], api['remark'], resp.text)
            result_lines.extend(lines)
        except Exception as e:
            print(f"【{api['remark']}】获取失败: {e}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result_lines))
    print(f'已写入 {OUTPUT_FILE}')

if __name__ == '__main__':
    main() 
