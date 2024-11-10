import fire
import requests


class Underdog():
    def web_fuzz(self, url, wordlist, payload, method="get"):
        print("[*] Loading wordlist...")
        with open(wordlist, "r") as wordlist_f:
            lines = [line.strip() for line in wordlist_f]
        
        print(f"[*] Loaded {len(lines)} words")
        
        for word in lines:
            if(method=="get"):
                attack_url = url.replace("$"+payload+"$", word)
                response = requests.get(attack_url)
                print(f"Code: {response.code}\tSize: {len(response.text)}")
        

if __name__ == '__main__':
    underdog = Underdog()
    fire.Fire(underdog)


    