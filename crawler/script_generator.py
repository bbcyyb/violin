import os

from violin_scraper.utility.common import running_path
from violin_scraper.utility.file import File

def run():
    size = 90
    print(f"each script file contains {size} items")
    running_folder = os.path.join(os.path.dirname(running_path()))
    temp_folder = os.path.join(running_folder, 'temp')

    files = os.listdir(temp_folder)

    launch_script = ''

    if len(files) == 0:
        return

    for file in files:
        if file == ".gitkeep":
            continue

        category_ = os.path.splitext(file)[0]
        file_type = os.path.splitext(file)[1]
        if file_type != '.csv':
            continue

        print(f"load [{file}] from {temp_folder}")
        full_name = os.path.join(temp_folder, file)
        fr = File()
        fr.open_file(file=full_name, mode='r')
        lst = fr.read_lines()
        count = len(lst)
        fr.close_file()

        index = 0
        while count > index:
            start = index + 1
            if index + size > count:
                index = count
            else:
                index += size

            end = index

            f_name = generate_file(category_, start, end, running_folder)
            print(f"generate {f_name}")
            launch_script += f'start {f_name} \ntimeout 2 \n'

    if len(launch_script) > 0:
        fw = File()
        fw.open_file(file=os.path.join(running_folder, 'root.bat'), mode='w')
        fw.write(f"{launch_script}", True)
        print("generate root.bat")
        fw.close_file()


def generate_file(category_, start, end, running_folder):
    template = """
@ECHO OFF
set spider_name=qulingyu_download
set spider_category={category}
set spider_range={start},{end}
python3 .\\main.py
    """
    runner_name = f"runner_{category_}_{start}-{end}.bat"
    content = template.format(category=category_, start=start, end=end)

    fw = File()
    fw.open_file(file=os.path.join(running_folder, runner_name), mode='w')
    fw.writeline(content, True)
    fw.close_file()
    return runner_name



if __name__ == "__main__":
    """
    template:
    runner_lingyu_1-50.bat
    """
    run()
