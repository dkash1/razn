'''
creaty by  https://t.me/YesW0rld1
'''

import json
import sys

def process_netobject(obj):
    if obj.get('type') == 'group':
        
        members = obj.get('members', [])
        member_list = []
        for member in members:
            member_name = member.get('name', '')
            member_ip = member.get('ip', '')
            member_list.append(f"{member_name} ({member_ip})")
        group_name = obj.get('name', 'Group')
        return f"{group_name} [Group]: " + ', '.join(member_list)
    else:
        
        name = obj.get('name', '')
        ip = obj.get('ip', '')
        return f"{name} ({ip})"

def generate_html_table(rules):
    html = '''
    <html>
    <head>
        <title>Переносимые правила</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h2>Переносимые правила</h2>
        <table>
            <tr>
                <th>Name</th>               
                <th>Source</th>
                <th>Destination</th>
                <th>Service</th>
                <th>Action</th>
                <th>Logging</th>
                <th>Description</th>
            </tr>
    '''

    for rule in rules:
        name = rule.get('name', '')
        description = rule.get('description', '')
        action = rule.get('rule_action', '')
        logging = 'Включено' if rule.get('logging', False) else 'Отключено'
        
        
        src_list = []
        for src in rule.get('src', []):
            src_str = process_netobject(src)
            src_list.append(src_str)
        src_str = ', '.join(src_list) if src_list else 'Any'

        
        dst_list = []
        for dst in rule.get('dst', []):
            dst_str = process_netobject(dst)
            dst_list.append(dst_str)
        dst_str = ', '.join(dst_list) if dst_list else 'Any'

        
        service_list = []
        for service in rule.get('service', []):
            service_name = service.get('name', '')
            dst_ports = service.get('dst', '')
            service_list.append(f"{service_name} (Ports: {dst_ports})")
        service_str = ', '.join(service_list) if service_list else 'Any'

        html += f'''
            <tr>
                <td>{name}</td>                
                <td>{src_str}</td>
                <td>{dst_str}</td>
                <td>{service_str}</td>
                <td>{action.capitalize()}</td>
                <td>{logging}</td>
                <td>{description}</td>
            </tr>
        '''

    html += '''
        </table>
    </body>
    </html>
    '''
    return html

def main():
    if len(sys.argv) != 3:
        print("Запуск: python script.py input.json output.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    
    with open(input_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)

    
    html_content = generate_html_table(rules)

    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML-файл успешно создан: {output_file}")

if __name__ == '__main__':
    main()
