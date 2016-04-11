import time
import datetime
import os
import os.path
import zipfile
import glob
from zipfile import ZIP_DEFLATED


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            if s == "System Volume Information":
                continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

def backup(filepath):

    from_dir = 'G:\\'
    # backup_time
    back_time = time.strftime(u'%Y-%m-%d_%H-%M')

    to_dir = filepath + u':\\backup'
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
        print u'Completely New Folder.'
    os.chdir(to_dir)

    target = back_time + u'.zip'

    if not os.path.exists(target):
        zip = zipfile.ZipFile(target, 'a', ZIP_DEFLATED)
        print u'Finding files ...'
        file = GetFileList(from_dir, [])
        print u'Zipping...'
        for f in file:
            zip.write(f)
        print u'Done.'
        zip.close()
    else:
        print u'Having Backups.'

    os.chdir(to_dir)
    list_file = os.listdir(to_dir)

    old_time = datetime.date.today() - datetime.timedelta(30)
    # print str(old_time)[5:7]
    for lis in list_file:
        if lis[5:7] == str(old_time)[5:7]:
            os.remove(lis)


if __name__ == '__main__':

    if os.path.exists('G:') == True:
        backup('D')
