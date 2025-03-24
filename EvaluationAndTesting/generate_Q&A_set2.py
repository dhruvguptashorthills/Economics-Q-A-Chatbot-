import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
load_dotenv()

class Gen_QA2():
    def save_to_file(data, filename):
        #if filename doesnot exsist create a new file
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        try:
            with open(filename, 'a', encoding='utf-8') as file:
                for item in data:
                    file.write(f"{item}\n\n")
            print(f"Questions and answers appended to {filename}")

        except Exception as e:
            print(f"An error occurred while saving to file: {e}")

    def generate_questions_and_answers(prompt):
        try:
            genai.configure(api_key=os.getenv("API_KEY"))
            client = genai.GenerativeModel('gemini-1.5-pro-latest')

            response = client.generate_content(
                prompt,
                generation_config = genai.types.GenerationConfig(
                    max_output_tokens=1500,
                    temperature=0.7,
                    top_p=1
                )
            )

            questions_and_answers = []
            if response.text:
                questions_and_answers.append(response.text.strip())
            else:
                print("No text generated in the response.")

            return questions_and_answers

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def Extract_content():
        qa_folder = 'EvaluationAndTesting/Testing_data'
        all_questions_and_answers = {category: [] for category in [
            "multilingual",
            "wrong_vocab_grammar",
            "misleading_out_of_context"
        ]}
        
        articles_folder = 'articles'
        prompts = [
            "Generate 5 multilingual(english with words from different languages like german, french, hindi) questions and their answers in JSON format based on the following content:\n{content}",
            "Generate 5 wrong vocab, grammar but comprehensive questions and their answers in JSON format based on the following content:\n{content}",
            "Generate 5 misleading and out of context questions and their answers in JSON format based on the following content:\n{content}"
        ]
        
        prompt_categories = [
            "multilingual",
            "wrong_vocab_grammar",
            "misleading"
        ]
        
        article_files = [f for f in os.listdir(articles_folder) if f.endswith('.txt')]
        
        for filename in article_files[78:]:
            title = filename.replace('.txt', '')
            with open(os.path.join(articles_folder, filename), 'r', encoding='utf-8') as file:
                content = file.read()
            for prompt_template, category in zip(prompts, prompt_categories):
                prompt = prompt_template.format(content=content)
                questions_and_answers = Gen_QA2.generate_questions_and_answers(prompt)
                all_questions_and_answers[category].extend(questions_and_answers)
                print(f"Questions and answers generated for {title} with prompt: {prompt_template}")
                time.sleep(20)  # Sleep for 2 seconds to avoid API rate limit
        
        for category in prompt_categories:
            category_filename = os.path.join(qa_folder, f'{category}.json')
            Gen_QA2.save_to_file(all_questions_and_answers[category], category_filename)
        
        combined_filename = os.path.join(qa_folder, 'golden_set2.json')
        combined_data = [qa for category in prompt_categories for qa in all_questions_and_answers[category]]
        Gen_QA2.save_to_file(combined_data, combined_filename)

if __name__ == "__main__":
    Gen_QA2.Extract_content()