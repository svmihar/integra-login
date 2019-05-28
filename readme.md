# Integra Login 

Collects NRP from forlap dikti, then tries to login with 'surabaya' as password.

## Colletected NRP 
panjang awal:  10063
panjang akhir:  9434

## Getting Started
- make sure you have an internal ITS connection
- install depedencies: 
  - install selenium (properly)
  - install beautifulsoup
  - install requests
## How does it work 
- takes nrp from nrp.txt
- tries login to `integra.its.ac.id`
- delete cookies
- if 
  - success: store to berhasil.txt
  - fail: repeat from 2 

## why? 
 stop using default password. or if you're an LPTSI member, please use hash generated password, don't use a plain string.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
