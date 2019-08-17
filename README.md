# SaneBackup

SaneBackup is a simple backup management tool for SideFX Houdini. It allows for
creating checkpoints in your automatic backup saving to more easily use your
backups. This is not true version control, but the tool can also be used for experimenting
and easily switch between different versions.  

## Installation

To install SaneBackup clone or download this repository into your Houdini python script
folder. This can be found at /Documents/houdiniXX.XX/scripts/python. If this folder
does not exist you can make it and Houdini will automatically search for it.

## Usage

SaneBackup is GUI driven program. First, save your file and set your project. Then
launch the GUI. Create a "commit" with a message describing what is special about
this backup. Hit "OK" and your specially marked backup is created.

To load a backup toggle the load option and from the dropdown select your chosen
backup and click "Load".

Please note that SaneBackup creates a .csv file located in the backup folder.
Do not delete this file or you will lose your backup messages.

## License
[MIT](https://choosealicense.com/licenses/mit/)
