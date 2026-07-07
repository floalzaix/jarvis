#
#   Imports
#

import streamlit as st

from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient

# Perso

from config.config import get_settings
from async_worker import bootstrap_async_worker

#
#   Bootstrap graphiti
#

settings = get_settings()

async_worker = bootstrap_async_worker()

@st.cache_resource
def bootstrap_graphiti() -> Graphiti:
    """
        Bootstraps the Graphiti instance.

        IT uses the Ollama API to generate the facts and the
        embeddings and the neo4j database to store the facts.

        It works as a graph check the Graphiti doc to know more.
    """

    #
    #   LLM client
    #
    
    llm_config = LLMConfig(
        api_key="ollama",  # Ollama doesn't require a real API key
        model=settings.MODEL,
        small_model=settings.MODEL,
        base_url=f"http://localhost:{settings.OLLAMA_PORT}/v1",
    )

    llm_client = OpenAIGenericClient(config=llm_config)

    #
    #   Graphiti
    #
    
    graphiti = Graphiti(
        settings.FACTS_MEMORY_DATABASE_URL,
        settings.FACTS_MEMORY_USERNAME,
        settings.FACTS_MEMORY_PASSWORD,
        llm_client=llm_client,
        embedder=OpenAIEmbedder(
            config=OpenAIEmbedderConfig(
                api_key="ollama",
                embedding_model=settings.EMBEDDER_MODEL,
                embedding_dim=settings.EMBEDDER_DIM,
                base_url=f"http://localhost:{settings.OLLAMA_PORT}/v1",
            )
        ),
        cross_encoder=OpenAIRerankerClient(
            client=llm_client, # type: ignore
            config=llm_config
        ),
    )

    async_worker.run(graphiti.build_indices_and_constraints())

    return graphiti