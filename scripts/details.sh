file=$1
res=$(ffmpeg -i $file 2>&1 | grep Video: | grep -Po '\d{3,5}x\d{3,5}')
duration=$(ffmpeg -i $file 2>&1 | grep Duration: | grep -Po [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9])
size=$(ls -lah $file | awk '{print $5}')
echo ==== $file ====
echo Resolution: $res
echo Duration: $duration
echo Size: $size
echo =================================
