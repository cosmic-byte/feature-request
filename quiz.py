from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcj_oxdaJEBwIEqfwXNgCzrFa6M0rHI1aB8y9rFbcQyyQxM' \
          b'-JFIK3oWk2NzXZEf_LyiRLNW_WqoueUknrFLDKtW15KNMu_Otud5JZF2NzGM' \
          b'-eHd5BBDovREjbHb6L8FRur5vL7HQtNo9uDIV6VYyu_iW_3g6P4vcprWtr5J4cI_-6DCBUhWfd-QI9Sv71MeG91DC5m '


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
