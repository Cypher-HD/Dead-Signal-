# engine/reconcore.py
import socket
import subprocess
import dns.resolver
import whois
from engine.logforge import log_event

def perform_recon(target):
    print(f"\n[+] RECONCORE ACTIVATED :: Scanning {target}\n")
    log_event(f"[RECON START] :: {target}")

    try:
        ip = socket.gethostbyname(target)
        print(f"[+] IP: {ip}")
        log_event(f"Resolved IP: {ip}")
    except Exception as e:
        print(f"[-] IP Resolution Failed: {e}")
        log_event(f"IP Resolution Failed: {e}")
        ip = None

    # WHOIS
    try:
        whois_data = whois.whois(target)
        print(f"[+] WHOIS Registered To: {whois_data.name if whois_data.name else 'UNKNOWN'}")
        print(f"[+] WHOIS Created: {whois_data.creation_date}")
        print(f"[+] WHOIS Registrar: {whois_data.registrar}")
        log_event(f"WHOIS Registered: {whois_data.name}, Registrar: {whois_data.registrar}")
    except Exception as e:
        print("[-] WHOIS Lookup Failed")
        log_event("WHOIS Failure")

    # DNS Records
    for rtype in ["A", "MX", "NS", "CNAME", "TXT"]:
        try:
            answers = dns.resolver.resolve(target, rtype)
            for rdata in answers:
                print(f"[+] {rtype} Record: {rdata.to_text()}")
                log_event(f"{rtype} Record: {rdata.to_text()}")
        except:
            print(f"[-] No {rtype} Record Found")

    # Subdomain sweep (passive dictionary)
    print("\n[+] Attempting Subdomain Discovery")
    subdomains = ['www', 'mail', 'ftp', 'dev', 'test', 'admin', 'webmail', 'vpn', 'blog']
    for sub in subdomains:
        try:
            full = f"{sub}.{target}"
            socket.gethostbyname(full)
            print(f"[+] Subdomain Found: {full}")
            log_event(f"Subdomain Found: {full}")
        except:
            pass
