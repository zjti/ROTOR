import js 
import json

def fufu2(data):
    print('a')
    print(data)
    print(str(type(data)))
    return 23
    

def fufu(data):
    k=data
    # k = json.loads(js.localStorage.getItem('TEST123')  )
    print(k)
    if k['dope'] % 3 == 0:
        k['dope']-=1
    k['x']=12
    # js.localStorage.setItem('TEST123',json.dumps(k) )
    print(k)
    # js.localStorage.setItem('TEST',json.dumps(k) )
    
    return k
    