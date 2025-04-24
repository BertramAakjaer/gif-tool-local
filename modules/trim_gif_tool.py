from PIL import Image, ImageSequence
import os

def trim_gif(input_path, cut_start=0.0, cut_end=0.0, force_fps=None):

    with Image.open(input_path) as im:
        frames = []
        durations = []

        total_duration = 0


        # Samler alle frames i gif'en og hvor langt tid de varer og ligger det til den totale længde
        for frame in ImageSequence.Iterator(im):
            duration = frame.info.get("duration", 100)
            total_duration += duration
            durations.append(duration)
            frames.append(frame.copy())

        # Omformer de afskåret sekundter til millisekunder og udregner tiden der skal beholdes
        start_cutoff = int(cut_start * 1000)
        end_cutoff = int(cut_end * 1000)
        keep_duration = total_duration - start_cutoff - end_cutoff

        # Giver fejl hvis der fjernes flere sekunder end der er i gif'em
        if keep_duration <= 0:
            raise ValueError("GIF too short to trim that much.")

        trimmed_frames = []
        trimmed_durations = []
        current_duration = 0

        # Springer alle frames inden for start_cutoff over, og samler alle frames derfra, indtil end_cutoff samt deres længde
        for frame, dur in zip(frames, durations):
            if current_duration + dur < start_cutoff:
                current_duration += dur
                continue
            if current_duration >= (start_cutoff + keep_duration):
                break
            trimmed_frames.append(frame)
            trimmed_durations.append(dur)
            current_duration += dur
        
        output_path = os.path.join("temp", os.path.basename(input_path).replace(".gif", "_trimmed.gif"))

        # Gemmer den nye, cut gif
        trimmed_frames[0].save(
            output_path,
            save_all=True,
            append_images=trimmed_frames[1:],
            duration=trimmed_durations,
            loop=0,
            disposal=2,
            optimize=False,
        )