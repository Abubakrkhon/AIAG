"""
Example usage of AI Tutor Agent
"""
from openai import OpenAI
from ai_tutor_agent import create_tutor, create_parsers


def main():
    # Initialize LLM client
    client = OpenAI(api_key="your-api-key")
    client.model = "gpt-4o-mini"
    
    # Create tutor agent
    tutor = create_tutor(client)
    
    # Sample educational content
    sample_content = """
    Фотосинтез - это процесс преобразования энергии света в химическую энергию.
    
    Основные этапы фотосинтеза:
    1. Световая фаза - происходит в тилакоидах хлоропластов
       - Поглощение света хлорофиллом
       - Фотолиз воды с выделением кислорода
       - Синтез АТФ и НАДФ·H2
    
    2. Темновая фаза (цикл Кальвина) - происходит в строме хлоропластов
       - Фиксация CO2
       - Восстановление до глюкозы
       - Использование АТФ и НАДФ·H2
    
    Уравнение фотосинтеза:
    6CO2 + 6H2O + свет → C6H12O6 + 6O2
    
    Значение фотосинтеза:
    - Производство органических веществ
    - Выделение кислорода
    - Поглощение углекислого газа
    - Основа пищевых цепей
    """
    
    print("🚀 Processing educational content...\n")
    
    # Process content through full pipeline
    results = tutor.process_content(sample_content)
    
    # Display results
    print("\n" + "="*50)
    print("📊 ANALYSIS RESULTS")
    print("="*50)
    print(f"\nMain Topic: {results['analysis'].get('main_topic', 'N/A')}")
    print(f"Difficulty: {results['analysis'].get('difficulty', 'N/A')}")
    print(f"Key Concepts: {', '.join(results['analysis'].get('key_concepts', [])[:5])}")
    
    print("\n" + "="*50)
    print("📒 SUMMARY")
    print("="*50)
    print(results['outputs']['summary']['content'][:500] + "...")
    
    print("\n" + "="*50)
    print("🎯 SIMPLE EXPLANATION (ELI5)")
    print("="*50)
    explanations = results['outputs']['explanations']['explanations']
    if 'child' in explanations:
        print(explanations['child'].get('simple_explanation', 'N/A'))
    
    print("\n" + "="*50)
    print("🧠 SAMPLE FLASHCARDS")
    print("="*50)
    cards = results['outputs']['flashcards']['cards'][:3]
    for i, card in enumerate(cards, 1):
        print(f"\n{i}. Q: {card['front']}")
        if card['back']:
            print(f"   A: {card['back']}")
    
    print("\n" + "="*50)
    print("📝 SAMPLE TEST QUESTIONS")
    print("="*50)
    questions = results['outputs']['tests']['questions'][:2]
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. [{q['type']}] {q['question']}")
        if q.get('options'):
            for opt, text in q['options'].items():
                print(f"   {opt}) {text}")
        print(f"   ✓ Answer: {q['correct_answer']}")
    
    print("\n" + "="*50)
    print("✅ Processing complete!")
    print(f"Generated: {len(cards)} flashcards, {len(questions)} test questions")
    print("="*50)


if __name__ == "__main__":
    main()
