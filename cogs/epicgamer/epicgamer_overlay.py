import ffmpeg
import os

def makeEpicGamer(videoPath, epicGamerVideoPath, position = "rightup"):
    info = ffmpeg.probe(videoPath, cmd=os.getcwd() + "/ffprobe")["streams"][0]
    #make epicgamer overlay and audio
    overlay_file_first = ffmpeg.input(epicGamerVideoPath, ss=112, t=float(info["duration"]) - 3.5)
    overlay_file_second = ffmpeg.input(epicGamerVideoPath, ss=227, t=3.5)
    audio_overlay_first = overlay_file_first.audio
    audio_overlay_second = overlay_file_second.audio
    overlay_file = ffmpeg.concat(
            overlay_file_first,
            audio_overlay_first,
            overlay_file_second,
            audio_overlay_second,
            v=1,
            a=1
        ).node

    overlay_video = overlay_file[0]
    overlay_audio = overlay_file[1]

    stream = ffmpeg.input(videoPath)
    overlay_video = ffmpeg.filter(overlay_video, "scale", info["width"] / 4, info["height"] / 4)
    overlay_audio = ffmpeg.filter(overlay_audio, "volume", 0.2)
    overlay_x, overlay_y = overlay_position(info, position)
    merge_stream = ffmpeg.overlay(stream, overlay_video, shortest=1, x=overlay_x, y=overlay_y)
    audio = ffmpeg.filter([stream.audio, overlay_audio], 'amix')
    filename = os.path.splitext(videoPath)[0]
    stream = ffmpeg.output(merge_stream, audio, filename + '_epicgamer.mp4', threads=1)
    ffmpeg.run(stream, cmd=os.getcwd() + "/ffmpeg", overwrite_output=True)
    return filename + '_epicgamer.mp4'

#return x, y
def overlay_position(info, position):
    if position == "leftup":
        return 0, 0
    if position == "rightup":
        return info["width"] - info["width"] / 4, 0
    if position == "leftdown":
        return 0, info["height"] - info["height"] / 4
    if position == "rightdown":
        return info["width"] - info["width"] / 4, info["height"] - info["height"] / 4
