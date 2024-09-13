from NSE import *



print("start")

index_list = ["NIFTY"]

# IOC = IndexOptionChain
# SOC = StockOptionChain
if __main__ 
    for index in index_list:
        obj = IOC(index)
        data = obj.fetch_data()
        print(data["records"].keys())
        print("")
        print(data["records"]["data"][1])
        # print(data["records"]["timestamp"].keys())


