# Input 1: path to json file of episodes
# Input 2: number of episodes to download (i.e. 5 will only check the 5 most recent episodes)

limit=$2
dir=$3
count=1

jq -c '.[]' $1 | while IFS= read -r item; do
    title=$(echo "$item" | jq -r '.title')
    url=$(echo "$item" | jq -r '.url')
    timestamp=$(echo "$item" | jq -r '.timestamp')
    description=$(echo "$item" | jq -r '.description')
    thumbnail=$(echo "$item" | jq -r '.thumbnail')

    echo "Title: $title, URL: $url, Timestamp: $timestamp"
    filename=$dir/$(echo -n "$title" | md5sum | cut -d ' ' -f 1).mp3
    echo $filename

    if [ -f "$filename" ]; then
      echo "'$title' has already been downloaded."
    else
      echo "Downloading '$title'."
      yt-dlp --cookies cookies.txt -f bestaudio -o $filename --extract-audio --audio-format mp3 $url

      filesize=`du -k "$filename" | cut -f1`

      echo "Adding to RSS feed"
      python update_feed.py $dir/feed.rss --title "$title" --url "https://github.com/DAKLabb/pod-tube/raw/refs/heads/main/$dir/$filename" --bytes $filesize --guid "$filename" --timestamp $timestamp --thumbnail $thumbnail --link $url --description "$description"
    fi

    if [[ $count -eq $limit ]]; then
        echo "Done checking the $limit most recent episodes"
        break  # Exit the loop when we have hit the limit
    fi
    count=$((count + 1))
done