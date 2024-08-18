# set up environment variables, aliases, and function

# Change EDA_TOOLS_PATH to the location of the EDA tools
setenv EDA_TOOLS_PATH /home/lab.apps/vlsiapps_new
setenv EDA_CSHRC_PATH ${EDA_TOOLS_PATH}/cshrc

source ${EDA_CSHRC_PATH}/general.cshrc
# Any other tool specific environments (.cshrc files) can be set here..


# Set location of the PDKs/technology files
setenv PDK_DIR /home/projects/ee478/common/45nmFreePDK_envsetup/common/freepdk45_opencelllibrarypdk45/FreePDK45 
# Do not change the following lines
umask 002

