from transformers import pipeline

# Load DistilBART summarization model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_text(text):
    summaries = []

    # Split long transcript into chunks
    chunk_size = 1000
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        result = summarizer(
            chunk,
            max_length=130,
            min_length=30,
            do_sample=False
        )
        summaries.append(result[0]["summary_text"])

    return " ".join(summaries)

if __name__ == "__main__":
    with open("transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    summary = summarize_text(transcript)

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("Summary generated using DistilBART")
