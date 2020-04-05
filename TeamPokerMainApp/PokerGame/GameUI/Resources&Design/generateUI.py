import shutil
import os



command = 'pyrcc5 pixels.qrc -o pixels_rc.py'

for file in os.listdir(os.getcwd()):
    if file.endswith('ui'):
        filename = file.split('.')[0]
        command = f'{command} && pyuic5 {filename}.ui -o {filename}UI.py'

print(f'Executing {command} \n')

try:
    result = os.system(command)
    if result is 0:
        pass
except Exception as e:
    print(f'Error {e}')

for file in os.listdir(os.getcwd()):
    if file.endswith('.py') and file != 'generateUI.py':
        print(f'Moving file {file}')
        path_one_folder_up = os.path.abspath(os.path.join(file, "../.."))
        shutil.copy(file, path_one_folder_up + '\\UiCode\\')
        os.remove(file)
