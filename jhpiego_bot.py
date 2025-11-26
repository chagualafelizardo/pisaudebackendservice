# jhpiego_bot.py
import os
import re
import logging
import PyPDF2
import docx
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class JhpiegoBot:
    def __init__(self, upload_dir='uploads'):
        self.UPLOAD_DIR = upload_dir
        self._ensure_upload_dir()
        
        # Tópicos expandidos para saúde
        self.TOPIC_KEYWORDS = {
            "hiv": ["hiv", "sida", "aids", "vírus", "antiretroviral", "cd4", "carga viral", "arv"],
            "malaria": ["malaria", "mosquito", "plasmodium", "anopheles", "quinino", "febre", "parasita"],
            "tuberculose": ["tb", "tuberculose", "bacilo", "pulmonar", "tosse", "bcg", "mycobacterium"],
            "gravidez": ["gravidez", "gestação", "parto", "pré-natal", "obstétrica", "neonatal"],
            "vacinação": ["vacina", "imunização", "vacinação", "calendário", "dose", "imune"],
            "cuidados infantis": ["criança", "infantil", "pediátrico", "neonatal", "recém-nascido"],
            "nutrição": ["nutrição", "alimentação", "dieta", "suplemento", "vitamina"],
            "higiene": ["higiene", "sanitário", "limpeza", "lavagem", "saneamento"]
        }
        
        logger.info("✅ Jhpiego Bot inicializado")

    def _ensure_upload_dir(self):
        """Garante que o diretório de uploads existe"""
        if not os.path.exists(self.UPLOAD_DIR):
            os.makedirs(self.UPLOAD_DIR)
            logger.info(f"📁 Diretório '{self.UPLOAD_DIR}' criado")

    # --- Funções para ler arquivos ---
    def read_txt(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"❌ Erro ao ler TXT {file_path}: {e}")
            return ""

    def read_pdf(self, file_path):
        try:
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"❌ Erro ao ler PDF {file_path}: {e}")
            return ""

    def read_docx(self, file_path):
        try:
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            logger.error(f"❌ Erro ao ler DOCX {file_path}: {e}")
            return ""

    def read_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            return df.to_csv(index=False)
        except Exception as e:
            logger.error(f"❌ Erro ao ler Excel {file_path}: {e}")
            return ""

    def load_files(self):
        """Carrega todos os arquivos do diretório de uploads"""
        data = ""
        file_count = 0
        
        if not os.path.exists(self.UPLOAD_DIR):
            logger.warning(f"❌ Diretório '{self.UPLOAD_DIR}' não encontrado")
            return data

        for filename in os.listdir(self.UPLOAD_DIR):
            path = os.path.join(self.UPLOAD_DIR, filename)
            if os.path.isfile(path):
                file_content = ""
                
                if filename.endswith('.txt'):
                    file_content = self.read_txt(path)
                elif filename.endswith('.pdf'):
                    file_content = self.read_pdf(path)
                elif filename.endswith('.docx'):
                    file_content = self.read_docx(path)
                elif filename.endswith('.xlsx'):
                    file_content = self.read_excel(path)
                
                if file_content.strip():
                    data += f"\n\n--- Documento: {filename} ---\n{file_content}"
                    file_count += 1
        
        logger.info(f"📚 Carregados {file_count} documentos")
        return data

    def clean_terms(self, text):
        """Limpa e tokeniza texto"""
        stopwords = ["o", "a", "os", "as", "de", "do", "da", "que", "é", "e", "para", "em", "um", "uma"]
        words = re.findall(r"\w+", text.lower())
        return [w for w in words if w not in stopwords and len(w) > 2]

    def detect_topic(self, question):
        """Detecta tópico com scoring"""
        q = question.lower()
        topic_scores = {}
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in q)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            best_topic = max(topic_scores.items(), key=lambda x: x[1])
            logger.info(f"🎯 Tópico detectado: {best_topic[0]} (score: {best_topic[1]})")
            return best_topic[0]
        
        return None

    def semantic_search(self, question, documents_text):
        """Busca semântica por similaridade"""
        try:
            # Dividir em documentos individuais
            docs = []
            doc_files = []
            
            for filename in os.listdir(self.UPLOAD_DIR):
                path = os.path.join(self.UPLOAD_DIR, filename)
                if os.path.isfile(path) and filename.endswith(('.txt', '.pdf', '.docx', '.xlsx')):
                    content = ""
                    if filename.endswith('.txt'):
                        content = self.read_txt(path)
                    elif filename.endswith('.pdf'):
                        content = self.read_pdf(path)
                    elif filename.endswith('.docx'):
                        content = self.read_docx(path)
                    elif filename.endswith('.xlsx'):
                        content = self.read_excel(path)
                    
                    if content.strip():
                        docs.append(content)
                        doc_files.append(filename)
            
            if not docs:
                return None, None
            
            # Calcular similaridade TF-IDF
            vectorizer = TfidfVectorizer(stop_words=self.clean_terms(""))
            tfidf_matrix = vectorizer.fit_transform([question] + docs)
            
            cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            best_match_idx = np.argmax(cosine_similarities)
            best_score = cosine_similarities[best_match_idx]
            
            logger.info(f"🎯 Melhor match: {doc_files[best_match_idx]} - Score: {best_score:.3f}")
            
            if best_score > 0.1:
                return docs[best_match_idx], doc_files[best_match_idx]
            
        except Exception as e:
            logger.error(f"❌ Erro no search semântico: {e}")
        
        return None, None

    def extract_relevant_part(self, full_text, question, topic):
        """Extrai a parte mais relevante do documento"""
        paragraphs = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) > 50]
        
        if not paragraphs:
            return full_text[:500] + "..." if len(full_text) > 500 else full_text
        
        # Ranking de parágrafos por relevância
        scored_paragraphs = []
        topic_keywords = self.TOPIC_KEYWORDS.get(topic, [])
        question_words = self.clean_terms(question)
        
        for i, paragraph in enumerate(paragraphs):
            score = 0
            
            # Score por keywords do tópico
            for kw in topic_keywords:
                if kw in paragraph.lower():
                    score += 2
            
            # Score por palavras da pergunta
            for word in question_words:
                if word in paragraph.lower():
                    score += 1
            
            # Bônus para parágrafos com tamanho adequado
            if 100 <= len(paragraph) <= 800:
                score += 1
            
            scored_paragraphs.append((score, paragraph, i))
        
        # Ordenar e pegar os melhores
        scored_paragraphs.sort(reverse=True)
        top_paragraphs = [p[1] for p in scored_paragraphs[:2] if p[0] > 0]
        
        if top_paragraphs:
            return "\n\n".join(top_paragraphs)
        else:
            return paragraphs[0]  # Fallback

    def process_query(self, question):
        """Processa a pergunta e retorna resposta"""
        question = question.strip()
        
        if not question:
            return {
                "response": "Por favor, faça uma pergunta.",
                "topic": None,
                "source": None
            }
        
        # Detectar tópico
        topic = self.detect_topic(question)
        
        if not topic:
            return {
                "response": "Não consegui identificar o tema (HIV, Malaria, Tuberculose, Gravidez, etc). Pode reformular mencionando o tema específico?",
                "topic": None,
                "source": None
            }
        
        # Busca semântica
        relevant_doc, doc_name = self.semantic_search(question, self.load_files())
        
        if not relevant_doc:
            return {
                "response": f"Não encontrei informações suficientes sobre {topic} nos documentos carregados.",
                "topic": topic,
                "source": None
            }
        
        # Extrair parte relevante
        best_response = self.extract_relevant_part(relevant_doc, question, topic)
        
        logger.info(f"✅ Resposta gerada - Tópico: {topic} - Documento: {doc_name}")
        
        return {
            "response": best_response,
            "topic": topic,
            "source": doc_name
        }

# Instância global do bot
jhpiego_bot = JhpiegoBot()