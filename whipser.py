# Description: This script transcribes podcast episodes from an audio file into a TXT file.
import whisper
import os
import opencc

converter = opencc.OpenCC('s2twp')

def write_txt(segments, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for seg in segments:
            text = converter.convert(seg["text"].strip())
            f.write(f"{text}\n")

def main():
    input_dir = "podcast_episodes"
    transcripts_dir = "transcripts"
    if not os.path.exists(transcripts_dir):
        os.makedirs(transcripts_dir)
    model = whisper.load_model("medium")
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".mp3"):
            audio_file = os.path.join(input_dir, filename)
            output_file = os.path.join(transcripts_dir, os.path.splitext(filename)[0] + ".txt")
            print(f"Processing: {audio_file}")
            
            result = model.transcribe(audio_file, language="zh", verbose=True)
            segments = result.get("segments", [])
            if not segments:
                print(f"No segments were detected in {audio_file}, skipping.")
                continue
            
            write_txt(segments, output_file)
            print(f"TXT file generated: {output_file}")
            print("----------------------------------")
            
    print("Processing completed.")
    
    import shutil
    print("Deleting podcast_episodes folder...")
    shutil.rmtree(input_dir)

if __name__ == "__main__":
    main()
