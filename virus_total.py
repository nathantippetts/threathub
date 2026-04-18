from vault import Vault
import vt

class VirusTotal:
    """
    Allows a user to send IoCs for reputation checks against VirusTotal
    """
    def __init__(self):
        vault = Vault()
        self.query = ""
        self.app = "virus_total"
        # Tries to fetch the API key, if it's not already there then ask the user to supply it
        try:
            self.API_KEY = vault.get_apikey_from_db(self.app)
        except:
            self.API_KEY = vault.get_apikey_from_user()
            # encrypted = vault.encrypt_key(self.API_KEY)
            # vault.store_key(encrypted, self.app)
        finally:
            self.client = vt.Client(self.API_KEY)

    def vt_hash_reputation(self):
        # Takes a user entered hash (doesn't matter type) and sends it to virus total
        # TODO: Figure out how to read in from the web interface
        self.hash = input("Enter a hash: ")
        response = self.client.get_object("/files/{}", self.hash)
        return response

    def vt_url_reputation(self):
        # Takes a user entered URL and sends it to virus total
        # TODO: Figure out how to read in from the web interface
        self.query = input("Enter a URL: ")
        self.url_id = vt.url_id(self.query)
        self.url = self.client.get_object("/urls/{}", self.url_id)
        return self.url

    def vt_parse_scan_results(self, response):
        return response.last_analysis_stats

    def vt_parse_scan_totals(self, response):
        hits = response['malicious'] + response['suspicious']
        total = response['harmless'] + response['malicious'] + response['suspicious'] + response['undetected']
        results = str(hits) + "/" + str(total)
        return results

def main():
    instance = VirusTotal()
    # Lookup file hash
    lookup = instance.vt_hash_reputation()
    print(lookup)
    raw = instance.vt_parse_scan_results(lookup)
    print(raw)
    stats = instance.vt_parse_scan_totals(raw)
    print(stats)
    # Lookup URL
    lookup = instance.vt_url_reputation()
    print(lookup)
    raw = instance.vt_parse_scan_results(lookup)
    print(raw)
    stats = instance.vt_parse_scan_totals(raw)
    print(stats)
    instance.client.close()

if __name__ == "__main__":
    main()