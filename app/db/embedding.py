"""
文本嵌入模块
使用 sentence-transformers 生成向量嵌入
"""
from typing import List, Optional
import numpy as np

from app.core.config import EMBEDDING_CONFIG
from app.core.logger import logger


class EmbeddingManager:
    """嵌入向量管理器"""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._load_model()

    def _load_model(self):
        """加载嵌入模型"""
        try:
            from sentence_transformers import SentenceTransformer

            model_name = EMBEDDING_CONFIG["model"]
            device = EMBEDDING_CONFIG["device"]

            logger.info(f"Loading embedding model: {model_name}")

            self._model = SentenceTransformer(model_name, device=device)

            logger.info("Embedding model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self._model = None

    def encode(self, text: str, normalize: bool = True) -> Optional[List[float]]:
        """
        将文本编码为向量

        Args:
            text: 输入文本
            normalize: 是否归一化向量

        Returns:
            向量列表，失败返回 None
        """
        try:
            if self._model is None:
                logger.error("Embedding model not loaded")
                return None

            # 编码
            embedding = self._model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
            )

            return embedding.tolist()

        except Exception as e:
            logger.error(f"Failed to encode text: {e}")
            return None

    def encode_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        normalize: bool = True,
    ) -> List[Optional[List[float]]]:
        """
        批量编码文本

        Args:
            texts: 文本列表
            batch_size: 批处理大小
            normalize: 是否归一化

        Returns:
            向量列表
        """
        try:
            if self._model is None:
                logger.error("Embedding model not loaded")
                return [None] * len(texts)

            embeddings = self._model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
                show_progress_bar=len(texts) > 100,
            )

            return [emb.tolist() for emb in embeddings]

        except Exception as e:
            logger.error(f"Failed to batch encode texts: {e}")
            return [None] * len(texts)

    def compute_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float],
    ) -> float:
        """
        计算两个向量的余弦相似度

        Args:
            embedding1: 向量1
            embedding2: 向量2

        Returns:
            余弦相似度 (-1 到 1)
        """
        try:
            v1 = np.array(embedding1)
            v2 = np.array(embedding2)

            # 计算余弦相似度
            dot_product = np.dot(v1, v2)
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            return float(dot_product / (norm1 * norm2))

        except Exception as e:
            logger.error(f"Failed to compute similarity: {e}")
            return 0.0


# 全局实例
embedding_manager = EmbeddingManager()
