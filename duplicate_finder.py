with open('nrp_good.txt','r') as f: 
    koleksi_nrp=f.readlines()

print(len(koleksi_nrp))    
koleksi_nrp = list(set(koleksi_nrp))
print(len(koleksi_nrp))    
