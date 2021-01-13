import re 
data = "เเจ้งราคา btc = 100000"
res = [int(i) for i in data.split() if i.isdigit()] 
if "btc" in data:
    name = "btc"
print(name, type(res[0]))



condition = {'THB_BTC':{'buy': 1020000, 'sell': 1115000}, 
            'THB_ETH':{'buy': 30000, 'sell': 40000},
            'THB_BAND':{'buy': 200, 'sell': 300},}
print(condition['THB_BTC']['buy'])
condition['THB_BTC']['buy'] = 100000
print(condition['THB_BTC']['buy'])