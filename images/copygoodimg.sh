# assuming you have $pic_list as an array of all images
# i.e. somethiing like pic_list=`find / -iname "*.jpg"`
for pic in ~/Dev/social-data-project/images/usersPosWtRatings/*.jpg
do
    eog -w $pic &
    echo "Press 'y' to copy $pic to /home/$USER/<dest_folder>"
    read option
    if [ $option = "y" -o $option = "Y" ]
    then
         cp -f $pic ~/Dev/social-data-project/images/good_users/
    else
          echo "will not copy $pic"
    fi
done
