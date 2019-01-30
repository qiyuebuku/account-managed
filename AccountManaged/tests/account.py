import pymysql
def get_account():
    host = 'localhost'#服务器地址
    user = 'root'#登录用户名
    password = '123456'#登录密码
    dbmame = 'account'#指定数据库
    db_conn = pymysql.connect(host,user,password,dbmame)
    
    cursor=db_conn.cursor()#获取游标
    sql = 'select * from account'    
    try:
        cursor.execute(sql)#执行sql

        result = cursor.fetchall()#取所有数据
        print('-'*43)
        print('|%s|%s｜'%('index'.center(20),'account'.center(20)))
        print('-'*43)
        for r in result:#遍历，打印
            account = r[0]
            ind = str(r[1])
            print('|%s|%s｜'%(ind.center(20),account.center(20)))
        print('-'*43)
    except Exception as e:
        print('查询异常')
        print(e)


    acct_ind = input('请输入要接收邮件的索引号：')
    s=''.join(acct_ind)
    sql = '''select account from account
            where ind in (%s)
            '''%s
    try:
        cursor.execute(sql)#执行sql
        result = cursor.fetchall()#取所有数据
        account_list=[]
        for r in result:
            account_list.append(r[0])
        print(account_list)

    except Exception as e:
        print('查询异常')
        print(e)
    return account_list

# get_account()