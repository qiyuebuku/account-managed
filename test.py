# def getfn():                                                                        
#     def print_hello():
#         print("hello")
#     return print_hello()
# fn = getfn()
# print(fn)
# print_hello()



# def print_square(row):
#     for i in range(row):
#         for j in range(i,i+6):
#             if j>9:
#                 print(str(j)[1],end='')
#             else:
#                 print(j,end='')
#         print()



# print_square(10)




# def dan_ci_reverse(s):
#     l1=s.split()
#     l1=[x[::-1] for x in l1]
#     return ' '.join(l1)

# print(dan_ci_reverse("welcome to beijing"))

# def fen_ge():
#     L=[1,2,3,4,5,6]
#     L=''.join([str(i)+"|" for i in L])
#     return L
# print(fen_ge())


# count=0
# for i in (1,2,3,4):
#     for j in (1,2,3,4):
#         for z in (1,2,3,4):
#             if i!=j and j!= z and z!=i:
#                 count+=1
#                 print('%s%s%s'%(i,j,z),end='|')
#     print()
# print('共有%s种组合'%count)

# a=1
# b=1
# print(a,b,sep='\n')
# for i in range(10):
#     a=a+b
#     print(a)
#     b=b+a
#     print(b)


# def readfile(f):
#     data=f.readlines(10)
#     yield data

# with open(r'D:\bj\account managed\AccountManaged\tests\1.txt') as f:
#     data = readfile(f)
#     for i in data:
#         print(i)



import random
l=[1,2,3,4]

l2=[]
while True:
    print(random.sample(l,4))
    num=([1,2,3,4])
    if num not in l2:
        l2.append(num) 
print(l2)



