with open('nrp.txt','r') as f: 
    data = f.readlines()

data.sort()
print(len(data))
for nrp in data: 
    nrp = nrp.strip()
    if len(nrp)>5 and nrp.isdigit(): 
        with open('nrp_good.txt', 'a') as file: 
            file.writelines(nrp+'\n')
