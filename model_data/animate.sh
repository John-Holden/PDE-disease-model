#!/bin/bash

# Generate a simulation based on frames



dir=fkpp_Fex_b_0_02_ell_25_L/animations

if test -e animations; then
    echo yes exists....
fi


ffmpeg -r 10 -f image2 -s 1920x1080 -i $dir/%05d.png -vcodec libx264 -crf 10  -pix_fmt yuv420p sim.mp4


# ffmpeg -r $rate1 -start_number 0 -i animations/000.png -c:v libx264 -r $rate2 -pix_fmt yuv420p sim_anim.mp4

# echo "animation complete:"
# echo "REMOVE UNWANTED: raw data DATA & temp_frames!!!!"


