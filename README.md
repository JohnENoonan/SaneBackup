# SaneBackup

SaneBackup is a simple backup management tool for SideFX Houdini. It allows for
creating checkpoints in your automatic backup saving to more easily use your
backups and iterate more quickly. This is not true version control, but for small
projects not requiring collaboration it is probably sufficient.  

## Installation

To install SaneBackup clone or download this repository into your Houdini python script
folder. This can be found at /Documents/houdiniXX.XX/scripts/python. If this folder
does not exist you can make it and Houdini will automatically search for it.

## Usage

SaneBackup is a GUI driven program. First, set your project and save your file. Then
launch the GUI. Create a "commit" with a message describing what is special about
this backup. Hit "Make Commit" and your specially marked backup is created.

To load a backup toggle the load option and from the dropdown select your chosen
backup and click "Load".

Please note that SaneBackup creates a .csv file located in the backup folder.
Do not delete this file or you will lose your backup messages.

## License
[MIT](https://choosealicense.com/licenses/gpl-3.0/)
