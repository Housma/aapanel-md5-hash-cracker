import hashlib
import argparse
import sys

def aapanel_hash(password, salt):
    """Calculate aaPanel's 3-step MD5 hash"""
    # Step 1: MD5 raw password
    step1 = hashlib.md5(password.encode()).hexdigest()
    
    # Step 2: MD5(step1 + "_bt.cn")
    step2 = hashlib.md5(f"{step1}_bt.cn".encode()).hexdigest()
    
    # Step 3: MD5(step2 + salt)
    return hashlib.md5(f"{step2}{salt}".encode()).hexdigest()

def crack_password(target_hash, salt, wordlist_path):
    """Brute-force using wordlist"""
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            for count, line in enumerate(f, 1):
                password = line.strip()
                if aapanel_hash(password, salt) == target_hash:
                    print(f"\n[+] Password found: {password}")
                    print(f"    Tried {count} passwords")
                    return
                
                # Progress indicator
                if count % 1000 == 0:
                    sys.stdout.write(f"\rAttempts: {count} | Last tried: {password[:20]}")
                    sys.stdout.flush()
                    
        print("\n[-] Password not found in wordlist")

    except FileNotFoundError:
        print(f"Error: Wordlist file {wordlist_path} not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="aaPanel MD5 Hash Cracker")
    parser.add_argument("-H", "--hash", required=True, help="Target hash to crack")
    parser.add_argument("-s", "--salt", required=True, help="Salt used in hash")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to password wordlist")
    
    args = parser.parse_args()
    
    print(f"""
    Starting aaPanel Hash Cracker
    Target Hash: {args.hash}
    Salt:        {args.salt}
    Wordlist:    {args.wordlist}
    """)
    
    try:
        crack_password(args.hash, args.salt, args.wordlist)
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
