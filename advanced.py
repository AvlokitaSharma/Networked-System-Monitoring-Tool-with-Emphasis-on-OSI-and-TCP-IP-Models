def process_packet(packet):
    current_time = pd.datetime.now()
    data['Timestamp'].append(current_time)
    data['Packet_Size'].append(len(packet))
    
    # Check for Ethernet layer
    if packet.haslayer(Ether):
        data['Ethernet'].append(1)
        data['Source_MAC'].append(packet[Ether].src)
        data['Destination_MAC'].append(packet[Ether].dst)
    else:
        data['Ethernet'].append(0)
        data['Source_MAC'].append('N/A')
        data['Destination_MAC'].append('N/A')
    
    # Check for IP layer and capture IPs
    if packet.haslayer(IP):
        data['IP'].append(1)
        data['Source_IP'].append(packet[IP].src)
        data['Destination_IP'].append(packet[IP].dst)
    else:
        data['IP'].append(0)
        data['Source_IP'].append('N/A')
        data['Destination_IP'].append('N/A')
    
    # Capture TCP and UDP details
    for layer, protocol in [('TCP', TCP), ('UDP', UDP)]:
        if packet.haslayer(protocol):
            data[layer].append(1)
        else:
            data[layer].append(0)

    # Add more protocols as necessary
