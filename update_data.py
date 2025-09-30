#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

# 从环境变量获取配置
GIST_ID = os.environ.get('GIST_ID')
GH_TOKEN = os.environ.get('GH_TOKEN')

def update_website_data():
    headers = {
        'Authorization': f'token {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # 1. 从Gist获取数据
        gist_url = f'https://api.github.com/gists/{GIST_ID}'
        response = requests.get(gist_url, headers=headers)
        gist_data = response.json()
        
        # 2. 处理数据
        filename = list(gist_data['files'].keys())[0]
        content = gist_data['files'][filename]['content']
        messages = json.loads(content) if content.strip() else []
        
        # 3. 生成前端数据
        frontend_data = {
            'lastUpdated': datetime.now().isoformat(),
            'messages': messages[:50]  # 只保留最近50条
        }
        
        # 4. 保存到data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(frontend_data, f, ensure_ascii=False, indent=2)
        
        print(f'成功同步 {len(messages)} 条数据')
        return True
        
    except Exception as e:
        print(f'同步失败: {e}')
        # 创建空数据文件
        empty_data = {
            'lastUpdated': datetime.now().isoformat(),
            'messages': []
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, ensure_ascii=False, indent=2)
        return False

if __name__ == '__main__':
    update_website_data()
