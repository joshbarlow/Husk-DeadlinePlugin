import os, subprocess, sys
# from System.IO import Path, StreamWriter, File, Directory

# from System.Collections.Specialized import StringCollection
# from System.Text import Encoding


tempDir = os.getenv('TEMP')
deadlineDir = os.getenv('DEADLINE_PATH')

########
sceneFile = "E:/Projects/0008_usd_testing/geo/test_render_02.usd"
startFrame = 1
endFrame = 100
stepSize = 5

renderDelegate = 'BRAY_HdKarma'
DeadlinePlugin = 'Husk'
########

lines = []
lines.append('Name=USD Test python\n')
lines.append('Frames=1-100\n')
lines.append('ChunkSize=10\n')
lines.append('Plugin=Husk\n')

infoFile = os.path.join(tempDir,'huskJobInfo.txt')

with open(infoFile, 'w') as f:
    f.writelines(lines)

lines = []
lines.append('SceneFile=E:/Projects/0008_usd_testing/geo/test_render_02.usd')

pluginFile = os.path.join(tempDir,'huskPluginInfo.txt')

with open(pluginFile, 'w') as f:
    f.writelines(lines)

deadline_cmd = os.path.join(deadlineDir, "deadlinecommand.exe")
##job_file = maya_deadline_job()
##info_file = maya_deadline_info()
command = '{deadline_cmd} "{infoFile}" "{pluginFile}"'.format(**vars())
print(str(command))
process = subprocess.Popen(command, stdout=subprocess.PIPE)
lines_iterator = iter(process.stdout.readline, b"")
#  Lets print the output log to see the Error / Success 
for line in lines_iterator:
    print(line.decode("utf-8").strip())
    sys.stdout.flush()