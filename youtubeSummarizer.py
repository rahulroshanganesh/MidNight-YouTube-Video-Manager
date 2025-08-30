from youtube_transcript_api import YouTubeTranscriptApi
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import T5Tokenizer, T5ForConditionalGeneration
from huggingface_hub import snapshot_download
import torch

def videoId(link):
    videoId = link.split("=")[1]
    return videoId


def GetTranscript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        # print("Transcript fetched:", transcript[:3])  # show first 3 lines
        return ' '.join([snippet.text for snippet in transcript])
    except Exception as e:
        print("Transcript fetch failed:", e)
        return ""


# def check(listOfTranscripts):
#     for transcript in listOfTranscripts:
#         if transcript.is_translatable:
#             return True
        
#     return False

def summarizer(tokenizer, model, text, device):
    inputs = tokenizer(
        "summarize: "+text,
        max_length=512,
        truncation=True,
        return_tensors="pt"
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=40
    )
    summary = tokenizer.batch_decode(
        summary_ids, 
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    return summary

def downloadModel():
    snapshot_download("google/pegasus-large")

def callModel(id):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # checkpoint = "google/pegasus-large"
    checkpoint = "t5-base"
    # downloadModel()
    print("Starting....")
    tokenizer  = AutoTokenizer.from_pretrained(checkpoint)
    print("Loaded the Tokenizer for the model....")
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint).to(device)
    print("Loaded the model....")
    transcript_text = GetTranscript(id)
    print("Generated transcripts...")
    print("SUMMARIZZING......")
    pegasus = summarizer(tokenizer, model, transcript_text, device)
    print("Done!!")
    return pegasus[0]
