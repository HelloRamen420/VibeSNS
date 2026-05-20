print("所持金はなんぼでっか？ >> ",end="")
x=input()
print("何個買うんでっか？ >> ",end="")
n=input()
res=0
for i in range(int(n)):
    print("なに買うんでっか？ >> ",end="")
    res+=int(input())

if int(x)>res:
    print("お買い上げー")
else:
    print("足りないぞー")
