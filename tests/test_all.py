import unittest
import subprocess
import os
import tempfile
import shutil

class TestPythonFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_script(self, script_path):
        result = subprocess.run(['python3', script_path], capture_output=True, text=True, cwd=self.test_dir)
        self.assertEqual(result.returncode, 0, f"{os.path.basename(script_path)} failed with error: {result.stderr}")

    def test_scraper(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/Scraper/Scraper.py')

    def test_rag_pipeline(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/Processing/rag_pipeline.py')

    def test_generate_embeddings(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/Processing/generate_embeddings.py')

    def test_chunker(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/Processing/chunker.py')

    def test_generate_QA_set(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/EvaluationAndTesting/generate_Q&A_set.py')

    def test_generate_QA_set2(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/EvaluationAndTesting/generate_Q&A_set2.py')

    def test_generate_answers(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/EvaluationAndTesting/generate_answers.py')

    def test_generate_answers2(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/EvaluationAndTesting/generate_answers2.py')

    def test_evaluate_model(self):
        self.run_script('/home/shtlp_0152/Desktop/Assignments/mini-project/EvaluationAndTesting/Evaluate_model.py')

    def test_app_ui(self):
        result = subprocess.run(['streamlit', 'run', '/home/shtlp_0152/Desktop/Assignments/mini-project/app.py'], capture_output=True, text=True, cwd=self.test_dir, timeout=10)
        self.assertIn("Economics Q&A System", result.stdout, "Streamlit app did not start correctly")

if __name__ == "__main__":
    unittest.main()
