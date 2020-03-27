import json,sys
def get_date(time):
    with open('record.json','r',newline='') as f:
        data = json.load(f)
        cnt = 0
        try:
            for i in data[time]:
                if(data[time][i] == True):
                    cnt += 1
            print(cnt)
        except:
            print(0)

if __name__ == "__main__":
    time = sys.argv[1]
    get_date(time)