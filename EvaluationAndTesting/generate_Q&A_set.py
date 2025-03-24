import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

class Gen_QA():
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
        qa_folder='EvaluationAndTesting/Testing_data'
        all_questions_and_answers = []
        
        articles_folder = 'articles'
        for filename in os.listdir(articles_folder):
            if filename.endswith('.txt'):
                title = filename.replace('.txt', '')
                with open(os.path.join(articles_folder, filename), 'r', encoding='utf-8') as file:
                    content = file.read()
                prompt = f"Generate 10 questions and their answers in JSON format based on the following content:\n{content}"
                questions_and_answers = Gen_QA.generate_questions_and_answers(prompt)
                all_questions_and_answers.extend(questions_and_answers)
                print(f"Questions and answers generated for {title}")
        Gen_QA.save_to_file(all_questions_and_answers, os.path.join(qa_folder, 'golden_set.json'))

if __name__ == "__main__":
    Gen_QA.Extract_content()
