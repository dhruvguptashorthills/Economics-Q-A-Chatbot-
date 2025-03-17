
```
RAG-project
├─ .env
├─ Data
│  ├─ chunked_data.json
│  ├─ combined_Raw_Data.json
│  ├─ faiss_index.index
│  ├─ faiss_index.json
│  └─ user_queries_log.json
├─ EvaluationAndTesting
│  ├─ Evaluate_model.py
│  ├─ Evaluation
│  │  ├─ CummulativeEvaluationReport.txt
│  │  └─ EvaluationReport.csv
│  ├─ Testing_data
│  │  ├─ generated_answers.csv
│  │  └─ golden_set.json
│  ├─ generate_answers.py
│  └─ generate_Q&A_set.py
├─ Processing
│  ├─ chunker.py
│  ├─ generate_embeddings.py
│  └─ rag_pipeline.py
├─ Scraper
│  ├─ Scraper.py
│  ├─ collector.py
│  └─ list.txt
├─ app.py
└─ articles
   ├─ Aggregate_demand.txt
   ├─ Aggregate_supply.txt
   ├─ Agricultural_economics.txt
   ├─ Austerity.txt
   ├─ Austrian_school_of_economics.txt
   ├─ Balance_of_trade.txt
   ├─ Behavioral_economics.txt
   └─ ...
```