
#检测用户邮箱账号的POP和SMT是否开启
def check_POP_SMT(server):
    flag=True
    try:
        if not server.smtp_able():
            flag=False
        if not server.pop_able():
            flag=False
    except Exception:
        flag=False
    finally:
        return flag

#读取配置文件
def read_config(config_path):
    with open(config_path,'r',encoding='utf8') as f:
        result=f.read()
    return result.split('\n')[:-1]

#写入配置文件
def write_config(config_path,info):
    with open(config_path,'a',encoding='utf8') as f:
        for i in info:
            for j in i:
                print(j,file=f,end='|')
            print(file=f)

#判断路径是否存在
def isfile(file_path):
    try:
        open(file_path,'r')
        return True
    except(FileNotFoundError,PermissionError,OSError) as e:
        print(e)
        return False

# 获取文件路径中的文件名称
def get_fielname(file_path):
    file_name=file_path.split("\\")[-1]
    if len(file_name)<=0:
        file_name=file_path.split("/")[-1]
        if len(file_name)<=0:
            file_name=file_path
    return file_name
        