import os
import re
import time
import traceback
import urllib.request
import socket

socket.setdefaulttimeout(10)

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
WRITE_TO_BASE_DIR = os.path.join(FILE_DIR, "dataset")
BASE_URL = "https://www.flickr.com/search/?text=%KEYWORD&media=photos&page=%PAGE&view_all=1"
KEYWORDS = ['Andromeda', 'Antlia', 'Apus', 'Aquarius', 'Aquila', 'Ara', 'Auriga', 'Caelum', 'Camelopardalis', 'Cancer', 'Canes%20Venatici', 'Canis%20Major', 'Canis%20Minor', 'Capricornus', 'Carina', 'Cassiopeia', 'Centaurus', 'Cepheus', 'Cetus', 'Chamaeleon', 'Circinus', 'Columba', 'Coma%20Berenices', 'Corona%20Australis', 'Corona%20Borealis', 'Corvus', 'Crater', 'Crux', 'Cygnus', 'Delphinus', 'Dorado', 'Draco', 'Equuleus', 'Eridanus', 'Fornax', 'Gemini', 'Grus', 'Hercules', 'Horologium', 'Hydra', 'Hydrus', 'Indus', 'Lacerta', 'Leo', 'Leo%20Minor', 'Lepus', 'Libra', 'Lupus', 'Lynx', 'Lyra', 'Mensa', 'Microscopium', 'Monoceros', 'Musca', 'Norma', 'Octans', 'Ophiuchus', 'Orion', 'Pavo', 'Pegasus', 'Perseus', 'Phoenix', 'Pictor', 'Pisces', 'Piscis%20Austrinus', 'Puppis', 'Pyxis', 'Reticulum', 'Sagitta', 'Sagittarius', 'Scorpius', 'Sculptor', 'Scutum', 'Serpens', 'Sextans', 'Taurus', 'Telescopium', 'Triangulum', 'Triangulum%20Australe', 'Tucana', 'Ursa%20Major', 'Ursa%20Minor', 'Vela']

URLS_LIST_FILEPATH = os.path.join(WRITE_TO_BASE_DIR, "_urls.txt")
PATTERN = re.compile(r"_z\.jpg$")


class ImageDownloader:
    def __init__(self):
        self.urls_list_file = open(URLS_LIST_FILEPATH, "a")

    def __del__(self):
        self.urls_list_file.close()

    def download_images(self):
        for keyword in KEYWORDS:
            keyword += "%20constellation"
            print("[Info] downloading images for keyword '%s'" % (keyword.replace("%20", " ")))
            main_url = BASE_URL.replace("%KEYWORD", keyword)
            dest_dir = os.path.join(WRITE_TO_BASE_DIR, "%s/" % (keyword.replace("%20", "_")))
            try:
                source = self.load_page_source(main_url)
            except Exception as exc:
                traceback.print_exc()
                print(exc)
                source = None

            if source is not None:
                raw_urls = self.extract_image_urls(source)
                urls = set([self.fix_url(url) for url in raw_urls])
                for url in urls:
                    if PATTERN.search(url):
                        print("<Image> %s" % (url))
                        try:
                            downloaded = self.download_image(url, dest_dir)
                            if downloaded:
                                time.sleep(1.0)
                        except Exception as exc:
                            traceback.print_exc()
                            print(exc)

            time.sleep(5.0)

    @staticmethod
    def load_page_source(url):
        response = urllib.request.urlopen(url)
        lines = response.readlines()
        return " ".join(line.decode() for line in lines)

    @staticmethod
    def extract_image_urls(source):
        source = source.replace("\/", "/")
        pattern = re.compile(r"\/\/[a-zA-Z0-9]{1,4}\.staticflickr\.com\/[a-zA-Z0-9\/_]+\.(?:jpg|jpeg|png)")
        matches = re.findall(pattern, source)
        return matches

    @staticmethod
    def fix_url(url):
        if url.startswith("//"):
            return "http:" + url
        else:
            return url

    def download_image(self, source_url, dest_dir):
        if "/" not in source_url or (".jpg" not in source_url and ".jpeg" not in source_url) or "?" in source_url:
            print("[Warning] source url '%s' is invalid" % (source_url))
            return False
        else:
            index = source_url.rfind(".com/")
            image_name = source_url[index + len(".com/"):].replace("/", "-")
            filepath = os.path.join(dest_dir, image_name)
            if os.path.isfile(filepath):
                print("[Info] skipped '%s', already downloaded" % (filepath))
                return False
            else:
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                self.urls_list_file.write("%s\t%s\n" % (source_url, filepath))
                urllib.request.urlretrieve(source_url, filepath)
                return True


if __name__ == "__main__":
    downloader = ImageDownloader()
    downloader.download_images()
