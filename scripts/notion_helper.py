#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = 'https://api.notion.com/v1'
API_VERSION = '2025-09-03'


def get_api_key():
    key = os.environ.get('NOTION_API_KEY')
    if key:
        return key.strip()
    path = os.path.expanduser('~/.config/notion/api_key')
    with open(path) as f:
        return f.read().strip()


def request(method, path, payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_BASE + path,
        data=data,
        headers={
            'Authorization': f'Bearer {get_api_key()}',
            'Notion-Version': API_VERSION,
            'Content-Type': 'application/json',
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')
        print(json.dumps({
            'ok': False,
            'status': e.code,
            'path': path,
            'body': body,
        }, indent=2))
        raise


def cmd_get_page(page_id):
    result = request('GET', f'/pages/{page_id}')
    print(json.dumps(result, indent=2))


def cmd_create_page(parent_page_id, title):
    payload = {
        'parent': {'page_id': parent_page_id},
        'properties': {
            'title': {
                'title': [
                    {'type': 'text', 'text': {'content': title}}
                ]
            }
        }
    }
    result = request('POST', '/pages', payload)
    print(json.dumps(result, indent=2))


def cmd_create_minimal_data_source(parent_page_id, title):
    payload = {
        'parent': {'page_id': parent_page_id},
        'title': [{'type': 'text', 'text': {'content': title}}],
        'is_inline': True,
        'properties': {
            'Name': {'title': {}},
            'Status': {'select': {'options': [{'name': 'Draft'}, {'name': 'Active'}]}}
        }
    }
    result = request('POST', '/data_sources', payload)
    print(json.dumps(result, indent=2))


def main():
    if len(sys.argv) < 2:
        print('Usage: notion_helper.py <command> [args...]', file=sys.stderr)
        sys.exit(2)

    cmd = sys.argv[1]
    if cmd == 'get-page' and len(sys.argv) == 3:
        cmd_get_page(sys.argv[2])
    elif cmd == 'create-page' and len(sys.argv) == 4:
        cmd_create_page(sys.argv[2], sys.argv[3])
    elif cmd == 'create-minimal-data-source' and len(sys.argv) == 4:
        cmd_create_minimal_data_source(sys.argv[2], sys.argv[3])
    else:
        print('Usage:', file=sys.stderr)
        print('  notion_helper.py get-page <page_id>', file=sys.stderr)
        print('  notion_helper.py create-page <parent_page_id> <title>', file=sys.stderr)
        print('  notion_helper.py create-minimal-data-source <parent_page_id> <title>', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
