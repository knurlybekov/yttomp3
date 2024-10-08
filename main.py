from pytube import YouTube
import os
from moviepy.audio.io.AudioFileClip import AudioFileClip
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def check_ffmpeg():
    # Check if ffmpeg is installed
    if not shutil.which("ffmpeg"):
        raise EnvironmentError("ffmpeg is not installed or not found in PATH. Please install ffmpeg to continue.")


def download_youtube_video(url, output_path='downloads', metadata=None):
    check_ffmpeg()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Download video from YouTube
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video_path = video.download(output_path=output_path)

    # Convert to MP3
    mp3_path = os.path.splitext(video_path)[0] + '.mp3'
    audio_clip = AudioFileClip(video_path)
    audio_clip
    audio_clip.write_audiofile(mp3_path)
    audio_clip.close()

    # Add metadata to MP3
    if metadata:
        audio = MP3(mp3_path, ID3=EasyID3)
        for key, value in metadata.items():
            audio[key] = value
        audio.save()

    # Remove original video file
    os.remove(video_path)

    print(f"Downloaded and converted to MP3: {mp3_path}")
    return mp3_path


if __name__ == "__main__":
    import shutil

    urls = [

    ] # youtube urls

    # Example metadata to be applied to all videos
    metadata = {
        "title": "Sample Title",
        "artist": "Sample Artist",
        "album": "Sample Album",
        "genre": "Sample Genre"
    }

    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        download_youtube_video(url, metadata=metadata)
