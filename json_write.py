import json
def modify(date,user_id,value,data_name):
    try:
        f = open(data_name,'r',newline='')
    except:
        return 'File Open Error'
    data = json.load(f)
    if(value == True):
        try:
            arr = data[date]
            data[date][user_id] = value
        except:
            data[date] = {}
            data[date][user_id] = value
        f.close()
    else:
        try:
            arr = data[date]
            data[date][user_id] = value
        except:
            return 'Not Found'
    
    try:
        f = open(data_name,'w',newline='')
        f.write(json.dumps(data,indent=4))
    except:
        return 'Write Error'
    return 'Success'
