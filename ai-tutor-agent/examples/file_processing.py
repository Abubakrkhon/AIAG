"""
Example: Processing different file types with AI Tutor Agent
"""
from openai import OpenAI
from ai_tutor_agent import create_tutor, create_parsers


def process_pdf_example():
    """Example: Process PDF file"""
    print("\n📄 Processing PDF file...")
    
    client = OpenAI(api_key="your-api-key")
    client.model = "gpt-4o-mini"
    
    tutor = create_tutor(client)
    parsers = create_parsers()
    
    # Parse PDF
    pdf_path = "path/to/your/lecture.pdf"
    result = parsers['pdf'].parse(pdf_path)
    
    print(f"Extracted {len(result['text'])} characters from {len(result['pages'])} pages")
    
    # Process content
    results = tutor.process_content(result['text'], result['metadata'])
    
    # Export
    exported = tutor.export_all("./output/pdf_results", formats=['md', 'json'])
    print(f"Exported to: {exported}")


def process_youtube_example():
    """Example: Process YouTube video"""
    print("\n🎥 Processing YouTube video...")
    
    client = OpenAI(api_key="your-api-key")
    client.model = "gpt-4o-mini"
    
    tutor = create_tutor(client)
    parsers = create_parsers(whisper_model="base")
    
    # Parse YouTube video
    video_url = "https://youtube.com/watch?v=VIDEO_ID"
    result = parsers['youtube'].parse(video_url)
    
    print(f"Transcribed video: {result['metadata']['title']}")
    print(f"Duration: {result['metadata']['duration']} seconds")
    
    # Process content
    results = tutor.process_content(result['text'], result['metadata'])
    
    # Show explanations at different levels
    explanations = results['outputs']['explanations']['explanations']
    
    print("\n--- ELI5 Explanation ---")
    print(explanations.get('child', {}).get('simple_explanation', 'N/A'))
    
    print("\n--- Beginner Explanation ---")
    print(explanations.get('beginner', {}).get('simple_explanation', 'N/A'))


def process_audio_example():
    """Example: Process audio lecture"""
    print("\n🎧 Processing audio file...")
    
    client = OpenAI(api_key="your-api-key")
    client.model = "gpt-4o-mini"
    
    tutor = create_tutor(client)
    parsers = create_parsers(whisper_model="medium")  # Use better model for accuracy
    
    # Parse audio
    audio_path = "path/to/lecture.mp3"
    result = parsers['audio'].parse(audio_path)
    
    print(f"Transcribed {len(result['text'])} characters")
    print(f"Detected language: {result['metadata']['language']}")
    
    # Process content
    results = tutor.process_content(result['text'], result['metadata'])
    
    # Generate clinical case (for medical education)
    if 'медицин' in result['text'][:100].lower() or 'medical' in result['text'][:100].lower():
        print("\n🏥 Creating clinical case...")
        case = tutor.create_clinical_case()
        print(f"Case: {case.get('title', 'N/A')}")
        print(f"Scenario: {case.get('scenario', 'N/A')[:200]}...")


def process_image_example():
    """Example: Process image with OCR"""
    print("\n📷 Processing image (OCR)...")
    
    client = OpenAI(api_key="your-api-key")
    client.model = "gpt-4o-mini"
    
    tutor = create_tutor(client)
    parsers = create_parsers()
    
    # Parse image
    image_path = "path/to/notes.jpg"
    result = parsers['ocr'].parse(image_path)
    
    print(f"Extracted {len(result['text'])} characters from image")
    print(f"Found {len(result['blocks'])} text blocks")
    
    # Process content
    results = tutor.process_content(result['text'], result['metadata'])
    
    # Generate flashcards
    cards = results['outputs']['flashcards']['cards']
    print(f"\nGenerated {len(cards)} flashcards from handwritten notes!")


def batch_processing_example():
    """Example: Batch process multiple files"""
    print("\n📚 Batch processing multiple files...")
    
    client = OpenAI(api_key="your-api-key")
    client.model = "gpt-4o-mini"
    
    tutor = create_tutor(client)
    parsers = create_parsers()
    
    # Multiple PDFs
    pdf_files = [
        "chapter1.pdf",
        "chapter2.pdf",
        "chapter3.pdf"
    ]
    
    all_content = []
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        result = parsers['pdf'].parse(pdf_file)
        all_content.append({
            'text': result['text'],
            'metadata': {**result['metadata'], 'source_file': pdf_file}
        })
    
    # Combine and process
    combined_text = "\n\n".join([c['text'] for c in all_content])
    combined_metadata = {
        'type': 'combined',
        'sources': [c['metadata'] for c in all_content]
    }
    
    results = tutor.process_content(combined_text, combined_metadata)
    
    # Export everything
    exported = tutor.export_all("./output/batch_results", formats=['md', 'json', 'apkg'])
    print(f"\n✅ Batch processing complete!")
    print(f"Exported files: {exported}")


if __name__ == "__main__":
    # Choose which example to run
    print("AI Tutor Agent - File Processing Examples")
    print("=" * 50)
    print("1. Process PDF")
    print("2. Process YouTube video")
    print("3. Process audio")
    print("4. Process image (OCR)")
    print("5. Batch processing")
    
    # Uncomment the example you want to run:
    # process_pdf_example()
    # process_youtube_example()
    # process_audio_example()
    # process_image_example()
    # batch_processing_example()
    
    print("\nTo run examples, uncomment the function call you need.")
