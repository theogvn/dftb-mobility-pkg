#!/usr/bin/env python3

dftb_in = open('dftb_in.hsd')
dftb_content = dftb_in.readlines()
dftb_in.close()

new_setting = open("../transport_settings.hsd")
new_setting_content = new_setting.readlines()
new_setting.close()

SourceSettings = open("../source_settings.hsd")
SourceSettings_content = SourceSettings.readlines()
SourceSettings.close()

DrainSettings = open("../drain_settings.hsd")
DrainSettings_content = DrainSettings.readlines()
DrainSettings.close()

taskFlag = False
hamiltonianFlag = False
sourceFlag = False
drainFlag = False

new_dftb_in_content = []

for i in range(len(dftb_content)):
    if 'Task' in dftb_content[i]:
        taskFlag = True

    if 'Id = "source"' in dftb_content[i] and taskFlag is False:
        sourceFlag = True

    if 'Id = "drain"' in dftb_content[i] and taskFlag is False:
        drainFlag = True

    if 'Hamiltonian = DFTB' in dftb_content[i]:
        hamiltonianFlag = True

    if hamiltonianFlag is True:
        new_dftb_in_content.extend(new_setting_content)
        break

    if taskFlag is False:
        new_dftb_in_content.append(dftb_content[i])

    if sourceFlag is True:
        new_dftb_in_content.extend(SourceSettings_content)
        sourceFlag = False

    if drainFlag is True:
        new_dftb_in_content.extend(DrainSettings_content)
        drainFlag = False

    if '}' in dftb_content[i]:
        taskFlag = False


new_dftb_in_file = open("dftb_in.hsd", "w")
for line in new_dftb_in_content:
    new_dftb_in_file.write(line)
new_dftb_in_file.close()
