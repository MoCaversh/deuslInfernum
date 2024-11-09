import json
import os
import random
import string
import time
import sys
from colorama import Fore, Style, init

# Colorama'yı başlat (Windows için gerekli)
init(autoreset=True)

# Global değişkenler
last_connected_server = None
in_server = False  # Sunucu içinde olma durumunu tutan değişken

def load_servers():
    """Load existing servers from servers.json."""
    if os.path.exists('servers.json'):
        with open('servers.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_servers(servers):
    """Save servers to servers.json."""
    with open('servers.json', 'w') as file:
        json.dump(servers, file, indent=4)

def create_server(server_name):
    """Create a new server with styled input prompts."""
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📛  {Fore.MAGENTA}Server Name: {Fore.RESET}{server_name}")
    
    print(f"{Fore.MAGENTA}🔐 Password: ", end="")
    password = input()

    print(f"{Fore.MAGENTA}🔄 Again Password: ", end="")
    password_again = input()

    if password == password_again:
        servers = load_servers()
        servers.append({'ServerName': server_name, 'Password': password, 'Data': []})
        save_servers(servers)
        print(f"{Fore.YELLOW}\n✨ Server başarıyla oluşturuldu!")
    else:
        print(f"{Fore.RED}\n❌ Şifreler uyuşmuyor!")
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def create_data():
    """Create a new data entry for an existing server."""
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.MAGENTA}📛  ServerName: ", end="")
    server_name = input()

    print(f"{Fore.MAGENTA}📂 DataName: ", end="")
    data_name = input()

    print(f"{Fore.MAGENTA}🔐 Server Password: ", end="")
    server_password = input()

    print(f"{Fore.MAGENTA}🔑 Data Password: ", end="")
    data_password = input()

    servers = load_servers()

    for server in servers:
        if server['ServerName'] == server_name and server['Password'] == server_password:
            # Check if 'Data' key exists, if not create it
            if 'Data' not in server:
                server['Data'] = []

            # Check if DataName already exists
            for data in server['Data']:
                if data['DataName'] == data_name:
                    print(f"{Fore.RED}\n❌ Bu DataName zaten mevcut!")
                    return  # Eğer zaten varsa, fonksiyondan çık

            # Add the data entry to the server if DataName does not exist
            server['Data'].append({'DataName': data_name, 'DataPassword': data_password})
            save_servers(servers)
            print(f"{Fore.YELLOW}\n✨ Data başarıyla eklendi!")
            break
    else:
        print(f"{Fore.RED}\n❌ Sunucu ismi ya da şifre hatalı!")
    
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def list_servers():
    """List all servers with modern output style."""
    servers = load_servers()
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if servers:
        print(Fore.CYAN + "🌐  Mevcut Sunucular:")
        for server in servers:
            print(f"{Fore.RED}🔴  {server['ServerName']}")
    else:
        print(f"{Fore.RED}⚠️  Hiç sunucu bulunamadı.")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def connect_server():
    """Connect to a server by name and password from servers.json."""
    global last_connected_server, in_server  # Global değişkenleri kullanıyoruz
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.MAGENTA}Katılınacak Sunucu İsmi: ", end="")
    server_name = input()

    print(f"{Fore.MAGENTA}Sunucunun Parolası: ", end="")
    server_password = input()

    servers = load_servers()

    for server in servers:
        if server['ServerName'] == server_name and server['Password'] == server_password:
            last_connected_server = server_name  # Son bağlanılan sunucu olarak kaydet
            print(f"{Fore.YELLOW}✨ Sunucuya başarıyla katıldınız: {server_name}")
            enter_last_server()  # Sunucu içindeki komut döngüsüne geç
            return
    print(f"{Fore.RED}❌ Sunucu ismi veya şifre hatalı!")
    print(f"{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def enter_last_server():
    """En son bağlanılan sunucuya gir"""
    global last_connected_server, in_server
    
    if last_connected_server:
        # Yükleme efekti
        print(f"{last_connected_server} sunucusuna giriliyor ━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for i in range(10):
            sys.stdout.write(f"\r{'━' * i}")
            sys.stdout.flush()
            time.sleep(0.2)
        
        print(f"\n✨ {last_connected_server} sunucusunun içine girildi!")
        in_server = True  # Sunucu içinde olduğumuzu belirt
        server_commands()  # Sunucu içindeki komut döngüsüne geç
    else:
        print(Fore.RED + "❌ Henüz hiçbir sunucuya bağlanılmadı.")

def server_commands():
    """Sunucu içinde geçerli olan komutları işleyen fonksiyon."""
    global in_server
    print(Fore.MAGENTA + f"{last_connected_server} sunucusunda komutlar aktif.\n")
    print(f"{Fore.YELLOW}Sunucu içindeki komutlar:")
    print(f"{Fore.GREEN}🔑 exit server -> Sunucudan çıkış yapar.")
    
    while in_server:
        command = input(Fore.MAGENTA + f"{last_connected_server} > ").strip().lower()

        if command == "exit server":
            print(Fore.YELLOW + "Sunucudan çıkılıyor...")
            in_server = False  # Sunucu dışına çık
            print(Fore.YELLOW + f"{last_connected_server} sunucusundan çıkıldı!")
        
        else:
            print(Fore.RED + "❌ Geçersiz komut. Sunucu içindeki komutlar sınırlıdır.")

def generate_easy_password():
    """Generate an easy password based on user preferences."""  
    print(f"{Fore.MAGENTA}Şifre Hanesi (8-16): ", end="")
    length = int(input())
    
    print(f"{Fore.MAGENTA}Sayı olacakmı (Evet/Hayır): ", end="")
    include_numbers = input().strip().lower() == "evet"
    
    print(f"{Fore.MAGENTA}Büyük/Küçük Harf Olacakmı (Evet/Hayır): ", end="")
    include_uppercase = input().strip().lower() == "evet"
    
    characters = string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_uppercase:
        characters += string.ascii_uppercase

    password = ''.join(random.choice(characters) for _ in range(length))
    print(f"{Fore.YELLOW}✨ Oluşturulan Şifre: {password}")

def main():
    """Main function for command processing."""
    print(Fore.CYAN + "Sunucu yönetimi için komutları kullanın.")
    print(Fore.YELLOW + "\nKomutlar:")
    print(f"{Fore.GREEN}⚙️  create server [server name] -> Yeni sunucu oluşturur")
    print(f"{Fore.GREEN}📂  create data -> Sunucuya veri ekler")
    print(f"{Fore.GREEN}📋  list servers -> Sunucu listesini gösterir")
    print(f"{Fore.GREEN}🔑  random key -> Rastgele şifre oluşturur")
    print(f"{Fore.GREEN}🔌  connect server -> Sunucuya katılır")
    print(f"{Fore.GREEN}🔄  server in -> Son bağlanılan sunucuya giriş yapar")
    print(f"{Fore.RED}❌  exit -> Çıkış yapar")

    while True:
        command = input(Fore.MAGENTA + "> ").strip().lower()

        if command.startswith("create server"):
            parts = command.split(" ", 2)
            if len(parts) == 3:
                create_server(parts[2])
            else:
                print(Fore.RED + "❌ Geçersiz kullanım. Doğru kullanım: create server [server name]")
        
        elif command == "create data":
            create_data()
        
        elif command == "list servers":
            list_servers()

        elif command == "random key":
            generate_easy_password()

        elif command == "connect server":
            connect_server()

        elif command == "server in":
            enter_last_server()

        elif command == "exit":
            print(Fore.YELLOW + "Çıkış yapılıyor...")
            break  # Programdan çık

        else:
            print(Fore.RED + "❌ Geçersiz komut.")

if __name__ == "__main__":
    main()
