import pathlib
import threading, subprocess
from time import sleep
import PySimpleGUI as sg
import requests, zipfile


def popup_prediction():
    col_layout = [[sg.Button('OK', size=(8, 1))]]
    layout = [
        [sg.Text("Cập nhật thành công", font=('Helvetica', 16), pad=(30, 30))],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Thông báo", layout, use_default_focus=False, finalize=True, modal=True)
    event, values = window.read()
    window.close()
    return None


def download_file(window):
    url = "https://bsite.net/tuanvu02/update.zip"
    with requests.get(url, stream=True) as r:
        chunk_size = 64 * 1024
        total_length = int(r.headers.get('content-length'))
        total = total_length // chunk_size if total_length % chunk_size == 0 else total_length // chunk_size + 1
        with open(f'{rootPath}/update.zip', 'wb') as f:
            for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                f.write(chunk)
                percentE = int((i + 1) / total * 100)
                window.write_event_value('Next', percentE)


if __name__ == "__main__":
    rootPath = pathlib.Path(__file__).parent.resolve()
    percentE = None
    sg.theme("SystemDefault")

    progress_bar = [
        [sg.ProgressBar(100, size=(40, 20), pad=(30, 20), key='Progress Bar'),
         sg.Text("  0%", size=(4, 1), key='Percent'), ],

    ]

    layout = [
        [sg.pin(sg.Column(progress_bar, key='Progress', visible=False))],
        [sg.Text('Đang cập nhật...', pad=(190, 0), font=('Helvetica', 13), key='Install')],
    ]
    window = sg.Window('Cập nhật', layout, size=(520, 120), finalize=True, use_default_focus=False)
    progress_bar = window['Progress Bar']
    percent = window['Percent']
    progressB = window['Progress']
    installText = window['Install']
    window.write_event_value('Download', percentE)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Download':
            count = 0
            progress_bar.update(current_count=0, max=100)
            progressB.update(visible=True)
            thread = threading.Thread(target=download_file, args=(window,), daemon=True)
            thread.start()
        elif event == 'Next':
            count = values[event]
            progress_bar.update(current_count=count)
            percent.update(value=f'{count:>3d}%')
            window.refresh()
            if count == 100:
                with zipfile.ZipFile(f'{rootPath}/update.zip', 'r') as zip_ref:
                    zip_ref.extractall(f"{rootPath}")
                subprocess.run(f"hdiutil attach {rootPath}/FineTest.dmg", shell=True)
                subprocess.run("cp -R /Volumes/FineTest/FineTest.app /Applications", shell=True)
                subprocess.run("hdiutil detach /Volumes/FineTest", shell=True)
                subprocess.run(f"rm -rf {rootPath}/FineTest.dmg", shell=True)
                subprocess.run(f"rm -r {rootPath}/__MACOSX", shell=True)
                subprocess.run(f"rm -rf {rootPath}/update.zip", shell=True)
                # popup_prediction()
                break

    window.close()


















