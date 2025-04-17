import yaml

yaml_path = './config.yaml'

def get_mysql_config():
    with open(yaml_path, 'r', encoding = 'utf-8') as file:
        data = yaml.safe_load_all(file)
        data_list = list(data)
    mysql_list = data_list[0]['mysql']
    return mysql_list

def get_emqx_config():
    with open(yaml_path, 'r', encoding = 'utf-8') as file:
        data = yaml.safe_load_all(file)
        data_list = list(data)
    emqx_list = data_list[0]['emqx']
    return emqx_list

if __name__=='__main__':
    mysql_list = get_mysql_config()
    host = mysql_list['host']
    port = mysql_list['port']
    username = mysql_list['username']
    password = mysql_list['password']
    database = mysql_list['database']
    print(host)
    print(port)
    print(username)
    print(password)
    print(database)

    emqx_list = get_emqx_config()
    username = emqx_list['username']
    password = emqx_list['password']
    topic = emqx_list['topic']
    broker = emqx_list['broker']
    port = emqx_list['port']
    print(username)
    print(password)
    print(topic)
    print(broker)
    print(port)
