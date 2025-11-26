# bot/jhpiego_bot.py (VERSÃO CORRIGIDA)
import os
import re
import logging
import PyPDF2
import docx
import pandas as pd
from collections import Counter

logger = logging.getLogger(__name__)

class JhpiegoBot:
    def __init__(self, upload_dir='uploads'):
        self.UPLOAD_DIR = upload_dir
        self._ensure_upload_dir()
        
        # Tópicos expandidos para saúde
        self.TOPIC_KEYWORDS = {
            "hiv": ["hiv", "sida", "aids", "vírus", "antiretroviral", "cd4", "carga viral", "arv", "tratamento"],
            "malaria": ["malária", "mosquito", "plasmodium", "anopheles", "quinino", "febre", "parasita", "sintomas"],
            "tuberculose": ["tb", "tuberculose", "bacilo", "pulmonar", "tosse", "bcg", "mycobacterium", "diagnóstico"],
            "gravidez": ["gravidez", "gestação", "parto", "pré-natal", "obstétrica", "neonatal", "cuidados"],
            "vacinação": ["vacina", "imunização", "vacinação", "calendário", "dose", "imune", "campanha"],
            "cuidados infantis": ["criança", "infantil", "pediátrico", "neonatal", "recém-nascido", "aleitamento"],
            "nutrição": ["nutrição", "alimentação", "dieta", "suplemento", "vitamina", "desnutrição"],
            "higiene": ["higiene", "sanitário", "limpeza", "lavagem", "saneamento", "prevenção"]
        }
        
        logger.info("✅ Jhpiego Bot inicializado (versão melhorada)")

    def _ensure_upload_dir(self):
        """Garante que o diretório de uploads existe"""
        if not os.path.exists(self.UPLOAD_DIR):
            os.makedirs(self.UPLOAD_DIR)
            logger.info(f"📁 Diretório '{self.UPLOAD_DIR}' criado")

    # --- Funções para ler arquivos (MANTIDAS) ---
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
            return df.to_string(index=False)
        except Exception as e:
            logger.error(f"❌ Erro ao ler Excel {file_path}: {e}")
            return ""

    def clean_terms(self, text):
        """Limpa e tokeniza texto de forma mais eficaz"""
        stopwords = {
            "o", "a", "os", "as", "de", "do", "da", "que", "é", "e", "para", "em", "um", "uma",
            "com", "por", "se", "na", "no", "nas", "nos", "uma", "um", "em", "por", "para", "com",
            "não", "sim", "como", "mas", "ou", "porque", "porquê", "quando", "onde", "qual"
        }
        # Melhor regex para capturar palavras
        words = re.findall(r'\b[a-záéíóúâêîôûãõç]{3,}\b', text.lower())
        return [w for w in words if w not in stopwords]

    def detect_topic(self, question):
        """Detecta tópico com scoring melhorado"""
        q = question.lower()
        topic_scores = {}
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            score = 0
            for kw in keywords:
                # Bônus maior se a palavra-chave for exata
                if f" {kw} " in f" {q} ":
                    score += 3
                elif kw in q:
                    score += 2
            
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            best_topic = max(topic_scores.items(), key=lambda x: x[1])
            logger.info(f"🎯 Tópico detectado: {best_topic[0]} (score: {best_topic[1]})")
            return best_topic[0]
        
        return None

    def calculate_advanced_similarity(self, question, text):
        """Calcula similaridade mais inteligente"""
        question_terms = self.clean_terms(question)
        text_terms = self.clean_terms(text)
        
        if not question_terms:
            return 0.0
        
        # Contar ocorrências
        question_counter = Counter(question_terms)
        text_counter = Counter(text_terms)
        
        # Calcular similaridade ponderada
        total_score = 0
        for word, q_count in question_counter.items():
            if word in text_counter:
                # Score baseado na frequência e importância
                word_score = min(q_count, text_counter[word])
                
                # Palavras mais longas são mais importantes
                length_bonus = min(len(word) / 10, 0.5)
                
                total_score += word_score + length_bonus
        
        # Normalizar pelo número de palavras únicas na pergunta
        normalized_score = total_score / len(question_terms)
        
        # Bônus para textos que contêm palavras da pergunta no início
        first_200_chars = text[:200].lower()
        bonus = 0
        for word in question_terms:
            if word in first_200_chars:
                bonus += 0.1
        
        final_score = min(normalized_score + bonus, 1.0)
        return final_score

    def semantic_search(self, question):
        """Busca semântica MELHORADA com ranking"""
        try:
            documents = []
            
            # Primeiro: coletar todos os documentos
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
                        documents.append({
                            'filename': filename,
                            'content': content,
                            'score': 0
                        })
            
            if not documents:
                logger.warning("❌ Nenhum documento encontrado para busca")
                return None, None
            
            # Segundo: calcular score para CADA documento
            scored_documents = []
            for doc in documents:
                score = self.calculate_advanced_similarity(question, doc['content'])
                doc['score'] = score
                scored_documents.append(doc)
            
            # Terceiro: ORDENAR por score (maior primeiro)
            scored_documents.sort(key=lambda x: x['score'], reverse=True)
            
            # Log detalhado dos scores
            logger.info("📊 Ranking de documentos:")
            for i, doc in enumerate(scored_documents[:3]):  # Top 3
                logger.info(f"   {i+1}. {doc['filename']}: {doc['score']:.3f}")
            
            # Quarto: retornar o MELHOR documento (se tiver score suficiente)
            best_doc = scored_documents[0]
            
            if best_doc['score'] > 0.15:  # Threshold ajustado
                logger.info(f"🎯 Selecionado: {best_doc['filename']} (score: {best_doc['score']:.3f})")
                return best_doc['content'], best_doc['filename']
            else:
                logger.warning(f"⚠️ Melhor score muito baixo: {best_doc['score']:.3f}")
                return None, None
            
        except Exception as e:
            logger.error(f"❌ Erro no search semântico: {e}")
            return None, None

    def extract_relevant_part(self, full_text, question, topic):
        """Extrai a parte MAIS RELEVANTE baseada na pergunta"""
        # Dividir em parágrafos significativos
        paragraphs = []
        for p in re.split(r'\n\s*\n', full_text):
            clean_p = p.strip()
            if len(clean_p) > 30:  # Parágrafos muito curtos são ignorados
                paragraphs.append(clean_p)
        
        if not paragraphs:
            return full_text[:400] + "..." if len(full_text) > 400 else full_text
        
        # Score cada parágrafo baseado na pergunta
        scored_paragraphs = []
        question_terms = self.clean_terms(question)
        topic_keywords = self.TOPIC_KEYWORDS.get(topic, [])
        
        for i, paragraph in enumerate(paragraphs):
            score = 0
            
            # 1. Score por palavras da PERGUNTA (mais importante)
            for word in question_terms:
                if word in paragraph.lower():
                    score += 2  # Bônus maior para palavras da pergunta
            
            # 2. Score por keywords do TÓPICO
            for kw in topic_keywords:
                if kw in paragraph.lower():
                    score += 1.5
            
            # 3. Bônus para parágrafos que respondem perguntas diretas
            question_lower = question.lower()
            if any(q_word in question_lower for q_word in ['como', 'quando', 'onde', 'qual', 'quais']):
                if any(a_word in paragraph.lower() for a_word in ['deve', 'dever', 'precisa', 'necessita', 'recomenda']):
                    score += 1
            
            # 4. Bônus para parágrafos de tamanho ideal
            if 80 <= len(paragraph) <= 600:
                score += 0.5
            
            scored_paragraphs.append((score, paragraph, i))
        
        # Ordenar por score e pegar os MELHORES
        scored_paragraphs.sort(reverse=True)
        
        # Selecionar os 2 melhores parágrafos com score > 0
        top_paragraphs = []
        for score, paragraph, idx in scored_paragraphs:
            if score > 0 and len(top_paragraphs) < 2:
                top_paragraphs.append(paragraph)
            elif len(top_paragraphs) >= 2:
                break
        
        # Se não encontrou parágrafos relevantes, usar estratégia fallback
        if not top_paragraphs:
            # Tentar encontrar parágrafos que contenham palavras da pergunta
            for paragraph in paragraphs:
                if any(term in paragraph.lower() for term in question_terms[:3]):  # 3 primeiras palavras
                    top_paragraphs.append(paragraph)
                    if len(top_paragraphs) >= 2:
                        break
            
            # Fallback final: primeiros parágrafos
            if not top_paragraphs:
                top_paragraphs = paragraphs[:2]
        
        # Juntar os parágrafos selecionados
        result = "\n\n".join(top_paragraphs)
        
        # Garantir que a resposta não seja muito longa
        if len(result) > 800:
            result = result[:800] + "..."
        
        return result

    def process_query(self, question):
        """Processa a pergunta e retorna resposta MELHORADA"""
        question = question.strip()
        
        if not question:
            return {
                "response": "Por favor, faça uma pergunta.",
                "topic": None,
                "source": None
            }
        
        logger.info(f"🔍 Processando pergunta: '{question}'")
        
        # Detectar tópico
        topic = self.detect_topic(question)
        
        if not topic:
            return {
                "response": "Não consegui identificar o tema específico da sua pergunta. Pode mencionar HIV, Malaria, Tuberculose, Gravidez, ou outro tema de saúde?",
                "topic": None,
                "source": None
            }
        
        # Busca semântica MELHORADA
        relevant_doc, doc_name = self.semantic_search(question)
        
        if not relevant_doc:
            return {
                "response": f"Não encontrei informações específicas sobre '{question}' nos documentos disponíveis.",
                "topic": topic,
                "source": None
            }
        
        # Extrair parte MAIS RELEVANTE
        best_response = self.extract_relevant_part(relevant_doc, question, topic)
        
        logger.info(f"✅ Resposta gerada - Tópico: {topic} - Documento: {doc_name}")
        
        return {
            "response": best_response,
            "topic": topic,
            "source": doc_name
        }

    def generate_faq(self, limit=12):
        """Gera perguntas frequentes automaticamente a partir dos documentos"""
        documents_text = ""

        # 1) Ler todos os documentos
        for filename in os.listdir(self.UPLOAD_DIR):
            path = os.path.join(self.UPLOAD_DIR, filename)
            if os.path.isfile(path) and filename.endswith(('.txt', '.pdf', '.docx', '.xlsx')):
                try:
                    if filename.endswith('.txt'):
                        documents_text += self.read_txt(path) + "\n"
                    elif filename.endswith('.pdf'):
                        documents_text += self.read_pdf(path) + "\n"
                    elif filename.endswith('.docx'):
                        documents_text += self.read_docx(path) + "\n"
                    elif filename.endswith('.xlsx'):
                        documents_text += self.read_excel(path) + "\n"
                except:
                    continue
        
        if not documents_text.strip():
            return []

        # 2) Dividir texto em frases
        sentences = re.split(r'(?<=[.!?])\s+', documents_text)

        candidate_faq = []
        question_prefixes = ("como", "quando", "onde", "qual", "quais", "o que", "por que", "quem", "deve", "precisa")
        
        # 3) Selecionar frases relevantes
        for s in sentences:
            s_clean = s.strip()
            s_low = s_clean.lower()

            # Tem perfil de pergunta ou orientação
            if any(p in s_low[:50] for p in question_prefixes):
                if 30 < len(s_clean) < 160:  # evitar frases curtas ou longas demais
                    candidate_faq.append(s_clean)

        # 4) Evitar duplicados e limitar quantidade
        faq_unique = list(dict.fromkeys(candidate_faq))[:limit]

        return faq_unique


# Instância global do bot
jhpiego_bot = JhpiegoBot()