
import re
import requests

MAX_PAGES = 6
download_folder = "F:\\06_pictures\download"
page_url = "http://simpledesktops.com/browse/"
log_file_path = "F:\\06_pictures\download\download_info.txt"
pic_names_list = []

pic_count = 0
log_file = open(log_file_path, mode="w")
for i in range(5, MAX_PAGES):
    r = requests.get(page_url + str(i) + "/")
    print(page_url + str(i) + "/")
    url_pattern = re.compile(
        "http://static.simpledesktops.com/uploads/desktops/[^\"]*\.png\.")
    match = url_pattern.findall(r.text)
    print("begin .....")
    for url in match:
        pic_count += 1
        url = url[:-1]
        pic_url_request = requests.get(url)
        pic_name = url[61:]
        pic_names_list.append(pic_name)
        pic_path = download_folder + "\\" + pic_name
        print("downloading " + pic_name + " ......")
        with open(pic_path, mode="wb") as file:
            file.write(pic_url_request.content)
pic_names_list = sorted(pic_names_list)
for name in pic_names_list:
    log_file.write(name + "\n")
log_file.write("download " + str(pic_count) + "pictures\n")
print 'Done...'
