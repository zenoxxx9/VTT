import os
import shutil
import requests
import re

def load_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def clean_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()    
    content = content.replace('{\\an8}', '')
    content = content.replace('<i>', '')
    content = content.replace('</i>', '')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_html(m3u8_link, use_subtitles, image_link, is720, folder_name, srt_path=None):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    response = requests.get(m3u8_link)
    if response.status_code == 200:        
        with open(os.path.join("temp", 'master.m3u8'), 'wb') as f:
            f.write(response.content)
    
    with open("temp/master.m3u8", 'r', encoding='utf-8') as file:
        content = file.read()
        if is720:
            resolution = '1280x720'
            html_without_subtitles = load_template('utils/ms/720p/html_without_subtitles.txt')
            html_with_subtitles = load_template('utils/ms/720p/html_with_subtitles.txt')
        else:
            resolution = '1920x1080'
            html_without_subtitles = load_template('utils/html_without_subtitles.txt')
            html_with_subtitles = load_template('utils/html_with_subtitles.txt')

        if resolution in content:
            html_without_subtitles = load_template('utils/html_without_subtitles.txt')
            html_with_subtitles = load_template('utils/html_with_subtitles.txt')
            print(f"LE MASTER.M3U8 est déjà ajusté à {resolution}")
        else:
            if is720:
                html_without_subtitles = load_template('utils/ms/720p/html_without_subtitles.txt')
                html_with_subtitles = load_template('utils/ms/720p/html_with_subtitles.txt')
            else:
                html_without_subtitles = load_template('utils/ms/html_without_subtitles.txt')
                html_with_subtitles = load_template('utils/ms/html_with_subtitles.txt')
            print(f"LE MASTER.M3U8 n'est pas ajusté à {resolution}")
            pattern = re.compile(r'BANDWIDTH=(\d+)')
            bandwidths_set = set()
            matches = pattern.findall(content)
            for match in matches:
                bandwidths_set.add(int(match[:-3]))
            bandwidths_list = list(bandwidths_set)
            bandwidths_list.sort(reverse=True)
    
    build_path = 'Build'
    if not os.path.exists(build_path):
        os.mkdir(build_path)

    user_folder_path = os.path.join(build_path, folder_name)
    if not os.path.exists(user_folder_path):
        os.mkdir(user_folder_path)
    
    if use_subtitles:
        if srt_path is None or not os.path.isfile(srt_path):
            print("Invalid .srt file path.")
            return      
        
        sub_folder_path = os.path.join(user_folder_path, 'sub')
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)

        srt_destination = os.path.join(sub_folder_path, '1.srt')
        shutil.copy(srt_path, srt_destination)
        clean_srt(srt_destination)
        
        if resolution not in content:
            html_content = html_with_subtitles.replace("REPLACE_M3U8_LINK", m3u8_link).replace("REPLACE_SRT_FILENAME", '1.srt').replace("_THISIMAGE", image_link)
            if not is720:
                placeholders = ["_UN", "_DEUX", "_TROIS", "_QUATRE", "_CINQ", "_SIX", "_SEPT"]
            else:
                placeholders = ["_DEUX", "_TROIS", "_QUATRE", "_CINQ", "_SIX", "_SEPT"]

            for i, placeholder in enumerate(placeholders):
                if i < len(bandwidths_list):
                    html_content = html_content.replace(placeholder, str(bandwidths_list[i]))
        else:
            html_content = html_with_subtitles.replace("REPLACE_M3U8_LINK", m3u8_link).replace("REPLACE_SRT_FILENAME", '1.srt').replace("_THISIMAGE", image_link)
    else:
        if resolution not in content:
            html_content = html_without_subtitles.replace("REPLACE_M3U8_LINK", m3u8_link).replace("_THISIMAGE", image_link)
            if not is720:
                placeholders = ["_UN", "_DEUX", "_TROIS", "_QUATRE", "_CINQ", "_SIX", "_SEPT"]
            else:
                placeholders = ["_DEUX", "_TROIS", "_QUATRE", "_CINQ", "_SIX", "_SEPT"]

            for i, placeholder in enumerate(placeholders):
                if i < len(bandwidths_list):
                    html_content = html_content.replace(placeholder, str(bandwidths_list[i]))
        else:
            html_content = html_without_subtitles.replace("REPLACE_M3U8_LINK", m3u8_link).replace("_THISIMAGE", image_link)

    with open(os.path.join(user_folder_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Files have been successfully created in the folder: {user_folder_path}")
