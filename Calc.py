import ipaddress

# Funksioni per te llogaritur Network ID dhe Broadcast ID
def network_and_broadcast(ip, netmask):
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return str(network.network_address), str(network.broadcast_address)

# Funksioni per te llogaritur IP-te e pare dhe te fundit, si dhe numrin e hosteve
def first_last_ip_and_hosts(ip, netmask):
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    first_ip = str(network.network_address + 1)
    last_ip = str(network.broadcast_address - 1)
    total_hosts = network.num_addresses - 2  # Pershtatja per adresat e rezervuara (network dhe broadcast)
    return first_ip, last_ip, total_hosts

# Funksioni per te gjeneruar subnetet dhe informacionet per secilen
def subnet_info(ip, netmask, subnets):
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    
    # Sigurohemi qe new_prefix eshte me i madh ose i barabarte me prefix-in ekzistues
    current_prefix = network.prefixlen
    if subnets <= current_prefix:
        raise ValueError(f"Numri i subneteve duhet te krijohet me prefix me te madh se {current_prefix}")

    # Gjenerojme subnetet
    subnets_list = list(network.subnets(new_prefix=subnets))
    subnet_info_list = []
    
    for subnet in subnets_list:
        first_ip = str(subnet.network_address + 1)
        last_ip = str(subnet.broadcast_address - 1)
        total_hosts = subnet.num_addresses - 2  # Pershtatja per adresat e rezervuara (network dhe broadcast)
        subnet_info_list.append({
            "Subnet_ID": str(subnet.network_address),
            "Broadcast_ID": str(subnet.broadcast_address),
            "IP_pare": first_ip,
            "IP_Fundit": last_ip,
            "Nr_Hostesh": total_hosts
        })
    
    return subnet_info_list

# Menyra e perdorimit te kalkulatorit

def main():
    print("Kalkulatori per Adresimin TCP/IP V4\n")

    # Pjesa a)
    ip = input("Jepni adresen IP (shkruani ne formatin X.X.X.X): ")
    netmask = input("Jepni Subnet Mask (shkruani ne formatin X.X.X.X): ")
    
    network_id, broadcast_id = network_and_broadcast(ip, netmask)
    print(f"Network ID: {network_id}")
    print(f"Broadcast ID: {broadcast_id}\n")

    # Pjesa b)
    first_ip, last_ip, total_hosts = first_last_ip_and_hosts(ip, netmask)
    print(f"IP e pare: {first_ip}")
    print(f"IP i fundit: {last_ip}")
    print(f"Numri i Hosteve te vlefshem: {total_hosts}\n")
    
    # Pjesa c)
    subnets = int(input("Jepni numrin e subneteve qe deshironi te krijoni: "))
    try:
        subnet_info_list = subnet_info(ip, netmask, subnets)
        print("\nInformacionet per subnetet e krijuara:")
        for subnet in subnet_info_list:
            print(f"Subnet_ID: {subnet['Subnet_ID']}")
            print(f"Broadcast_ID: {subnet['Broadcast_ID']}")
            print(f"IP_pare: {subnet['IP_pare']}")
            print(f"IP_Fundit: {subnet['IP_Fundit']}")
            print(f"Nr_Hostesh: {subnet['Nr_Hostesh']}\n")
    except ValueError as e:
        print(f"Gabim: {e}")

if __name__ == "__main__":
    main()
